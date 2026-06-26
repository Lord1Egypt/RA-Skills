#!/usr/bin/env python3
"""
Nex Domains - DNS & Domain Portfolio Manager
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
https://nex-ai.be
"""
import sys
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from config import DATA_DIR, DOMAIN_EXPIRY_WARNING_DAYS, SSL_EXPIRY_WARNING_DAYS, CF_API_TOKEN
from storage import (
    init_db, save_domain, get_domain, list_domains, update_domain, delete_domain,
    save_dns_records, get_dns_records, get_expiring_domains, get_expiring_ssl,
    get_domain_stats, search_domains, export_domains, save_check_result, get_check_history
)
from checkers import (
    check_whois, check_dns, check_ssl, check_http,
    scan_domain, bulk_scan, query_cloudflare_zones, query_cloudflare_dns,
    sync_domain_from_cloudflare
)

FOOTER = "[Nex Domains by Nex AI | nex-ai.be]"


def format_domain_info(domain_dict: dict) -> str:
    """Format domain information for display."""
    output = []
    output.append(f"\nDomain: {domain_dict['domain']}")
    output.append(f"Registrar: {domain_dict.get('registrar', 'N/A')}")
    output.append(f"Status: {domain_dict.get('status', 'N/A')}")

    if domain_dict.get('client'):
        output.append(f"Client: {domain_dict['client']}")

    if domain_dict.get('expiry_date'):
        output.append(f"Expiry: {domain_dict['expiry_date']}")

    if domain_dict.get('auto_renew'):
        output.append(f"Auto-Renew: Yes")

    if domain_dict.get('ssl_expiry'):
        output.append(f"SSL Expiry: {domain_dict['ssl_expiry']}")

    if domain_dict.get('dns_provider'):
        output.append(f"DNS Provider: {domain_dict['dns_provider']}")

    if domain_dict.get('hosting_provider'):
        output.append(f"Hosting Provider: {domain_dict['hosting_provider']}")

    if domain_dict.get('monthly_cost'):
        output.append(f"Monthly Cost: €{domain_dict['monthly_cost']:.2f}")

    if domain_dict.get('notes'):
        output.append(f"Notes: {domain_dict['notes']}")

    output.append(f"Last Checked: {domain_dict.get('last_checked', 'Never')}")
    output.append(f"Created: {domain_dict.get('created_at', 'N/A')}")

    return "\n".join(output)


def cmd_add(args):
    """Add a domain."""
    domain_id = save_domain(
        domain=args.domain,
        registrar=args.registrar,
        client=args.client,
        auto_renew=args.auto_renew,
        monthly_cost=args.monthly_cost,
        status="active",
        notes=args.notes
    )
    print(f"Added domain: {args.domain} (ID: {domain_id})")
    print(FOOTER)


def cmd_scan(args):
    """Scan domain(s) for health/info."""
    domains = args.domains if isinstance(args.domains, list) else [args.domains]

    for domain_name in domains:
        domain_obj = get_domain(domain_name)

        # Scan the domain
        scan_result = scan_domain(domain_name)

        # Save results to database
        if domain_obj:
            domain_id = domain_obj['id']

            # Update domain with scan results
            updates = {}

            whois = scan_result['checks'].get('whois', {})
            if whois.get('expiry_date'):
                updates['expiry_date'] = whois['expiry_date']
            if whois.get('registrar'):
                updates['registrar'] = whois['registrar']
            if whois.get('nameservers'):
                updates['nameservers'] = json.dumps(whois['nameservers'])

            ssl_info = scan_result['checks'].get('ssl', {})
            if ssl_info.get('expiry_date'):
                updates['ssl_expiry'] = ssl_info['expiry_date']
            if ssl_info.get('issuer'):
                updates['ssl_issuer'] = ssl_info['issuer']

            updates['last_checked'] = datetime.utcnow().isoformat()

            if updates:
                update_domain(domain_id, **updates)

            # Save check results
            for check_type, check_data in scan_result['checks'].items():
                status = check_data.get('status', 'unknown')
                details = {k: v for k, v in check_data.items() if k != 'status'}
                save_check_result(domain_id, check_type, status, details)

        # Display results
        print(f"\nScanning: {domain_name}")
        print("---")
        print(f"Scanned at: {scan_result['scanned_at']}")

        for check_type, check_result in scan_result['checks'].items():
            status = check_result.get('status', 'unknown')
            print(f"{check_type.upper()}: {status}")

    print(FOOTER)


