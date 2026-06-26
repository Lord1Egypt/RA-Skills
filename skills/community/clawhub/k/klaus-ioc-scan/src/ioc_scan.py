#!/usr/bin/env python3
"""
Klaus IOC Scanner
Analisa URLs, domínios e IPs usando VirusTotal e AbuseIPDB
"""

import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.parse
from typing import Dict, List, Optional, Tuple

import requests

# Configuração
VIRUSTOTAL_API_KEY = os.environ.get("VIRUSTOTAL_API_KEY", "")
ABUSEIPDB_API_KEY = os.environ.get("ABUSEIPDB_API_KEY", "")
VT_API_URL_V2 = "https://www.virustotal.com/vtapi/v2"
ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2"


def extract_iocs(text: str) -> List[Tuple[str, str]]:
    """Extrai IOCs (URL, domínio, IP) do texto."""
    iocs = []
    
    # URLs
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(url_pattern, text)
    for url in urls:
        url = url.rstrip('.,;:)]\"')
        iocs.append((url, 'url'))
    
    # IPv4
    ip_pattern = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    ips = re.findall(ip_pattern, text)
    for ip in ips:
        # Ignora IPs privados comuns
        if not ip.startswith(('10.', '192.168.', '172.16.', '127.', '169.254.', '0.')):
            iocs.append((ip, 'ip'))
    
    # Domínios (após remover URLs e IPs)
    text_sem_url = text
    for url in urls:
        text_sem_url = text_sem_url.replace(url, '')
    for ip in ips:
        text_sem_url = text_sem_url.replace(ip, '')
    
    # Domínio pattern
    domain_pattern = r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
    domains = re.findall(domain_pattern, text_sem_url.lower())
    for domain in domains:
        # Ignora TLDs comuns e palavras largas
        if domain not in ['com.br', 'gov.br', 'edu.br', 'org.br', 'net.br',
                          'google.com', 'microsoft.com', 'amazon.com',
                          'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']:
            if not any(domain.endswith(tld) for tld in ['.br', '.com', '.org', '.net', '.io', '.co']):
                continue
            iocs.append((domain, 'domain'))
    
    # Deduplicate preserving order
    seen = set()
    unique_iocs = []
    for ioc, ioc_type in iocs:
        key = (ioc, ioc_type)
        if key not in seen:
            seen.add(key)
            unique_iocs.append(key)
    
    return unique_iocs


