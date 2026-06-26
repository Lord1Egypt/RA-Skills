#!/usr/bin/env python3
"""Thermal Controller - Linux version."""
import subprocess, json, sys, os, argparse, time
from common import run_cmd

def get_status():
    """Get CPU/GPU temperature and fan speed."""
    stdout, _, code = run_cmd(['sensors'])
    return json.dumps({"temperature": stdout if code == 0 else "error"}, indent=2)

def monitor(interval=2, count=5):
    """Real-time temperature monitoring."""
    results = []
    for i in range(count):
        stdout, _, code = run_cmd(['sensors'])
        if code == 0:
            results.append({"iteration": i+1, "data": stdout.strip()})
        time.sleep(interval)
    return json.dumps({"monitor_results": results}, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Thermal Controller')
    subparsers = parser.add_subparsers(dest='command')

    # status command
    subparsers.add_parser('status')

    # monitor command
    monitor_parser = subparsers.add_parser('monitor')
    monitor_parser.add_argument('--interval', type=int, default=2)
    monitor_parser.add_argument('--count', type=int, default=5)

    args = parser.parse_args()

    if args.command == 'status':
        print(get_status())
    elif args.command == 'monitor':
        print(monitor(args.interval, args.count))

if __name__ == '__main__':
    main()
