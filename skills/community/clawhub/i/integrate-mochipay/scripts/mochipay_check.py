#!/usr/bin/env python3
"""Read-only offline catalog/config checks. Never calls a payment API."""
import argparse
import json
import sys
import ipaddress
from pathlib import Path
from urllib.parse import urlsplit

METHODS = {'USDT_TRC20', 'USDC_ERC20', 'BTC_BITCOIN', 'ETH_ERC20', 'SOL_SOLANA','TRX_TRON'}
LIMIT = 'Offline declared-configuration check only; credentials, wallet ownership, live API, core/PHP compatibility and payments are unverified.'

def https_url(value, base=False):
    if not isinstance(value, str) or not value or any(c.isspace() for c in value):
        return False
    try:
        u = urlsplit(value)
        if u.scheme != 'https' or not u.hostname or u.username is not None or u.password is not None or u.fragment:
            return False
        if u.port not in (None, 443):
            return False
        return not base or (u.path in ('', '/') and not u.query)
    except ValueError:
        return False

def audit(config):
    if not isinstance(config, dict):
        return ['Configuration must be a JSON object.']
    issues = []
    allowed = {'integration','base_url','payment_mode','unique_amount_direction','payment_methods','active_wallet_methods','api_key_configured','api_secret_configured','subscription_active','notify_url','redirect_url','backend_language','request_id_supported','retry_uses_saved_payload','api_credentials_in_app','verified_callback_enabled','atomic_order_update_enabled'}
    if set(config) - allowed:
        issues.append('Unexpected fields: use only the sanitized example schema; never supply credentials or private configuration.')
    integration = config.get('integration')
    if integration not in ('plugin', 'custom', 'mobile', 'classic_saas', 'payment_link'):
        issues.append('integration must be plugin, custom, mobile, classic_saas or payment_link.')
    if not https_url(config.get('base_url'), True):
        issues.append('base_url must be an HTTPS origin without /api, credentials, query or fragment.')
    elif config.get('base_url').rstrip('/') != 'https://mochi.bz':
        issues.append('Non-default base URL: verify the authorized deployment before configuring credentials.')
    mode = config.get('payment_mode')
    if mode not in ('ON_SITE', 'HPP'):
        issues.append('payment_mode must be ON_SITE or HPP.')
    if integration in ('classic_saas', 'payment_link') and mode != 'HPP':
        issues.append('Classic SaaS and payment links support HPP only.')
    if config.get('unique_amount_direction') not in ('UP', 'DOWN'):
        issues.append('unique_amount_direction must be UP or DOWN.')
    chosen = config.get('payment_methods')
    wallets = config.get('active_wallet_methods')
    valid_chosen = isinstance(chosen, list) and bool(chosen) and all(isinstance(x,str) and x in METHODS for x in chosen)
    valid_wallets = isinstance(wallets, list) and all(isinstance(x,str) and x in METHODS for x in wallets)
    if not valid_chosen:
        issues.append('Select at least one recognized payment method.')
    if not valid_wallets:
        issues.append('active_wallet_methods must be a list of recognized method codes.')
    if valid_chosen and valid_wallets and not set(chosen).issubset(set(wallets)):
        issues.append('Every enabled method needs a declared active receiving wallet.')
    if config.get('subscription_active') is not True:
        issues.append('Confirm an active subscription.')
    if integration != 'payment_link':
        for flag in ('api_key_configured','api_secret_configured'):
            if config.get(flag) is not True:
                issues.append('Confirm '+flag+' privately; do not supply credentials.')
    if integration in ('custom','plugin','mobile'):
        for field in ('notify_url','redirect_url'):
            value = config.get(field)
            if value in (None, ''):
                continue  # Optional API fields; integration verification is still required.
            if not https_url(value):
                issues.append(field+' must be public HTTPS; live reachability is not checked.')
            else:
                host = urlsplit(value).hostname
                blocked = host in ('example.com','example.org','localhost') or host.endswith(('.localhost','.local')) or '.' not in host
                try:
                    blocked = blocked or not ipaddress.ip_address(host).is_global
                except ValueError:
                    pass
                if blocked:
                    issues.append(field+' is a placeholder/local/private endpoint.')
    if config.get('backend_language') is not None and config['backend_language'] not in ('php','nodejs','python','dotnet','java'):
        issues.append('Choose php, nodejs, python, dotnet or java for the implemented backend demo.')
    for field in ('request_id_supported','retry_uses_saved_payload','verified_callback_enabled','atomic_order_update_enabled'):
        if field in config and config[field] is not True:
            issues.append('Confirm '+field+'; an offline declaration is not live verification.')
    if integration == 'mobile' and config.get('api_credentials_in_app') is not False:
        issues.append('Mobile apps must declare api_credentials_in_app:false; API key/secret belong on the merchant backend.')
    return issues

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    catalog = commands.add_parser('catalog', help='List pinned packages and exact core rows.')
    catalog.add_argument('--package')
    examples = commands.add_parser('examples', help='List backend/mobile demos and pinned runtime requirements.')
    examples.add_argument('--language', choices=['php','nodejs','python','dotnet','java','ios','android'])
    check = commands.add_parser('audit', help='Audit sanitized config; no network or secrets.')
    check.add_argument('config', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'examples':
            data = json.loads((Path(__file__).resolve().parent.parent/'references/developer-examples.json').read_text(encoding='utf-8'))
            if args.language: data['resources'] = [r for r in data['resources'] if r['id'] == args.language]
            data['limitation'] = LIMIT
            print(json.dumps(data, indent=2, ensure_ascii=False)); return 0
        if args.command == 'catalog':
            data = json.loads((Path(__file__).resolve().parent.parent/'references/catalog.json').read_text(encoding='utf-8'))
            if args.package:
                data['packages'] = [p for p in data['packages'] if p['id'] == args.package]
                if not data['packages']:
                    print(json.dumps({'error':'Unknown package ID. Run catalog for available IDs.'}))
                    return 2
            data['limitation'] = 'Envelope is not core compatibility. Check exact release requirements.'
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return 0
        if args.config.stat().st_size > 65536:
            raise ValueError()
        issues = audit(json.loads(args.config.read_text(encoding='utf-8')))
        print(json.dumps({'declared_checks_passed':not issues,'issues':issues,'limitation':LIMIT},indent=2))
        return 2 if issues else 0
    except (OSError, ValueError, UnicodeError):
        print(json.dumps({'error':'Cannot read valid UTF-8 JSON of at most 64 KiB.'}))
        return 2

if __name__ == '__main__':
    sys.exit(main())