def cmd_list(args):
    """List domains."""
    domains = list_domains(
        registrar=args.registrar,
        client=args.client,
        expiring_within=args.expiring_within,
        status=args.status
    )

    if not domains:
        print("No domains found.")
        print(FOOTER)
        return

    print(f"\nFound {len(domains)} domain(s):")
    print("---")

    for domain in domains:
        print(f"{domain['domain']:<30} {domain['registrar']:<15} {domain['status']:<12}")
        if domain.get('client'):
            print(f"  Client: {domain['client']}")
        if domain.get('expiry_date'):
            print(f"  Expires: {domain['expiry_date']}")

    print(FOOTER)


def cmd_show(args):
    """Show detailed domain information."""
    domain_obj = get_domain(args.domain)

    if not domain_obj:
        print(f"Domain not found: {args.domain}")
        print(FOOTER)
        return

    print(format_domain_info(domain_obj))

    # Show DNS records
    dns_records = get_dns_records(domain_obj['id'])
    if dns_records:
        print("\nDNS Records:")
        print("---")
        for record in dns_records:
            print(f"{record['record_type']:<10} {record['name']:<30} {record['content'][:50]}")

    # Show check history
    checks = get_check_history(domain_obj['id'], limit=5)
    if checks:
        print("\nRecent Checks:")
        print("---")
        for check in checks:
            print(f"{check['check_type']:<15} {check['status']:<10} {check['checked_at']}")

    print(FOOTER)


def cmd_dns(args):
    """Show DNS records."""
    domain_obj = get_domain(args.domain)

    if not domain_obj:
        print(f"Domain not found: {args.domain}")
        print(FOOTER)
        return

    records = get_dns_records(domain_obj['id'], record_type=args.type)

    if not records:
        print(f"No {args.type if args.type else 'DNS'} records found for {args.domain}")
        print(FOOTER)
        return

    print(f"\nDNS Records for {args.domain}:")
    print("---")

    for record in records:
        print(f"Type:     {record['record_type']}")
        print(f"Name:     {record['name']}")
        print(f"Content:  {record['content']}")
        if record['ttl']:
            print(f"TTL:      {record['ttl']}")
        if record['priority']:
            print(f"Priority: {record['priority']}")
        print()

    print(FOOTER)


def cmd_ssl(args):
    """Show SSL certificate information."""
    ssl_result = check_ssl(args.domain)

    print(f"\nSSL Certificate for {args.domain}:")
    print("---")

    if ssl_result.get('status') != 'success':
        print(f"Error: {ssl_result.get('message', 'Unknown error')}")
    else:
        if ssl_result.get('subject'):
            print(f"Subject: {ssl_result['subject']}")
        if ssl_result.get('issuer'):
            print(f"Issuer: {ssl_result['issuer']}")
        if ssl_result.get('expiry_date'):
            print(f"Expiry: {ssl_result['expiry_date']}")
        if ssl_result.get('not_before'):
            print(f"Valid From: {ssl_result['not_before']}")

    print(FOOTER)


def cmd_whois(args):
    """Show WHOIS information."""
    whois_result = check_whois(args.domain)

    print(f"\nWHOIS Information for {args.domain}:")
    print("---")

    if whois_result.get('status') != 'success':
        print(f"Error: {whois_result.get('message', 'Unknown error')}")
    else:
        if whois_result.get('registrar'):
            print(f"Registrar: {whois_result['registrar']}")
        if whois_result.get('expiry_date'):
            print(f"Expiry Date: {whois_result['expiry_date']}")
        if whois_result.get('nameservers'):
            print(f"Nameservers:")
            for ns in whois_result['nameservers']:
                print(f"  - {ns}")

    print(FOOTER)


