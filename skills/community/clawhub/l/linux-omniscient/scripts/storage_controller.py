#!/usr/bin/env python3
"""Storage Controller - Linux version."""
import subprocess, json, sys, os, argparse
from common import run_cmd

def list_drives():
    """List all drives with capacity/usage/filesystem."""
    stdout, _, code = run_cmd(['df', '-h'])
    return json.dumps({"drives": stdout if code == 0 else "error"}, indent=2)

def get_drive_info(drive=None):
    """Get drive details (default root)."""
    path = drive or '/'
    stdout, _, code = run_cmd(['df', '-h', path])
    return json.dumps({"info": stdout if code == 0 else "error"}, indent=2)

def get_health(drive=None):
    """Get disk health status."""
    stdout, _, code = run_cmd(['smartctl', '-H', drive or '/dev/sda'])
    return json.dumps({"health": stdout if code == 0 else "error"}, indent=2)

def find_big_files(top=20, drive=None):
    """Find largest files."""
    path = drive or '/'
    stdout, _, code = run_cmd(['find', path, '-type', 'f', '-exec', 'du', '-h', '{}', '+', '|', 'sort', '-rh', '|', 'head', '-n', str(top)])
    return json.dumps({"big_files": stdout if code == 0 else "error"}, indent=2)

def get_usage(path=None, top=15):
    """Analyze folder sizes."""
    target_path = path or os.path.expanduser('~')
    stdout, _, code = run_cmd(['du', '-h', '--max-depth=1', target_path, '|', 'sort', '-rh', '|', 'head', '-n', str(top)])
    return json.dumps({"usage": stdout if code == 0 else "error"}, indent=2)

def get_partitions():
    """Get physical disk-partition mapping."""
    stdout, _, code = run_cmd(['lsblk'])
    return json.dumps({"partitions": stdout if code == 0 else "error"}, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Storage Controller')
    subparsers = parser.add_subparsers(dest='command')

    # list command
    subparsers.add_parser('list')

    # info command
    info_parser = subparsers.add_parser('info')
    info_parser.add_argument('--drive', help='Drive path')

    # health command
    health_parser = subparsers.add_parser('health')
    health_parser.add_argument('--drive', help='Drive path')

    # big-files command
    big_parser = subparsers.add_parser('big-files')
    big_parser.add_argument('--drive', help='Drive path')
    big_parser.add_argument('--top', type=int, default=20)

    # usage command
    usage_parser = subparsers.add_parser('usage')
    usage_parser.add_argument('--path', help='Path to analyze')
    usage_parser.add_argument('--top', type=int, default=15)

    # partitions command
    subparsers.add_parser('partitions')

    args = parser.parse_args()

    if args.command == 'list':
        print(list_drives())
    elif args.command == 'info':
        print(get_drive_info(args.drive))
    elif args.command == 'health':
        print(get_health(args.drive))
    elif args.command == 'big-files':
        print(find_big_files(args.top, args.drive))
    elif args.command == 'usage':
        print(get_usage(args.path, args.top))
    elif args.command == 'partitions':
        print(get_partitions())

if __name__ == '__main__':
    main()
