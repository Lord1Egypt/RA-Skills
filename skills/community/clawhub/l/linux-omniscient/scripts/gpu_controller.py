#!/usr/bin/env python3
"""GPU Controller - Linux version."""
import subprocess, json, sys, os, argparse, time
from common import run_cmd

def get_info():
    """Get GPU overview information."""
    stdout, _, code = run_cmd(['lspci', '|', 'grep', '-i', 'vga'])
    return json.dumps({"gpu": stdout if code == 0 else "error"}, indent=2)

def list_gpus():
    """List all GPUs with indices."""
    stdout, _, code = run_cmd(['lspci', '-nn', '|', 'grep', '-i', 'vga'])
    gpus = []
    if code == 0:
        for i, line in enumerate(stdout.split('\n')):
            if line.strip():
                gpus.append({"index": i, "info": line})
    return json.dumps({"gpus": gpus}, indent=2)

def monitor(interval=2, count=5):
    """Monitor GPU in real-time (utilization/temperature/power)."""
    results = []
    for i in range(count):
        stdout, _, code = run_cmd(['nvidia-smi', '--query-gpu=utilization.gpu,temperature.gpu,power.draw', '--format=csv,noheader'])
        if code == 0:
            results.append({"iteration": i+1, "data": stdout.strip()})
        time.sleep(interval)
    return json.dumps({"monitor_results": results}, indent=2)

def main():
    parser = argparse.ArgumentParser(description='GPU Controller')
    subparsers = parser.add_subparsers(dest='command')

    # info command
    subparsers.add_parser('info')

    # list-gpus command
    subparsers.add_parser('list-gpus')

    # monitor command
    monitor_parser = subparsers.add_parser('monitor')
    monitor_parser.add_argument('--interval', type=int, default=2)
    monitor_parser.add_argument('--count', type=int, default=5)

    args = parser.parse_args()

    if args.command == 'info':
        print(get_info())
    elif args.command == 'list-gpus':
        print(list_gpus())
    elif args.command == 'monitor':
        print(monitor(args.interval, args.count))

if __name__ == '__main__':
    main()
