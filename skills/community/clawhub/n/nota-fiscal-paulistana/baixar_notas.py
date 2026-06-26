import os
import json
import argparse
import tempfile
import warnings
from datetime import datetime, timedelta

import requests
from lxml import etree
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12
from dotenv import load_dotenv

# Ignora os warnings de PKCS12 parse antigos que poluem o console
warnings.filterwarnings("ignore", category=UserWarning, module="cryptography")

load_dotenv(override=True)

from signxml import XMLSigner, SignatureConstructionMethod, SignatureMethod, DigestAlgorithm, CanonicalizationMethod
import re

class XMLSignerSHA1(XMLSigner):
    def check_deprecated_methods(self):
        pass

def carrega_config(caminho="config.json"):
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)

def consultar_periodo(config, data_inicio, data_fim):
    """
    Envia a requisição ConsultaNFeEmitidasRequest para a Prefeitura
    e retorna o JSON parsed com as notas contábeis.
    """
    with open(config['certificado'], "rb") as f:
        p12_dados = f.read()

    senha_cert = os.environ.get("NFSE_CERT_PASSWORD", "")
    if not senha_cert:
        print("❌ Senha do certificado não encontrada na variável NFSE_CERT_PASSWORD.")
        return []

    chave_privada, certificado, _ = pkcs12.load_key_and_certificates(
        p12_dados, senha_cert.encode('utf-8')
    )
    
    chave_pem = chave_privada.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()
    )
    cert_pem = certificado.public_bytes(serialization.Encoding.PEM)

    cnpj = config['cnpj_prestador']
    im = config['inscricao_municipal']

    # Montar o XML interno a ser Assinado (A prefeitura exige tudo dentro de Cabecalho)
    xml_interno = f"""<PedidoConsultaNFePeriodo xmlns="http://www.prefeitura.sp.gov.br/nfe" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <Cabecalho xmlns="" Versao="1">
        <CPFCNPJRemetente>
          <CNPJ>{cnpj}</CNPJ>
        </CPFCNPJRemetente>
        <CPFCNPJ>
          <CNPJ>{cnpj}</CNPJ>
        </CPFCNPJ>
        <Inscricao>{im}</Inscricao>
        <dtInicio>{data_inicio}</dtInicio>
        <dtFim>{data_fim}</dtFim>
        <NumeroPagina>1</NumeroPagina>
      </Cabecalho>
    </PedidoConsultaNFePeriodo>"""

    # Canonicaliza removendo espacos entre tags
    xml_interno = re.sub(r'>\s+<', '><', xml_interno.strip())
    
    # Assina XML Interno
    root_interno = etree.fromstring(xml_interno.encode('utf-8'))
    signer = XMLSignerSHA1(
        method=SignatureConstructionMethod.enveloped,
        signature_algorithm=SignatureMethod.RSA_SHA1,
        digest_algorithm=DigestAlgorithm.SHA1,
        c14n_algorithm=CanonicalizationMethod.CANONICAL_XML_1_0,
    )
    root_assinado = signer.sign(root_interno, key=chave_pem, cert=cert_pem)
    xml_assinado_str = etree.tostring(root_assinado, encoding='unicode').replace('\n', '').replace('\r', '')

    # Escapar XML assinado para colocar no SOAP Envelope
    xml_escapado = (xml_assinado_str
                    .replace('&', '&amp;')
                    .replace('<', '&lt;')
                    .replace('>', '&gt;')
                    .replace('"', '&quot;'))

    # Envelope SOAP
    xml_consulta = f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ConsultaNFeEmitidasRequest xmlns="http://www.prefeitura.sp.gov.br/nfe">
      <VersaoSchema>1</VersaoSchema>
      <MensagemXML>&lt;?xml version="1.0" encoding="UTF-8"?&gt;{xml_escapado}</MensagemXML>
    </ConsultaNFeEmitidasRequest>
  </soap:Body>
