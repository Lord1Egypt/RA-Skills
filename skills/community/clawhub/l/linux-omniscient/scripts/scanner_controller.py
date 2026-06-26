#!/usr/bin/env python3
"""Scanner Controller - Linux version."""
import subprocess, json, sys, os, argparse
from common import run_cmd

def list_scanners():
    """List all scanners."""
    stdout, _, code = run_cmd(['sane-find-scanner', '-q'])
    return json.dumps({"scanners": stdout if code == 0 else "error"}, indent=2)

def get_scanner_details():
    """Get scanner details."""
    stdout, _, code = run_cmd(['scanimage', '-L'])
    return json.dumps({"details": stdout if code == 0 else "error"}, indent=2)

def get_wia_status():
    """Get WIA service status (Linux equivalent)."""
    stdout, _, code = run_cmd(['systemctl', 'status', 'saned'])
    return json.dumps({"wia_status": stdout if code == 0 else "error"}, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Scanner Controller')
    subparsers = parser.add_subparsers(dest='command')

    # list command
    subparsers.add_parser('list')

    # details command
    subparsers.add_parser('details')

    # wia command
    subparsers.add_parser('wia')

    args = parser.parse_args()

    if args.command == 'list':
        print(list_scanners())
    elif args.command == 'details':
        print(get_scanner_details())
    elif args.command == 'wia':
        print(get_wia_status())

if __name__ == '__main__':
    main()
