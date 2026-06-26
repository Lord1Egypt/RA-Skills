import os
import re
import json
import base64
import argparse
import tempfile
import requests
from lxml import etree
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import pkcs12
from signxml import XMLSigner, SignatureConstructionMethod, SignatureMethod, DigestAlgorithm, CanonicalizationMethod
from dotenv import load_dotenv

load_dotenv(override=True)

class XMLSignerSHA1(XMLSigner):
    def check_deprecated_methods(self):
        pass

def carrega_config(caminho="config.json"):
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)

def gerar_assinatura_cancelamento(im, nfe_numero, chave_privada):
    """
    Assinatura do cancelamento exigida por SP:
    Inscrição Municipal do Prestador (8 posições com zeros à esquerda)
    Número da NFS-e (12 posições com zeros à esquerda)
    """
    im_formatado = str(im).zfill(8)
    nfe_formatado = str(nfe_numero).zfill(12)
    string_assinatura = f"{im_formatado}{nfe_formatado}"
    
    assinatura = chave_privada.sign(
        string_assinatura.encode('utf-8'),
        padding.PKCS1v15(),
        SHA1()
    )
    return base64.b64encode(assinatura).decode('utf-8')

def build_cancelamento(config, nfe_numero, assinatura_canc, chave_pem, cert_pem):
    cnpj = config['cnpj_prestador']
    im = config['inscricao_municipal']
    
    xml_template = f"""<PedidoCancelamentoNFe xmlns="http://www.prefeitura.sp.gov.br/nfe" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <Cabecalho xmlns="" Versao="1">
        <CPFCNPJRemetente>
          <CNPJ>{cnpj}</CNPJ>
        </CPFCNPJRemetente>
        <transacao>false</transacao>
      </Cabecalho>
      <Detalhe xmlns="">
        <ChaveNFe>
          <InscricaoPrestador>{im}</InscricaoPrestador>
          <NumeroNFe>{nfe_numero}</NumeroNFe>
        </ChaveNFe>
        <AssinaturaCancelamento>{assinatura_canc}</AssinaturaCancelamento>
      </Detalhe>
    </PedidoCancelamentoNFe>"""
    
    # Remove espaços entre tags para Canonicalização perfeita
    xml_template = re.sub(r'>\s+<', '><', xml_template.strip())
    
    root = etree.fromstring(xml_template.encode('utf-8'))
    signer = XMLSignerSHA1(
        method=SignatureConstructionMethod.enveloped,
        signature_algorithm=SignatureMethod.RSA_SHA1,
        digest_algorithm=DigestAlgorithm.SHA1,
        c14n_algorithm=CanonicalizationMethod.CANONICAL_XML_1_0,
    )
    root_assinado = signer.sign(root, key=chave_pem, cert=cert_pem)
    return etree.tostring(root_assinado, encoding='unicode').replace('\n', '').replace('\r', '')

def cancelar_nota(nfe_numero):
    config = carrega_config("config.json")
    
    # Carregar Certificado
    with open(config['certificado'], "rb") as f:
        p12_dados = f.read()

    senha_cert = os.environ.get("NFSE_CERT_PASSWORD")
    if not senha_cert:
        return {"sucesso": False, "erros": [{"codigo": "SEC", "descricao": "Senha Ausente"}]}
        
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        chave_privada, certificado, _ = pkcs12.load_key_and_certificates(p12_dados, senha_cert.encode('utf-8'))
    
    chave_pem = chave_privada.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()
    )
    cert_pem = certificado.public_bytes(serialization.Encoding.PEM)

    # Assinatura interna (RPS) de cancelamento
    assinatura_canc = gerar_assinatura_cancelamento(config['inscricao_municipal'], nfe_numero, chave_privada)
    
    # Montar e Assinar o XML de lote final
    xml_assinado = build_cancelamento(config, nfe_numero, assinatura_canc, chave_pem, cert_pem)
    
    # Escapar XML
    xml_escapado = (xml_assinado
                    .replace('&', '&amp;')
                    .replace('<', '&lt;')
                    .replace('>', '&gt;')
                    .replace('"', '&quot;'))

    envelope_soap = f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CancelamentoNFeRequest xmlns="http://www.prefeitura.sp.gov.br/nfe">
      <VersaoSchema>1</VersaoSchema>
      <MensagemXML>{xml_escapado}</MensagemXML>
    </CancelamentoNFeRequest>
  </soap:Body>
</soap:Envelope>"""

    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': '"http://www.prefeitura.sp.gov.br/nfe/ws/cancelamentoNFe"',
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
            timeout=30
        )
        
        with open('debug_cancelamento.xml', 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        if response.status_code == 200:
            root_soap = etree.fromstring(response.text.encode('utf-8'))
            ns = {"soap": "http://schemas.xmlsoap.org/soap/envelope/", "nfe": "http://www.prefeitura.sp.gov.br/nfe"}
            retorno_node = root_soap.xpath('//nfe:RetornoXML', namespaces=ns)
            if retorno_node:
                root_retorno = etree.fromstring(retorno_node[0].text.encode('utf-8'))
                
                sucesso_node = root_retorno.xpath('//Cabecalho/Sucesso')
                if sucesso_node and sucesso_node[0].text.lower() == 'true':
                    # Pode confirmar sucesso lendo a respost
                    return {"sucesso": True, "mensagem": f"NF-e {nfe_numero} cancelada com sucesso!"}
                else:
                    erros = root_retorno.xpath('//Erro')
                    lista_erros = []
                    for erro in erros:
                        cod = erro.xpath('.//Codigo')[0].text
                        desc = erro.xpath('.//Descricao')[0].text
                        lista_erros.append({"codigo": cod, "descricao": desc})
                    return {"sucesso": False, "erros": lista_erros}
            else:
                return {"sucesso": False, "erros": [{"codigo": "N/D", "descricao": "XML Retorno Vazio"}]}
        else:
            return {"sucesso": False, "erros": [{"codigo": str(response.status_code), "descricao": "Erro HTTP"}]}
            
    finally:
        if os.path.exists(temp_cert_path):
            os.remove(temp_cert_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("numero_nfe", type=str, help="Numero da Nota Fiscal a ser cancelada")
    parser.add_argument("--json-out", action="store_true")
    
    args = parser.parse_args()
    
    resultado = cancelar_nota(args.numero_nfe)
    
    if args.json_out:
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    else:
        if resultado["sucesso"]:
            print(f"✅ Sucesso: {resultado['mensagem']}")
        else:
            print("❌ Erro ao cancelar a nota:")
            for e in resultado["erros"]:
                print(f"  [{e['codigo']}] {e['descricao']}")