</soap:Envelope>"""

    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': '"http://www.prefeitura.sp.gov.br/nfe/ws/consultaNFeEmitidas"',
    }

    url = "https://nfews.prefeitura.sp.gov.br/lotenfe.asmx"

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pem") as temp_cert:
        temp_cert.write(chave_pem + b'\n' + cert_pem)
        temp_cert_path = temp_cert.name

    try:
        response = requests.post(
            url,
            data=xml_consulta.encode('utf-8'),
            headers=headers,
            cert=temp_cert_path,
            timeout=30
        )

        if response.status_code != 200:
            print(f"❌ Erro HTTP {response.status_code}")
            return []

        # Parsear o retorno SOAP
        root_soap = etree.fromstring(response.text.encode('utf-8'))
        ns = {"soap": "http://schemas.xmlsoap.org/soap/envelope/", "nfe": "http://www.prefeitura.sp.gov.br/nfe"}
        retorno_node = root_soap.xpath('//nfe:RetornoXML', namespaces=ns)
        
        if not retorno_node:
            print("❌ RetornoXML não encontrado na resposta.")
            return []

        root_retorno = etree.fromstring(retorno_node[0].text.encode('utf-8'))
        
        notas = []
        nfe_nodes = root_retorno.xpath('.//nfe:NFe', namespaces=ns)
        
        if not nfe_nodes:
            # Pode ser que o XPath precise ser sem namespace ou o conteudo tenha erros.
            nfe_nodes = root_retorno.xpath('.//NFe')
            if not nfe_nodes:
                print("   [DEBUG] Nenhuma <NFe> encontrada no retorno. O XML retornado foi:")
                print(response.text[:2000]) # Imprime um pedaço do XML para diagnóstico
                
                # Tem mensagem de erro?
                mensagens = root_retorno.xpath('.//MensagemRetorno') or root_retorno.xpath('.//nfe:MensagemRetorno', namespaces=ns)
                for msg in mensagens:
                    codigo = msg.xpath('.//Codigo') or msg.xpath('.//nfe:Codigo', namespaces=ns)
                    desc = msg.xpath('.//Descricao') or msg.xpath('.//nfe:Descricao', namespaces=ns)
                    c = codigo[0].text if codigo else "N/A"
                    d = desc[0].text if desc else "N/A"
                    print(f"   [ERRO API] Código: {c} - {d}")
                
        for nfe in nfe_nodes:
            # Helper function para pegar texto com fallback
            def get_text(xpath_query):
                elm = nfe.xpath(xpath_query)
                return elm[0].text if elm and elm[0].text else ""
            
            # Helper function para pegar número flutuante
            def get_float(xpath_query):
                val = get_text(xpath_query)
                return float(val) if val else 0.0

            # Extracao de Dados Contabeis da NFE
            nota_dict = {
                "numero_nfe": get_text('.//ChaveNFe/NumeroNFe'),
                "codigo_verificacao": get_text('.//ChaveNFe/CodigoVerificacao'),
                "data_emissao": get_text('.//DataEmissaoNFe'),
                "status": get_text('.//StatusNFe'), # N = Normal, C = Cancelada
                "valor_servicos": get_float('.//ValorServicos'),
                "valor_pis": get_float('.//ValorPIS'),
                "valor_cofins": get_float('.//ValorCOFINS'),
                "valor_ir": get_float('.//ValorIR'),
                "valor_csll": get_float('.//ValorCSLL'),
                "valor_iss": get_float('.//ValorISS'),
                "tomador": {
                    "documento": get_text('.//CPFCNPJTomador/CNPJ') or get_text('.//CPFCNPJTomador/CPF'),
                    "razao_social": get_text('.//RazaoSocialTomador'),
                    "email": get_text('.//EmailTomador')
                }
            }
            notas.append(nota_dict)
            
        return notas
        
    finally:
        if os.path.exists(temp_cert_path):
            os.remove(temp_cert_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exportador de Notas Fiscais para Contabilidade")
    parser.add_argument("--dias", type=int, default=30, help="Busca retroativa em dias caso não informe datas (padrão 30).")
    parser.add_argument("--inicio", type=str, help="Data de início (Formato: YYYY-MM-DD) Ex: 2026-01-01")
    parser.add_argument("--fim", type=str, help="Data de fim (Formato: YYYY-MM-DD) Ex: 2026-12-31")
    parser.add_argument("--out", type=str, default="nfse_contabilidade.json", help="Nome do arquivo JSON de saida")
    
    args = parser.parse_args()
    
    # Define as Datas de Busca
    hoje = datetime.now()
    if args.inicio and args.fim:
        data_ini_obj = datetime.strptime(args.inicio, "%Y-%m-%d")
        data_fim_obj = datetime.strptime(args.fim, "%Y-%m-%d")
    else:
        data_fim_obj = hoje
        data_ini_obj = hoje - timedelta(days=args.dias)
    
    print("=" * 60)
    print(f"📊 Relatório Contábil (Período: {data_ini_obj.strftime('%Y-%m-%d')} até {data_fim_obj.strftime('%Y-%m-%d')})")
    
    config = carrega_config()
    todas_notas = []
    
    # Motor de paginação (A Prefeitura bloqueia pesquisas de > 30 dias)
    # Se o range for grande, nosso script fatiará sozinho em abas de 30 dias:
    cursor_ini = data_ini_obj
    while cursor_ini <= data_fim_obj:
        cursor_fim = min(cursor_ini + timedelta(days=29), data_fim_obj)
        str_ini = cursor_ini.strftime("%Y-%m-%d")
        str_fim = cursor_fim.strftime("%Y-%m-%d")
        
        print(f"   ⏳ Batch Consultando: {str_ini} a {str_fim}...")
        notas_periodo = consultar_periodo(config, str_ini, str_fim)
        
        if notas_periodo:
            todas_notas.extend(notas_periodo)
            
        cursor_ini = cursor_fim + timedelta(days=1)
    
    if todas_notas:
        print(f"✅ Download concluído! Foram processadas {len(todas_notas)} notas fiscais no período unificado.")
        
        # Filtra apenas as notas válidas (não Canceladas)
        notas_ativas = [n for n in todas_notas if n['status'] == 'N']
        valor_total = sum([n['valor_servicos'] for n in notas_ativas])
        
        print(f"   => Notas Ativas: {len(notas_ativas)}")
        print(f"   => Valor Faturado (Bruto Ativo): R$ {valor_total:,.2f}")
        
        with open(args.out, 'w', encoding='utf-8') as f:
            json.dump(todas_notas, f, indent=4, ensure_ascii=False)
            
        print(f"📁 Extrato contábil unificado salvo em: {args.out}")
        print("=" * 60)
    else:
        print("⚠ Nenhuma nota encontrada no período especificado ou houve falha na conexão.")
