import os
import re
import json
import base64
import requests
from lxml import etree
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12
from signxml import XMLSigner, SignatureConstructionMethod, SignatureMethod, DigestAlgorithm, CanonicalizationMethod
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class XMLSignerSHA1(XMLSigner):
    def check_deprecated_methods(self):
        pass

def carrega_config(caminho="config.json"):
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_consulta(config, chave_pem, cert_pem):
    # SP API requires YYYY-MM-DD
    hoje = datetime.now()
    inicio = (hoje - timedelta(days=30)).strftime('%Y-%m-%d')
    fim = hoje.strftime('%Y-%m-%d')
    
    xml_template = f"""<PedidoConsultaNFePeriodo xmlns="http://www.prefeitura.sp.gov.br/nfe" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <Cabecalho xmlns="" Versao="1">
            <CPFCNPJRemetente>
                <CNPJ>{config['cnpj_prestador']}</CNPJ>
            </CPFCNPJRemetente>
            <CPFCNPJ>
                <CNPJ>{config['cnpj_prestador']}</CNPJ>
            </CPFCNPJ>
            <Inscricao>{config['inscricao_municipal']}</Inscricao>
            <dtInicio>{inicio}</dtInicio>
            <dtFim>{fim}</dtFim>
            <NumeroPagina>1</NumeroPagina>
        </Cabecalho>
    </PedidoConsultaNFePeriodo>"""
    
    xml_template = re.sub(r'>\s+<', '><', xml_template.strip())
    
    root = etree.fromstring(xml_template.encode('utf-8'))
    signer = XMLSignerSHA1(
        method=SignatureConstructionMethod.enveloped,
        signature_algorithm=SignatureMethod.RSA_SHA1,
        digest_algorithm=DigestAlgorithm.SHA1,
        c14n_algorithm=CanonicalizationMethod.CANONICAL_XML_1_0,
    )
    root_assinado = signer.sign(root, key=chave_pem, cert=cert_pem)
    xml_assinado = etree.tostring(root_assinado, encoding='unicode').replace('\n', '').replace('\r', '')
    
    return xml_assinado

def main():
    config = carrega_config()
    with open(config['certificado'], "rb") as f:
        p12_dados = f.read()

    senha_cert = os.environ.get("NFSE_CERT_PASSWORD")
    if not senha_cert:
        print("Senha NFSE_CERT_PASSWORD nao encontrada.")
        return

    chave_privada, certificado, _ = pkcs12.load_key_and_certificates(p12_dados, senha_cert.encode('utf-8'))
    chave_pem = chave_privada.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
    cert_pem = certificado.public_bytes(serialization.Encoding.PEM)

    xml_assinado = build_consulta(config, chave_pem, cert_pem)
    
    xml_escapado = (xml_assinado
                    .replace('&', '&amp;')
                    .replace('<', '&lt;')
                    .replace('>', '&gt;')
                    .replace('"', '&quot;'))

    envelope_soap = f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ConsultaNFeEmitidasRequest xmlns="http://www.prefeitura.sp.gov.br/nfe">
      <VersaoSchema>1</VersaoSchema>
      <MensagemXML>{xml_escapado}</MensagemXML>
    </ConsultaNFeEmitidasRequest>
  </soap:Body>
</soap:Envelope>"""

    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': '"http://www.prefeitura.sp.gov.br/nfe/ws/consultaNFeEmitidas"',
    }

    url = "https://nfews.prefeitura.sp.gov.br/lotenfe.asmx"
    
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pem") as temp_cert:
        temp_cert.write(chave_pem + b'\n' + cert_pem)
        temp_cert_path = temp_cert.name

    try:
        print("Consultando API da prefeitura...")
        response = requests.post(url, data=envelope_soap.encode('utf-8'), headers=headers, cert=temp_cert_path, timeout=30)
        print("Status code:", response.status_code)
        
        with open("resposta_consulta.xml", "w") as f:
            f.write(response.text)
            
        if response.status_code == 200:
            root_soap = etree.fromstring(response.text.encode('utf-8'))
            ns = {"soap": "http://schemas.xmlsoap.org/soap/envelope/", "nfe": "http://www.prefeitura.sp.gov.br/nfe"}
            retorno_node = root_soap.xpath('//nfe:RetornoXML', namespaces=ns)
            if retorno_node:
                root_retorno = etree.fromstring(retorno_node[0].text.encode('utf-8'))
                sucesso_node = root_retorno.xpath('//Cabecalho/Sucesso')
                if sucesso_node and sucesso_node[0].text.lower() == 'true':
                    print("Sucesso! Buscando ultimo RPS ou Nota...")
                    rps_list = root_retorno.xpath('//ChaveRPS/NumeroRPS')
                    nfe_list = root_retorno.xpath('//ChaveNFe/NumeroNFe')
                    
                    maior_rps = 0
                    maior_nfe = 0
                    
                    if rps_list:
                        numeros = [int(n.text) for n in rps_list if n.text and n.text.isdigit()]
                        if numeros: maior_rps = max(numeros)
                        
                    if nfe_list:
                        numeros = [int(n.text) for n in nfe_list if n.text and n.text.isdigit()]
                        if numeros: maior_nfe = max(numeros)
                        
                    print(f"MAIOR ENCONTRADO - RPS: {maior_rps} | NFe: {maior_nfe}")
                else:
                    print("Falha na consulta:")
                    erros = root_retorno.xpath('//Erro')
                    for e in erros:
                        print(f"[{e.xpath('.//Codigo')[0].text}] {e.xpath('.//Descricao')[0].text}")
    finally:
        if os.path.exists(temp_cert_path):
            os.remove(temp_cert_path)

if __name__ == '__main__':
    main()
