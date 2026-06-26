#!/usr/bin/env python3
import os
import re
import sys
import json
import argparse
import tempfile
import requests
import base64
from xml.dom.minidom import parseString
from decimal import Decimal, ROUND_HALF_UP
from dotenv import load_dotenv

load_dotenv(override=True)

from lxml import etree
from signxml import XMLSigner, SignatureConstructionMethod, SignatureMethod, DigestAlgorithm, CanonicalizationMethod
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import pkcs12

IS_JSON_OUT = False
def log(*args, **kwargs):
    if not IS_JSON_OUT:
        print(*args, **kwargs)

class XMLSignerSHA1(XMLSigner):
    """Subclasse para liberar uso de SHA1 exigido pela Prefeitura de SP."""
    def check_deprecated_methods(self):
        pass


def carrega_config(caminho="config.json"):
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        log(f"Erro: Arquivo {caminho} não encontrado.")
        sys.exit(1)


def carrega_dados_nota(caminho):
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        log(f"Erro: Arquivo {caminho} não encontrado.")
        sys.exit(1)


def formata_valor(valor):
    """Formata Decimal para string com 2 casas decimais sem separador de milhar."""
    return f"{Decimal(str(valor)):.2f}"


def limpa_documento(doc):
    """Remove caracteres não numéricos."""
    return re.sub(r'[^0-9]', '', str(doc))


def gerar_assinatura_rps(config, nota):
    """
    Gera o hash RSA-SHA1 da string de assinatura do RPS (Layout v1).
    A exatidão dos espaços e zeros é estritamente validada pela Prefeitura (Erro 1057).
    """
    v_servicos = int(Decimal(str(nota['valor_servicos'])) * 100)
    v_deducoes = int(Decimal(str(nota.get('valor_deducoes', 0))) * 100)
    
    # Campo 1: 8 posicoes, zeros a esquerda
    inscricao_prestador = str(config['inscricao_municipal']).zfill(8)
    # Campo 2: 5 posicoes, espacos a direita
    serie = str(config['serie_rps']).ljust(5)
    # Campo 3: 12 posicoes, zeros a esquerda
    numero = str(nota['numero_rps']).zfill(12)
    # Campo 4: 8 posicoes, AAAAMMDD
    data = str(nota['data_emissao']).replace('-', '')[:8]
    # Campo 5: 1 posicao (na v1, TributacaoRPS tem 1 caractere, nao 2!)
    tributacao = str(config['tributacao_rps']).ljust(1)
    # Campo 6: 1 posicao
    status = str(nota['status_rps'])
    # Campo 7: 1 posicao ('S' ou 'N')
    iss_retido = str(nota['iss_retido'])
    # Campo 8: 15 posicoes, zeros a esquerda
    vr_servico = str(v_servicos).zfill(15)
    # Campo 9: 15 posicoes, zeros a esquerda
    vr_deducao = str(v_deducoes).zfill(15)
    # Campo 10: 5 posicoes, zeros a esquerda
    codigo_servico = str(config['codigo_servico']).zfill(5)
    # Campo 11: 1 posicao
    ind_tomador = str(nota['indicador_tomador'])
    # Campo 12: 14 posicoes, zeros a esquerda
    doc_tomador = limpa_documento(nota.get('documento_tomador', '')).zfill(14)

    string_rps = (
        inscricao_prestador +
        serie +
        numero +
        data +
        tributacao +
        status +
        iss_retido +
        vr_servico +
        vr_deducao +
        codigo_servico +
        ind_tomador +
        doc_tomador
    )
    
    # Para debug de Erro 1057: mostrar a string (oculta em producao normal, mas util aqui)
    log(f"    (debug) RPS String   : '{string_rps}' (len: {len(string_rps)})")
    
    # É crucial gerar do certificado P12 recarrega-lo e assinar
    with open(config['certificado'], "rb") as f:
        p12_dados = f.read()
        
    senha_cert = os.environ.get("NFSE_CERT_PASSWORD") or config.get('senha_certificado', '')
    if not senha_cert:
        return "" # Will implicitly fail upstream or could raise, handled gracefully by emitir_nota
        
    chave_privada, _, _ = pkcs12.load_key_and_certificates(
        p12_dados, senha_cert.encode('utf-8')
    )
    
    assinatura_bytes = chave_privada.sign(
        string_rps.encode('ascii'),
        padding.PKCS1v15(),
        hashes.SHA1()
    )
    return base64.b64encode(assinatura_bytes).decode('ascii')


