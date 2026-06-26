"""
Nex Domains - Domain Checkers
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
Domain validation and scanning functions
"""
import subprocess
import json
import logging
import ssl
import socket
import urllib.request
import urllib.error
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path
import re

from config import (
    WHOIS_COMMAND, DIG_COMMAND, OPENSSL_COMMAND,
    DEFAULT_NAMESERVERS, API_TIMEOUT, WHOIS_TIMEOUT,
    SSL_CHECK_TIMEOUT, CF_API_TOKEN, CF_EMAIL
)

logger = logging.getLogger(__name__)


def run_command(cmd: List[str], timeout: int = 10) -> Optional[str]:
    """Run a shell command safely and return output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        logger.warning(f"Command timeout: {cmd[0]}")
        return None
    except Exception as e:
        logger.error(f"Command failed: {str(e)}")
        return None


def check_whois(domain: str) -> Dict[str, Any]:
    """Check WHOIS information for a domain."""
    try:
        output = run_command([WHOIS_COMMAND, domain], timeout=WHOIS_TIMEOUT)
        if not output:
            return {'status': 'error', 'message': 'WHOIS command failed'}

        result = {
            'status': 'success',
            'domain': domain,
            'expiry_date': None,
            'registrar': None,
            'nameservers': [],
        }

        # Parse common WHOIS formats
        lines = output.lower()

        # Extract expiry date (multiple formats)
        expiry_patterns = [
            r'registrar expiration date:\s*(\d{4}-\d{2}-\d{2})',
            r'expiry date:\s*(\d{4}-\d{2}-\d{2})',
            r'expiration date:\s*([a-z]+\s+\d{1,2},?\s+\d{4})',
            r'expire date:\s*(\d{4}-\d{2}-\d{2})',
            r'paid-till:\s*(\d{4}-\d{2}-\d{2})',
        ]

        for pattern in expiry_patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                result['expiry_date'] = match.group(1)
                break

        # Extract registrar
        registrar_patterns = [
            r'registrar:\s*(.+)',
            r'registrar name:\s*(.+)',
        ]

        for pattern in registrar_patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                result['registrar'] = match.group(1).strip()
                break

        # Extract nameservers
        ns_lines = re.findall(r'name\s*server:?\s*([a-z0-9\.\-]+)', output, re.IGNORECASE)
        result['nameservers'] = list(set(ns_lines))

        return result

    except Exception as e:
        logger.error(f"WHOIS check failed for {domain}: {str(e)}")
        return {'status': 'error', 'message': str(e)}


def check_dns(domain: str, record_type: str = "A", nameserver: str = None) -> List[Dict]:
    """Query DNS records for a domain."""
    try:
        cmd = [DIG_COMMAND, f"@{nameserver or '8.8.8.8'}", domain, record_type, "+short"]
        output = run_command(cmd, timeout=API_TIMEOUT)

        if not output:
            return []

        records = []
        for line in output.strip().split('\n'):
            if line.strip():
                records.append({
                    'type': record_type,
                    'name': domain,
                    'content': line.strip(),
                })

        logger.info(f"DNS {record_type} records for {domain}: {len(records)}")
        return records

    except Exception as e:
        logger.error(f"DNS check failed for {domain}: {str(e)}")
        return []


def check_ssl(domain: str, port: int = 443) -> Dict[str, Any]:
    """Check SSL certificate information."""
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with socket.create_connection((domain, port), timeout=SSL_CHECK_TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()

                if not cert:
                    return {'status': 'error', 'message': 'No certificate found'}

                # Parse expiry date
                expiry_str = cert.get('notAfter', '')
                try:
                    expiry_date = datetime.strptime(expiry_str, '%b %d %H:%M:%S %Y %Z')
                except:
                    expiry_date = None

                # Extract issuer
                issuer = ''
                for part in cert.get('issuer', []):
                    for key, value in part:
                        if key == 'organizationName':
                            issuer = value
                            break

                # Extract subject
                subject = ''
                for part in cert.get('subject', []):
                    for key, value in part:
                        if key == 'commonName':
                            subject = value
                            break

                return {
                    'status': 'success',
                    'domain': domain,
                    'subject': subject,
                    'issuer': issuer,
                    'expiry_date': expiry_date.isoformat() if expiry_date else None,
                    'not_before': cert.get('notBefore'),
                    'not_after': cert.get('notAfter'),
                }

    except ssl.SSLError as e:
        return {'status': 'error', 'message': f'SSL error: {str(e)}'}
    except socket.timeout:
        return {'status': 'error', 'message': 'SSL check timeout'}
    except Exception as e:
        logger.error(f"SSL check failed for {domain}: {str(e)}")
        return {'status': 'error', 'message': str(e)}


def check_http(domain: str) -> Dict[str, Any]:
    """Check if domain resolves and HTTP/HTTPS works."""
    result = {
        'domain': domain,
        'http_status': None,
        'https_status': None,
        'resolves': False,
    }

    # Check DNS resolution
    try:
        ip = socket.gethostbyname(domain)
        result['resolves'] = True
        result['resolved_ip'] = ip
    except socket.gaierror:
        logger.warning(f"Domain does not resolve: {domain}")
        return result
    except Exception as e:
        logger.error(f"DNS resolution failed for {domain}: {str(e)}")
        return result

    # Check HTTPS
    try:
        req = urllib.request.Request(f'https://{domain}', method='HEAD')
        with urllib.request.urlopen(req, timeout=API_TIMEOUT) as response:
            result['https_status'] = response.status
    except urllib.error.HTTPError as e:
        result['https_status'] = e.code
    except Exception:
        result['https_status'] = None

    # Check HTTP
    try:
        req = urllib.request.Request(f'http://{domain}', method='HEAD')
        with urllib.request.urlopen(req, timeout=API_TIMEOUT) as response:
            result['http_status'] = response.status
    except urllib.error.HTTPError as e:
        result['http_status'] = e.code
    except Exception:
        result['http_status'] = None

    return result


def query_cloudflare_zones(api_token: str) -> List[Dict]:
    """List all Cloudflare zones (domains)."""
    if not api_token:
        logger.warning("Cloudflare API token not configured")
        return []

    try:
        req = urllib.request.Request(
            'https://api.cloudflare.com/client/v4/zones?per_page=100',
            headers={
                'Authorization': f'Bearer {api_token}',
                'Content-Type': 'application/json',
            }
        )

        with urllib.request.urlopen(req, timeout=API_TIMEOUT) as response:
            data = json.loads(response.read().decode())

            if data.get('success'):
                zones = data.get('result', [])
                logger.info(f"Retrieved {len(zones)} Cloudflare zones")
                return zones

            logger.error(f"Cloudflare API error: {data.get('errors')}")
            return []

    except Exception as e:
        logger.error(f"Cloudflare zones query failed: {str(e)}")
        return []


def query_cloudflare_dns(api_token: str, zone_id: str) -> List[Dict]:
    """Get DNS records for a Cloudflare zone."""
    if not api_token:
        logger.warning("Cloudflare API token not configured")
        return []

    try:
        req = urllib.request.Request(
            f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?per_page=100',
            headers={
                'Authorization': f'Bearer {api_token}',
                'Content-Type': 'application/json',
            }
        )

        with urllib.request.urlopen(req, timeout=API_TIMEOUT) as response:
            data = json.loads(response.read().decode())

            if data.get('success'):
                records = data.get('result', [])
                logger.info(f"Retrieved {len(records)} DNS records from Cloudflare")
                return records

            logger.error(f"Cloudflare DNS query error: {data.get('errors')}")
            return []

    except Exception as e:
        logger.error(f"Cloudflare DNS query failed: {str(e)}")
        return []


def sync_domain_from_cloudflare(api_token: str, domain: str) -> Dict[str, Any]:
    """Sync domain information from Cloudflare."""
    try:
        # Get zone ID for the domain
        zones = query_cloudflare_zones(api_token)
        zone = None

        for z in zones:
            if z.get('name') == domain or z.get('name').endswith('.' + domain):
                zone = z
                break

        if not zone:
            return {'status': 'error', 'message': f'Domain not found in Cloudflare'}

        result = {
            'status': 'success',
            'domain': domain,
            'zone_id': zone.get('id'),
            'zone_name': zone.get('name'),
            'dns_provider': 'cloudflare',
            'nameservers': zone.get('nameservers', []),
            'dns_records': [],
        }

        # Get DNS records
        records = query_cloudflare_dns(api_token, zone.get('id'))
        result['dns_records'] = records

        return result

    except Exception as e:
        logger.error(f"Cloudflare sync failed for {domain}: {str(e)}")
        return {'status': 'error', 'message': str(e)}


def scan_domain(domain: str) -> Dict[str, Any]:
    """Run comprehensive scan on a domain."""
    logger.info(f"Scanning domain: {domain}")

    result = {
        'domain': domain,
        'scanned_at': datetime.utcnow().isoformat(),
        'checks': {},
    }

    # WHOIS check
    whois_result = check_whois(domain)
    result['checks']['whois'] = whois_result

    # DNS check
    dns_result = check_dns(domain, "A")
    result['checks']['dns_a'] = dns_result

    # SSL check
    ssl_result = check_ssl(domain)
    result['checks']['ssl'] = ssl_result

    # HTTP check
    http_result = check_http(domain)
    result['checks']['http'] = http_result

    logger.info(f"Domain scan complete: {domain}")
    return result


def bulk_scan(domains: List[str]) -> List[Dict]:
    """Scan multiple domains."""
    results = []
    for domain in domains:
        result = scan_domain(domain)
        results.append(result)
    return results
