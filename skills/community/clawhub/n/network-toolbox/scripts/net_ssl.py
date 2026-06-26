#!/usr/bin/env python3
"""SSL/TLS certificate inspection."""

import argparse, json, ssl, socket, sys, datetime

def get_cert(host, port=443, timeout=10):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        ssock = ctx.wrap_socket(sock, server_hostname=host)
        cert = ssock.getpeercert()
        ssock.close()
        return cert
    except Exception as e:
        return {"error": str(e)}

def format_cert(cert, verbose=False):
    if 'error' in cert:
        return f"ERROR: {cert['error']}"

    lines = []
    lines.append("SSL Certificate:")
    lines.append(f"  Subject:      {dict(cert.get('subject', []))}")
    lines.append(f"  Issuer:       {dict(cert.get('issuer', []))}")

    # Validity
    not_before = cert.get('notBefore', '')
    not_after = cert.get('notAfter', '')
    lines.append(f"  Valid From:   {not_before}")
    lines.append(f"  Valid Until:  {not_after}")

    if not_after:
        try:
            expiry = datetime.datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
            remaining = (expiry - datetime.datetime.now()).days
            if remaining < 0:
                lines.append(f"  Status:       EXPIRED ({-remaining} days ago)")
            elif remaining < 30:
                lines.append(f"  Status:       EXPIRING SOON ({remaining} days)")
            else:
                lines.append(f"  Status:       VALID ({remaining} days remaining)")
        except:
            pass

    # SAN
    san = cert.get('subjectAltName', [])
    if san:
        lines.append(f"  SAN ({len(san)}):")
        for typ, val in san[:10]:
            lines.append(f"    {typ}: {val}")
        if len(san) > 10:
            lines.append(f"    ... {len(san) - 10} more")

    # Serial, version, algorithms
    lines.append(f"  Serial:       {cert.get('serialNumber', 'N/A')}")
    lines.append(f"  Version:      {cert.get('version', 'N/A')}")

    if verbose:
        lines.append(f"\n  Full cert dict:")
        lines.append(json.dumps(cert, indent=4))

    return '\n'.join(lines)

def main():
    p = argparse.ArgumentParser(description='SSL certificate inspection')
    p.add_argument('url', help='URL or hostname (e.g., https://example.com or example.com)')
    p.add_argument('--port', type=int, default=443, help='Port (default: 443)')
    p.add_argument('--verbose', action='store_true', help='Show full certificate details')
    p.add_argument('--json', action='store_true', help='JSON output')
    args = p.parse_args()

    host = args.url.replace('https://', '').replace('http://', '').split('/')[0].split(':')[0]
    cert = get_cert(host, args.port)

    if args.json:
        print(json.dumps(cert, indent=2, default=str))
    else:
        print(format_cert(cert, args.verbose))

if __name__ == '__main__':
    main()