def processar_resposta(xml_resposta):
    """
    Parseia a resposta da Prefeitura que retorna no RetornoXML (escapado ou cdata).
    """
    try:
        root_soap = etree.fromstring(xml_resposta.encode('utf-8'))
        
        # O namespace do SOAP
        ns = {"soap": "http://schemas.xmlsoap.org/soap/envelope/",
              "nfe": "http://www.prefeitura.sp.gov.br/nfe"}
              
        # Pode estar em TesteEnvioLoteRPSResponse ou EnvioLoteRPSResponse
        retorno_node = root_soap.xpath('//nfe:RetornoXML', namespaces=ns)
        
        if not retorno_node:
            log("❌ ERRO: Elemento 'RetornoXML' não encontrado na resposta SOAP.")
            return False

        retorno_xml_str = retorno_node[0].text
        root_retorno = etree.fromstring(retorno_xml_str.encode('utf-8'))
        
        # Analisando o sucesso/erros
        sucesso_node = root_retorno.xpath('//Cabecalho/Sucesso')
        if sucesso_node:
            sucesso = sucesso_node[0].text.lower() == 'true'
            
            if sucesso:
                log("✅ Lote recebido com sucesso!")
                chaves = root_retorno.xpath('//ChaveNFeRPS')
                notas_geradas = []
                for ch in chaves:
                    # Tenta capturar a Chave oficial da NF-e (que vem se convertida com sucesso)
                    nfe = ch.xpath('.//ChaveNFe/NumeroNFe')
                    nfe_num = nfe[0].text if nfe else "N/D"
                    
                    # Tenta capturar dados extras para gerar o PDF
                    cod_ver = ch.xpath('.//ChaveNFe/CodigoVerificacao')
                    cod_ver_text = cod_ver[0].text if cod_ver else ""
                    
                    insc_prest = ch.xpath('.//ChaveNFe/InscricaoPrestador')
                    insc_text = insc_prest[0].text if insc_prest else ""
                    
                    url_pdf = ""
                    if nfe_num != "N/D" and cod_ver_text and insc_text:
                        url_pdf = f"https://nfe.prefeitura.sp.gov.br/contribuinte/notaprint.aspx?inscricao={insc_text}&nf={nfe_num}&verificacao={cod_ver_text}"

                    notas_geradas.append({
                        "numero": nfe_num,
                        "url_pdf": url_pdf
                    })
                    log(f"   => NFS-e Gerada: {nfe_num}")
                    if url_pdf:
                        log(f"   => Link PDF: {url_pdf}")
                return {"sucesso": True, "notas_geradas": notas_geradas}
            else:
                log("❌ Falha no processamento do lote:")
                erros = root_retorno.xpath('//Erro')
                lista_erros = []
                for erro in erros:
                    codigo = erro.xpath('.//Codigo')[0].text
                    desc = erro.xpath('.//Descricao')[0].text
                    lista_erros.append({"codigo": codigo, "descricao": desc})
                    log(f"   - [Erro {codigo}] {desc}")
                    
                alertas = root_retorno.xpath('//Alerta')
                lista_alertas = []
                for alerta in alertas:
                    codigo = alerta.xpath('.//Codigo')[0].text
                    desc = alerta.xpath('.//Descricao')[0].text
                    lista_alertas.append({"codigo": codigo, "descricao": desc})
                    log(f"   - [Alerta {codigo}] {desc}")
                return {"sucesso": False, "erros": lista_erros, "alertas": lista_alertas}
        else:
            log("❌ Resposta inesperada: não foi possível encontrar <Sucesso>")
            return {"sucesso": False, "erros": [{"codigo": "N/D", "descricao": "Resposta inesperada sem tag Sucesso"}]}
            
    except etree.XMLSyntaxError as e:
        log(f"❌ Erro ao parsear XML de retorno: {e}")
        return {"sucesso": False, "erros": [{"codigo": "XML", "descricao": str(e)}]}
    except Exception as e:
        log(f"❌ Ocorreu um erro ao processar a resposta: {e}")
        return {"sucesso": False, "erros": [{"codigo": "EXC", "descricao": str(e)}]}