def cmd_expiring(args):
    """Show expiring domains and SSL certs."""
    days = args.days

    print(f"\nDomains expiring within {days} days:")
    print("---")

    expiring_domains = get_expiring_domains(days)
    if expiring_domains:
        for domain in expiring_domains:
            print(f"{domain['domain']:<30} Expires: {domain['expiry_date']}")
    else:
        print("No domains expiring soon.")

    print(f"\nSSL certificates expiring within {days} days:")
    print("---")

    expiring_ssl = get_expiring_ssl(days)
    if expiring_ssl:
        for domain in expiring_ssl:
            print(f"{domain['domain']:<30} SSL Expires: {domain['ssl_expiry']}")
    else:
        print("No SSL certificates expiring soon.")

    print(FOOTER)


def cmd_sync(args):
    """Sync domains from Cloudflare."""
    if not CF_API_TOKEN:
        print("Error: CF_API_TOKEN environment variable not set")
        print(FOOTER)
        return

    print("Syncing domains from Cloudflare...")
    print("---")

    zones = query_cloudflare_zones(CF_API_TOKEN)

    if not zones:
        print("No zones found or API error.")
        print(FOOTER)
        return

    for zone in zones:
        domain_name = zone.get('name')
        print(f"Processing: {domain_name}")

        # Check if domain exists
        domain_obj = get_domain(domain_name)

        if domain_obj:
            domain_id = domain_obj['id']
        else:
            # Add new domain
            domain_id = save_domain(
                domain=domain_name,
                registrar="cloudflare",
                status="active"
            )

        # Sync DNS records
        records = query_cloudflare_dns(CF_API_TOKEN, zone.get('id'))
        if records:
            dns_data = [
                {
                    'type': r.get('type'),
                    'name': r.get('name'),
                    'content': r.get('content'),
                    'ttl': r.get('ttl'),
                    'proxied': r.get('proxied', False),
                    'priority': r.get('priority'),
                }
                for r in records
            ]
            save_dns_records(domain_id, dns_data)

        # Update domain info
        update_domain(
            domain_id,
            dns_provider="cloudflare",
            nameservers=json.dumps(zone.get('nameservers', [])),
            last_checked=datetime.utcnow().isoformat()
        )

        print(f"  ✓ Synced {len(records)} DNS records")

    print(FOOTER)


def cmd_search(args):
    """Search domains."""
    results = search_domains(args.query)

    if not results:
        print(f"No domains found matching: {args.query}")
        print(FOOTER)
        return

    print(f"\nFound {len(results)} domain(s) matching '{args.query}':")
    print("---")

    for domain in results:
        print(f"{domain['domain']:<30} {domain['registrar']:<15} {domain['status']:<12}")

    print(FOOTER)


def cmd_remove(args):
    """Remove a domain."""
    domain_obj = get_domain(args.domain)

    if not domain_obj:
        print(f"Domain not found: {args.domain}")
        print(FOOTER)
        return

    delete_domain(domain_obj['id'])
    print(f"Removed domain: {args.domain}")
    print(FOOTER)


def cmd_export(args):
    """Export domains."""
    data = export_domains(format=args.format)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(data)
        print(f"Exported {args.format.upper()} to: {args.output}")
    else:
        print(data)

    print(FOOTER)


def cmd_stats(args):
    """Show portfolio statistics."""
    stats = get_domain_stats()

    print("\nDomain Portfolio Statistics:")
    print("---")
    print(f"Total Domains: {stats['total_domains']}")

    print("\nBy Registrar:")
    for registrar, count in stats['by_registrar'].items():
        print(f"  {registrar}: {count}")

    print("\nBy Status:")
    for status, count in stats['by_status'].items():
        print(f"  {status}: {count}")

    if stats['by_client']:
        print("\nBy Client:")
        for client, count in stats['by_client'].items():
            print(f"  {client}: {count}")

    print(f"\nTotal Monthly Cost: €{stats['total_monthly_cost']:.2f}")
    print(f"Expiring within 90 days: {stats['expiring_soon_90d']}")

    print(FOOTER)


