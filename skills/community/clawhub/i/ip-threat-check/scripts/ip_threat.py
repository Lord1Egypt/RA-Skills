#!/usr/bin/env python3
"""
IP Threat Check - Query IP threat intelligence from multiple sources
"""

import argparse
import json
import sys
import os
import urllib.request
import urllib.error

def get_ip_api_info(ip: str) -> dict:
    """Get IP info from ip-api.com (free, no API key needed)"""
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,region,regionName,city,isp,org,as,asname,query"
        
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'OpenClaw-IP-Threat-Check/1.0')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
        if data.get('status') == 'success':
            return {
                "success": True,
                "ip": data.get('query'),
                "country": data.get('country'),
                "country_code": data.get('countryCode'),
                "region": data.get('regionName'),
                "city": data.get('city'),
                "isp": data.get('isp'),
                "org": data.get('org'),
                "asn": data.get('as'),
                "asname": data.get('asname')
            }
        else:
            return {"success": False, "error": data.get('message', 'Unknown error')}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_abuseipdb_info(ip: str, api_key: str, days: int = 30) -> dict:
    """Get IP threat info from AbuseIPDB"""
    try:
        url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays={days}"
        
        req = urllib.request.Request(url)
        req.add_header('Key', api_key)
        req.add_header('Accept', 'application/json')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
        if data.get('data'):
            d = data['data']
            return {
                "success": True,
                "ip": d.get('ipAddress'),
                "abuse_score": d.get('abuseConfidenceScore', 0),
                "reports": d.get('totalReports', 0),
                "last_reported": d.get('lastReportedAt'),
                "country": d.get('countryCode'),
                "usage_type": d.get('usageType'),
                "isp": d.get('isp'),
                "domain": d.get('domain'),
                "risk": "high" if d.get('abuseConfidenceScore', 0) > 50 else "medium" if d.get('abuseConfidenceScore', 0) > 10 else "low"
            }
        else:
            return {"success": False, "error": "No data returned"}
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return {"success": False, "error": "Invalid API key"}
        elif e.code == 429:
            return {"success": False, "error": "Rate limit exceeded"}
        else:
            return {"success": False, "error": f"HTTP error: {e.code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_ip_info(ip: str) -> dict:
    """Get basic IP info (no API key needed)"""
    info = get_ip_api_info(ip)
    
    if info.get('success'):
        return {
            "success": True,
            "ip": ip,
            "geolocation": {
                "country": info.get('country'),
                "country_code": info.get('country_code'),
                "region": info.get('region'),
                "city": info.get('city')
            },
            "network": {
                "isp": info.get('isp'),
                "org": info.get('org'),
                "asn": info.get('asn'),
                "asname": info.get('asname')
            }
        }
    else:
        return info

def check_ip_threat(ip: str, sources: str = "all", days: int = 30) -> dict:
    """Check IP threat from multiple sources"""
    result = {
        "success": True,
        "ip": ip,
        "sources": {}
    }
    
    # Get basic info (always)
    basic_info = get_ip_api_info(ip)
    if basic_info.get('success'):
        result["geolocation"] = {
            "country": basic_info.get('country'),
            "country_code": basic_info.get('country_code'),
            "region": basic_info.get('region'),
            "city": basic_info.get('city')
        }
        result["network"] = {
            "isp": basic_info.get('isp'),
            "org": basic_info.get('org'),
            "asn": basic_info.get('asn')
        }
        result["sources"]["ip-api"] = {"status": "success"}
    else:
        result["sources"]["ip-api"] = {"status": "failed", "error": basic_info.get('error')}
    
    # Get AbuseIPDB info (if API key available)
    abuseipdb_key = os.environ.get('ABUSEIPDB_API_KEY')
    if abuseipdb_key and sources in ["all", "abuseipdb"]:
        abuse_info = get_abuseipdb_info(ip, abuseipdb_key, days)
        if abuse_info.get('success'):
            result["threat"] = {
                "score": abuse_info.get('abuse_score', 0),
                "reports": abuse_info.get('reports', 0),
                "last_reported": abuse_info.get('last_reported'),
                "risk": abuse_info.get('risk', 'unknown')
            }
            result["sources"]["abuseipdb"] = {"status": "success"}
        else:
            result["sources"]["abuseipdb"] = {"status": "failed", "error": abuse_info.get('error')}
    else:
        if sources in ["all", "abuseipdb"]:
            result["sources"]["abuseipdb"] = {"status": "skipped", "reason": "API key not configured"}
    
    # Determine overall risk
    if "threat" in result:
        result["overall_risk"] = result["threat"]["risk"]
    else:
        result["overall_risk"] = "unknown"
    
    return result

def bulk_check(file_path: str, sources: str = "all", days: int = 30) -> dict:
    """Check multiple IPs from file"""
    try:
        with open(file_path, 'r') as f:
            ips = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return {"success": False, "error": f"File not found: {file_path}"}
    
    results = []
    for ip in ips:
        result = check_ip_threat(ip, sources, days)
        results.append(result)
    
    return {
        "success": True,
        "total": len(ips),
        "results": results
    }

def main():
    parser = argparse.ArgumentParser(
        description='IP Threat Check - Query IP threat intelligence'
    )
    parser.add_argument(
        'action',
        choices=['info', 'check', 'bulk'],
        help='Action to perform'
    )
    parser.add_argument(
        '--ip', '-i',
        help='IP address to check'
    )
    parser.add_argument(
        '--file', '-f',
        help='File with IPs (one per line)'
    )
    parser.add_argument(
        '--source', '-s',
        default='all',
        choices=['all', 'ipapi', 'abuseipdb'],
        help='Data source (default: all)'
    )
    parser.add_argument(
        '--days', '-d',
        type=int,
        default=30,
        help='Days of history to check (default: 30)'
    )

    args = parser.parse_args()

    # Execute action
    if args.action == 'info':
        if not args.ip:
            result = {"success": False, "error": "Missing --ip parameter"}
        else:
            result = get_ip_info(args.ip)
    elif args.action == 'check':
        if not args.ip:
            result = {"success": False, "error": "Missing --ip parameter"}
        else:
            result = check_ip_threat(args.ip, args.source, args.days)
    elif args.action == 'bulk':
        if not args.file:
            result = {"success": False, "error": "Missing --file parameter"}
        else:
            result = bulk_check(args.file, args.source, args.days)
    else:
        result = {"success": False, "error": f"Unknown action: {args.action}"}

    # Output result
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result.get('success') else 1)

if __name__ == '__main__':
    main()