def check_ip_abuseipdb(ip: str) -> Optional[Dict]:
    """Consulta reputação do IP no AbuseIPDB."""
    if not ABUSEIPDB_API_KEY:
        return None
    
    url = f"{ABUSEIPDB_URL}/check"
    params = {
        'ipAddress': ip,
        'maxAgeInDays': 90,
    }
    headers = {
        'Key': ABUSEIPDB_API_KEY,
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[AbuseIPDB] Erro {response.status_code}: {response.text[:100]}")
            return None
    except Exception as e:
        print(f"[AbuseIPDB] Erro: {e}")
        return None


def check_ip_virustotal(ip: str) -> Optional[Dict]:
    """Consulta IP no VirusTotal."""
    if not VIRUSTOTAL_API_KEY:
        return None
    
    url = f"{VT_API_URL_V2}/ip-address/report"
    params = {
        'apikey': VIRUSTOTAL_API_KEY,
        'ip': ip
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get('response_code') == 1:
                return data
        return None
    except Exception as e:
        print(f"[VirusTotal] Erro: {e}")
        return None


def check_domain_virustotal(domain: str) -> Optional[Dict]:
    """Consulta domínio no VirusTotal."""
    if not VIRUSTOTAL_API_KEY:
        return None
    
    url = f"{VT_API_URL_V2}/domain/report"
    params = {
        'apikey': VIRUSTOTAL_API_KEY,
        'domain': domain
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get('response_code') == 1:
                return data
        return None
    except Exception as e:
        print(f"[VirusTotal] Erro: {e}")
        return None


def check_url_virustotal(url: str) -> Optional[Dict]:
    """Consulta URL no VirusTotal (relatório existente)."""
    if not VIRUSTOTAL_API_KEY:
        return None
    
    url_encoded = urllib.parse.quote(url, safe='')
    url_api = f"{VT_API_URL_V2}/url/report"
    params = {
        'apikey': VIRUSTOTAL_API_KEY,
        'resource': url
    }
    
    try:
        response = requests.get(url_api, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get('response_code') == 1:
                return data
        return None
    except Exception as e:
        print(f"[VirusTotal] Erro: {e}")
        return None


def scan_url_virustotal(url: str) -> Optional[Dict]:
    """Submete URL para scan no VirusTotal."""
    if not VIRUSTOTAL_API_KEY:
        return None
    
    url_api = f"{VT_API_URL_V2}/url/scan"
    data = {
        'apikey': VIRUSTOTAL_API_KEY,
        'url': url
    }
    
    try:
        response = requests.post(url_api, data=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            # Aguarda e consulta novamente
            time.sleep(3)
            return check_url_virustotal(url)
        return None
    except Exception as e:
        print(f"[VirusTotal Scan] Erro: {e}")
        return None


def calculate_risk(vt_positives: int, vt_total: int, abuse_score: int = 0) -> Tuple[int, str]:
    """Calcula risco baseado em detecções."""
    risk = 0
    
    # VirusTotal
    if vt_positives == 0:
        risk += 0
    elif vt_positives <= 2:
        risk += 20
    elif vt_positives <= 5:
        risk += 40
    else:
        risk += 70
    
    # AbuseIPDB
    if abuse_score > 0:
        if abuse_score <= 24:
            risk += 0
        elif abuse_score <= 49:
            risk += 20
        elif abuse_score <= 74:
            risk += 50
        else:
            risk += 80
    
    # Clamp
    risk = min(100, risk)
    
    # Veredito
    if risk < 20:
        veredito = "BAIXO"
    elif risk < 50:
        veredito = "MÉDIO"
    elif risk < 75:
        veredito = "ALTO"
    else:
        veredito = "CRÍTICO"
    
    return risk, veredito


def format_result(ioc: str, ioc_type: str, vt_data: Optional[Dict], 
                 abuse_data: Optional[Dict], verbose: bool = False) -> str:
    """Formata o resultado da análise."""
    
    # Extrair dados relevantes
    vt_positives = 0
    vt_total = 0
    vt_permalink = ""
    vt_detections = []
    
    if vt_data:
        vt_positives = vt_data.get('positives', 0)
        vt_total = vt_data.get('total', 0)
        vt_permalink = vt_data.get('permalink', '')
        
        if 'scans' in vt_data:
            for engine, result in vt_data['scans'].items():
                if result.get('detected'):
                    vt_detections.append(f"{engine}: {result.get('result', 'Malicious')}")
    
    abuse_score = 0
    abuse_last_report = ""
    abuse_total_reports = 0
    
    if abuse_data:
        abuse_score = abuse_data.get('abuseConfidenceScore', 0)
        abuse_last_report = abuse_data.get('lastReportedAt', '')[:10] if abuse_data.get('lastReportedAt') else 'N/A'
        abuse_total_reports = abuse_data.get('totalReports', 0)
    
    # Calcular risco
    risk, veredito = calculate_risk(vt_positives, vt_total, abuse_score)
    
    # Output
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"🛡️ ANÁLISE: {ioc}")
    lines.append(f"{'='*60}")
    lines.append(f"Tipo: {ioc_type.upper()}")
    lines.append(f"Risco: {risk}/100 - {veredito}")
    lines.append(f"")
    
    # VirusTotal
    lines.append("🔬 VIRUSTOTAL:")
    if vt_data:
        lines.append(f"   Detecções: {vt_positives}/{vt_total}")
        if vt_permalink:
            lines.append(f"   Link: {vt_permalink}")
        if vt_detections and verbose:
            lines.append("   Engines que detectaram:")
            for det in vt_detections[:10]:
                lines.append(f"     - {det}")
    else:
        lines.append("   Sem dados (API key não configurada ou rate limit)")
    
    # AbuseIPDB
    if ioc_type == 'ip' and abuse_data:
        lines.append("")
        lines.append("⚠️ ABUSEIPDB:")
        lines.append(f"   Score: {abuse_score}/100")
        lines.append(f"   Total Reports: {abuse_total_reports}")
        lines.append(f"   Último Report: {abuse_last_report}")
    
    # Recomendações
    lines.append("")
    lines.append("💡 RECOMENDAÇÃO:")
    if veredito == "BAIXO":
        lines.append("   - Seems seguro, continue monitorando")
    elif veredito == "MÉDIO":
        lines.append("   - Cuidado ao acessar")
        lines.append("   - Recomenda-se verificação adicional")
    elif veredito == "ALTO":
        lines.append("   - NÃO clique/accesse sem necessidade")
        lines.append("   - Considere bloquear em firewall/antivírus")
    else:
        lines.append("   - BLOQUEAR imediatamente")
        lines.append("   - Reportar como malware/phishing")
    
    return "\n".join(lines)


def scan_ioc(ioc: str, ioc_type: str, verbose: bool = False) -> str:
    """Executa scan de um IOC."""
    
    vt_data = None
    abuse_data = None
    
    if ioc_type == 'ip':
        print(f"[*] Consultando IP: {ioc}")
        vt_data = check_ip_virustotal(ioc)
        abuse_data = check_ip_abuseipdb(ioc)
    elif ioc_type == 'domain':
        print(f"[*] Consultando domínio: {ioc}")
        vt_data = check_domain_virustotal(ioc)
    elif ioc_type == 'url':
        print(f"[*] Consultando URL: {ioc}")
        vt_data = check_url_virustotal(ioc)
        if not vt_data:
            print(f"[*] Nenhum resultado, submetendo para scan...")
            vt_data = scan_url_virustotal(ioc)
    
    return format_result(ioc, ioc_type, vt_data, abuse_data, verbose)


def main():
    parser = argparse.ArgumentParser(description='Klaus IOC Scanner')
    parser.add_argument('ioc', nargs='?', help='IOC para scanear (URL, domínio ou IP)')
    parser.add_argument('ioc_extra', nargs='*', help='IOCs adicionais')
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo detalhado')
    parser.add_argument('--text', '-t', help='Texto contendo IOCs para extrair')
    
    args = parser.parse_args()
    
    # Verificar API keys
    if not VIRUSTOTAL_API_KEY and not ABUSEIPDB_API_KEY:
        print("⚠️ AVISO: Variables de ambiente não configuradas!")
        print("   Configure VIRUSTOTAL_API_KEY e ABUSEIPDB_API_KEY")
        print("")
    
    # Coletar IOCs
    iocs = []
    
    if args.text:
        iocs = extract_iocs(args.text)
    elif args.ioc:
        ioc_list = [args.ioc] + args.ioc_extra
        for ioc in ioc_list:
            # Detectar tipo
            if ioc.startswith(('http://', 'https://')):
                iocs.append((ioc, 'url'))
            elif re.match(r'^\d+\.\d+\.\d+\.\d+$', ioc):
                iocs.append((ioc, 'ip'))
            else:
                # Assume domínio
                iocs.append((ioc.lower(), 'domain'))
    else:
        print("用法:")
        print("  python3 ioc_scan.py <ioc>")
        print("  python3 ioc_scan.py --text 'texto com IOCs'")
        print("  python3 ioc_scan.py 1.2.3.4 exemplo.com")
        return
    
    # Executar scans
    print(f"\n🛡️ KLAUS IOC SCANNER")
    print(f"   IOCs encontrados: {len(iocs)}")
    
    if not iocs:
        print("❌ Nenhum IOC encontrado")
        return
    
    for ioc, ioc_type in iocs:
        result = scan_ioc(ioc, ioc_type, args.verbose)
        print(result)


if __name__ == '__main__':
    main()