def construir_xml_lote(config, nota, assinatura_rps):
    """
    Constrói o XML `<PedidoEnvioLoteRPS>` e seus elementos internos.
    """
    # Lógica de cálculo de Retenções
    calcular = nota.get('calcular_retencoes', False)
    retencoes = config.get('retencoes_federais', {})
    limites = config.get('limites_retencao', {'irrf': 10.0, 'csrf': 10.0})
    
    val_servicos = Decimal(str(nota['valor_servicos']))
    v_pis = Decimal('0.00')
    v_cofins = Decimal('0.00')
    v_inss = Decimal('0.00')
    v_ir = Decimal('0.00')
    v_csll = Decimal('0.00')

    texto_retencoes = ""
    itens_retencao = []
    
    if calcular and retencoes:
        # Calcular valores brutos primeiro
        if retencoes.get('pis', 0) > 0:
            v_pis = (val_servicos * Decimal(str(retencoes['pis'])) / 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if retencoes.get('cofins', 0) > 0:
            v_cofins = (val_servicos * Decimal(str(retencoes['cofins'])) / 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if retencoes.get('inss', 0) > 0:
            v_inss = (val_servicos * Decimal(str(retencoes['inss'])) / 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if retencoes.get('ir', 0) > 0:
            v_ir = (val_servicos * Decimal(str(retencoes['ir'])) / 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if retencoes.get('csll', 0) > 0:
            v_csll = (val_servicos * Decimal(str(retencoes['csll'])) / 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Tratar limiares configuráveis (Art. 31 Lei 10.833 e alterações, DARF mínimo IR)
        limite_csrf = Decimal(str(limites.get('csrf', 10.0)))
        limite_irrf = Decimal(str(limites.get('irrf', 10.0)))
        
        # O IRRF é dispensado se o valor do IR for <= ao limite (geralmente R$ 10,00)
        if v_ir <= limite_irrf:
            v_ir = Decimal('0.00')
            
        # A CSRF (PIS, COFINS, CSLL) só é retida se a soma das contribuições for > ao limite (geralmente R$ 10,00)
        soma_csrf = v_pis + v_cofins + v_csll
        if soma_csrf <= limite_csrf:
            v_pis = Decimal('0.00')
            v_cofins = Decimal('0.00')
            v_csll = Decimal('0.00')

        # Montar os textos baseados nos novos valores validados
        if v_pis > 0:
            itens_retencao.append(f"PIS {str(retencoes['pis']).replace('.', ',')}%: R$ {formata_valor(v_pis)}")
        if v_cofins > 0:
            itens_retencao.append(f"COFINS {str(retencoes['cofins']).replace('.', ',')}%: R$ {formata_valor(v_cofins)}")
        if v_inss > 0:
            # INSS tem regras próprias, mantemos como foi retido independentemente de CSRF e IR
            itens_retencao.append(f"INSS {str(retencoes['inss']).replace('.', ',')}%: R$ {formata_valor(v_inss)}")
        if v_ir > 0:
            itens_retencao.append(f"IRRF {str(retencoes['ir']).replace('.', ',')}%: R$ {formata_valor(v_ir)}")
        if v_csll > 0:
            itens_retencao.append(f"CSLL {str(retencoes['csll']).replace('.', ',')}%: R$ {formata_valor(v_csll)}")

    texto_disc = str(nota.get('discriminacao', '')).strip()
    if itens_retencao:
        texto_disc += " | Retenções Federais: " + " / ".join(itens_retencao)
    
    msg_padrao = config.get('mensagem_padrao', '')
    if msg_padrao:
        texto_disc += f" | {msg_padrao.strip()}"
        
    texto_disc = texto_disc.strip(' |')

    xml_template = f"""<PedidoEnvioLoteRPS xmlns="http://www.prefeitura.sp.gov.br/nfe" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <Cabecalho xmlns="" Versao="1">
            <CPFCNPJRemetente>
                <CNPJ>{config['cnpj_prestador']}</CNPJ>
            </CPFCNPJRemetente>
            <transacao>false</transacao>
            <dtInicio>{nota['data_emissao']}</dtInicio>
            <dtFim>{nota['data_emissao']}</dtFim>
            <QtdRPS>1</QtdRPS>
            <ValorTotalServicos>{formata_valor(nota['valor_servicos'])}</ValorTotalServicos>
            <ValorTotalDeducoes>{formata_valor(nota.get('valor_deducoes', 0))}</ValorTotalDeducoes>
        </Cabecalho>
        <RPS xmlns="">
            <Assinatura>{assinatura_rps}</Assinatura>
            <ChaveRPS>
                <InscricaoPrestador>{config['inscricao_municipal']}</InscricaoPrestador>
                <SerieRPS>{config['serie_rps']}</SerieRPS>
                <NumeroRPS>{nota['numero_rps']}</NumeroRPS>
            </ChaveRPS>
            <TipoRPS>RPS</TipoRPS>
            <DataEmissao>{nota['data_emissao']}</DataEmissao>
            <StatusRPS>{nota['status_rps']}</StatusRPS>
            <TributacaoRPS>{config['tributacao_rps']}</TributacaoRPS>
            <ValorServicos>{formata_valor(nota['valor_servicos'])}</ValorServicos>
            <ValorDeducoes>{formata_valor(nota.get('valor_deducoes', 0))}</ValorDeducoes>
            {f"<ValorPIS>{formata_valor(v_pis)}</ValorPIS>" if v_pis > 0 else ""}
            {f"<ValorCOFINS>{formata_valor(v_cofins)}</ValorCOFINS>" if v_cofins > 0 else ""}
            {f"<ValorINSS>{formata_valor(v_inss)}</ValorINSS>" if v_inss > 0 else ""}
            {f"<ValorIR>{formata_valor(v_ir)}</ValorIR>" if v_ir > 0 else ""}
            {f"<ValorCSLL>{formata_valor(v_csll)}</ValorCSLL>" if v_csll > 0 else ""}
            <CodigoServico>{config['codigo_servico']}</CodigoServico>
            <AliquotaServicos>{config['aliquota_servicos']}</AliquotaServicos>
            <ISSRetido>{'true' if nota['iss_retido'] == 'S' else 'false'}</ISSRetido>
            <CPFCNPJTomador>
                <{'CNPJ' if nota['indicador_tomador'] == 2 else 'CPF'}>{limpa_documento(nota.get('documento_tomador', ''))}</{'CNPJ' if nota['indicador_tomador'] == 2 else 'CPF'}>
            </CPFCNPJTomador>
            <RazaoSocialTomador>{nota.get('razao_social_tomador', '')[:75]}</RazaoSocialTomador>
            """
            
    # Adicionar endereço tomador se existir
    end = nota.get('endereco_tomador', {})
    if end:
        xml_template += f"""<EnderecoTomador>
                <TipoLogradouro></TipoLogradouro>
                <Logradouro>{end.get('logradouro', '')[:50]}</Logradouro>
                <NumeroEndereco>{end.get('numero', '')[:10]}</NumeroEndereco>
                <ComplementoEndereco>{end.get('complemento', '')[:30]}</ComplementoEndereco>
                <Bairro>{end.get('bairro', '')[:30]}</Bairro>
                <Cidade>{end.get('cidade', '')}</Cidade>
                <UF>{end.get('uf', '')}</UF>
                <CEP>{limpa_documento(end.get('cep', ''))}</CEP>
            </EnderecoTomador>
            """
            
    if nota.get('email_tomador'):
        xml_template += f"<EmailTomador>{nota['email_tomador'][:75]}</EmailTomador>\n"
        
    xml_template += f"""<Discriminacao>{texto_disc[:2000]}</Discriminacao>
        </RPS>
    </PedidoEnvioLoteRPS>"""
    
    # Remove whitespace/tabs extra for proper C14N digest (though C14N normalizes, it's cleaner)
    return re.sub(r'>\s+<', '><', xml_template.strip())


def assinar_lote(xml_str, chave_pem, cert_pem):
    """Aplica XMLDSig ao lote inteiro."""
    root = etree.fromstring(xml_str.encode('utf-8'))
    
    signer = XMLSignerSHA1(
        method=SignatureConstructionMethod.enveloped,
        signature_algorithm=SignatureMethod.RSA_SHA1,
        digest_algorithm=DigestAlgorithm.SHA1,
        c14n_algorithm=CanonicalizationMethod.CANONICAL_XML_1_0,
    )
    
    root_assinado = signer.sign(root, key=chave_pem, cert=cert_pem)
    xml = etree.tostring(root_assinado, encoding='unicode')
    # Removed regex that stripped `ds:` because tampering with the XML AFTER signing invalidates the Reference DigestValue and SignedInfo hashes!
    return xml.replace('\n', '').replace('\r', '')


def emitir_nota(config_file, dados_file, modo):
    log("=" * 60)
    log(f"  NFS-e São Paulo - Emissão (Modo: {modo.upper()})")
    log("=" * 60)

    config = carrega_config(config_file)
    nota = carrega_dados_nota(dados_file)

    with open(config['certificado'], "rb") as f:
        p12_dados = f.read()

    log("[1/5] Carregando certificados...")
    
    # Segurança: Lendo senha da variável de ambiente primeiro, senão do fallback no json
    senha_cert = os.environ.get("NFSE_CERT_PASSWORD") or config.get('senha_certificado', '')
    if not senha_cert:
        log("❌ Erro: Senha do certificado não encontrada (variável NFSE_CERT_PASSWORD ou config.json).")
        return {"sucesso": False, "erros": [{"codigo": "SEC", "descricao": "Senha do certificado Ausente"}]}
        
    chave_privada, certificado, _ = pkcs12.load_key_and_certificates(
        p12_dados, senha_cert.encode('utf-8')
    )
    chave_pem = chave_privada.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()
    )
    cert_pem = certificado.public_bytes(serialization.Encoding.PEM)

    log("[2/5] Gerando assinatura interna RPS...")
    assinatura_rps = gerar_assinatura_rps(config, nota)

    log("[3/5] Montando XML do lote...")
    xml_nao_assinado = construir_xml_lote(config, nota, assinatura_rps)

    log("[4/5] Assinando digitalmente (XMLDSig)...")
    xml_assinado = assinar_lote(xml_nao_assinado, chave_pem, cert_pem)
    
    # Faz escape do XML interno para ser inserido no campo `MensagemXML` (que é string)
    xml_escapado = (xml_assinado
                    .replace('&', '&amp;')
                    .replace('<', '&lt;')
                    .replace('>', '&gt;')
                    .replace('"', '&quot;'))

    log("[5/5] Enviando para prefeitura...")
    
    if modo == 'teste':
        wrapper_tag = 'TesteEnvioLoteRPSRequest'
        soap_action = '"http://www.prefeitura.sp.gov.br/nfe/ws/testeenvio"'
    else:
        # Modo produção real!
        wrapper_tag = 'EnvioLoteRPSRequest'
        soap_action = '"http://www.prefeitura.sp.gov.br/nfe/ws/envioLoteRPS"'

    envelope_soap = f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <{wrapper_tag} xmlns="http://www.prefeitura.sp.gov.br/nfe">
      <VersaoSchema>1</VersaoSchema>
      <MensagemXML>{xml_escapado}</MensagemXML>
    </{wrapper_tag}>
  </soap:Body>
</soap:Envelope>"""

    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': soap_action,
    }

    url = "https://nfews.prefeitura.sp.gov.br/lotenfe.asmx"

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pem") as temp_cert:
        temp_cert.write(chave_pem + b'\n' + cert_pem)
        temp_cert_path = temp_cert.name

    try:
        response = requests.post(
            url,
            data=envelope_soap.encode('utf-8'),
            headers=headers,
            cert=temp_cert_path,
            timeout=30,
            allow_redirects=False,
        )

        with open('debug_resposta_prod.xml', 'w', encoding='utf-8') as f:
            f.write(response.text)

        if response.status_code == 200:
            return processar_resposta(response.text)
        else:
            log(f"❌ Erro de HTTP: {response.status_code}")
            log(response.text[:500])
            return {"sucesso": False, "erros": [{"codigo": str(response.status_code), "descricao": "Erro HTTP da prefeitura"}]}
            
    finally:
        if os.path.exists(temp_cert_path):
            os.remove(temp_cert_path)
            
    log("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Emissor de NFS-e SP")
    parser.add_argument("--modo", choices=['teste', 'producao'], default='teste',
                        help="Modo de operação: 'teste' (TesteEnvioLoteRPS) ou 'producao' (EnvioLoteRPS)")
    parser.add_argument("--config", default="config.json", help="Arquivo de configuracao")
    parser.add_argument("--dados", default="dados_nota.json", help="Arquivo com os dados do RPS/Nota")
    parser.add_argument("--json-out", action="store_true", help="Retorna apenas a saida JSON")
    
    args = parser.parse_args()
    
    if args.json_out:
        IS_JSON_OUT = True
        import warnings
        warnings.filterwarnings('ignore')
        
    resultado = emitir_nota(args.config, args.dados, args.modo)
    
    if args.json_out and resultado:
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