def cmd_check(args):
    """Quick health check on a domain."""
    domain_obj = get_domain(args.domain)

    if not domain_obj:
        print(f"Adding domain: {args.domain}")
        domain_obj = {'id': save_domain(args.domain, registrar="other", status="active")}

    domain_id = domain_obj['id']

    print(f"\nQuick check: {args.domain}")
    print("---")

    # HTTP check
    http_result = check_http(args.domain)
    print(f"Resolves: {'Yes' if http_result.get('resolves') else 'No'}")
    if http_result.get('resolved_ip'):
        print(f"IP Address: {http_result['resolved_ip']}")
    print(f"HTTPS: {http_result.get('https_status', 'N/A')}")
    print(f"HTTP: {http_result.get('http_status', 'N/A')}")

    # Save check result
    save_check_result(domain_id, 'http', 'success', http_result)

    print(FOOTER)


def main():
    """Main entry point."""
    # Initialize database on first run
    if not DATA_DIR.exists():
        init_db()

    parser = argparse.ArgumentParser(
        description="Nex Domains - DNS & Domain Portfolio Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Built by Nex AI (https://nex-ai.be)"
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a domain')
    add_parser.add_argument('domain', help='Domain name')
    add_parser.add_argument('--registrar', required=True, help='Registrar')
    add_parser.add_argument('--client', help='Client name')
    add_parser.add_argument('--auto-renew', action='store_true', help='Enable auto-renewal')
    add_parser.add_argument('--monthly-cost', type=float, help='Monthly cost')
    add_parser.add_argument('--notes', help='Additional notes')
    add_parser.set_defaults(func=cmd_add)

    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan domain(s)')
    scan_parser.add_argument('domains', nargs='+', help='Domain(s) to scan')
    scan_parser.set_defaults(func=cmd_scan)

    # List command
    list_parser = subparsers.add_parser('list', help='List domains')
    list_parser.add_argument('--registrar', help='Filter by registrar')
    list_parser.add_argument('--client', help='Filter by client')
    list_parser.add_argument('--expiring-within', type=int, help='Expiring within N days')
    list_parser.add_argument('--status', help='Filter by status')
    list_parser.set_defaults(func=cmd_list)

    # Show command
    show_parser = subparsers.add_parser('show', help='Show domain details')
    show_parser.add_argument('domain', help='Domain name')
    show_parser.set_defaults(func=cmd_show)

    # DNS command
    dns_parser = subparsers.add_parser('dns', help='Show DNS records')
    dns_parser.add_argument('domain', help='Domain name')
    dns_parser.add_argument('--type', help='Record type')
    dns_parser.set_defaults(func=cmd_dns)

    # SSL command
    ssl_parser = subparsers.add_parser('ssl', help='Show SSL info')
    ssl_parser.add_argument('domain', help='Domain name')
    ssl_parser.set_defaults(func=cmd_ssl)

    # WHOIS command
    whois_parser = subparsers.add_parser('whois', help='Show WHOIS info')
    whois_parser.add_argument('domain', help='Domain name')
    whois_parser.set_defaults(func=cmd_whois)

    # Expiring command
    expiring_parser = subparsers.add_parser('expiring', help='Show expiring domains/SSL')
    expiring_parser.add_argument('--days', type=int, default=90, help='Days threshold')
    expiring_parser.set_defaults(func=cmd_expiring)

    # Sync command
    sync_parser = subparsers.add_parser('sync', help='Sync from Cloudflare')
    sync_parser.set_defaults(func=cmd_sync)

    # Search command
    search_parser = subparsers.add_parser('search', help='Search domains')
    search_parser.add_argument('query', help='Search query')
    search_parser.set_defaults(func=cmd_search)

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove domain')
    remove_parser.add_argument('domain', help='Domain name')
    remove_parser.set_defaults(func=cmd_remove)

    # Export command
    export_parser = subparsers.add_parser('export', help='Export domains')
    export_parser.add_argument('format', choices=['csv', 'json'], help='Export format')
    export_parser.add_argument('--output', help='Output file path')
    export_parser.set_defaults(func=cmd_export)

    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show statistics')
    stats_parser.set_defaults(func=cmd_stats)

    # Check command
    check_parser = subparsers.add_parser('check', help='Quick health check')
    check_parser.add_argument('domain', help='Domain name')
    check_parser.set_defaults(func=cmd_check)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {str(e)}")
        print(FOOTER)
        sys.exit(1)


if __name__ == '__main__':
    main()
