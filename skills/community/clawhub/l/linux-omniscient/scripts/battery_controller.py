#!/usr/bin/env python3
"""Battery Controller - Linux version."""
import subprocess, json, sys, os, argparse
from common import run_cmd

def get_status():
    """Get battery status (percentage/charging/health)."""
    stdout, _, code = run_cmd(['upower', '-i', '/org/freedesktop/UPower/devices/battery_BAT0'])
    return json.dumps({"status": stdout if code == 0 else "error"}, indent=2)

def get_history():
    """Get battery capacity history."""
    stdout, _, code = run_cmd(['upower', '-d'])
    return json.dumps({"history": stdout if code == 0 else "error"}, indent=2)

def list_plans():
    """List all power plans."""
    stdout, _, code = run_cmd(['powerprofilesctl', 'list'])
    return json.dumps({"plans": stdout if code == 0 else "error"}, indent=2)

def get_current_plan():
    """Get current active plan."""
    stdout, _, code = run_cmd(['powerprofilesctl', 'get'])
    return json.dumps({"current": stdout.strip() if code == 0 else "error"}, indent=2)

def set_plan(name):
    """Set power plan by name."""
    stdout, _, code = run_cmd(['powerprofilesctl', 'set', name])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def generate_report(output=None):
    """Generate battery report HTML."""
    report_path = output or os.path.expanduser('~/battery_report.html')
    stdout, _, code = run_cmd(['upower', '-i', '/org/freedesktop/UPower/devices/battery_BAT0'])
    with open(report_path, 'w') as f:
        f.write(f'<html><body><pre>{stdout}</pre></body></html>')
    return json.dumps({"success": True, "output": report_path}, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Battery Controller')
    subparsers = parser.add_subparsers(dest='command')

    # status command
    subparsers.add_parser('status')

    # history command
    subparsers.add_parser('history')

    # plans command
    subparsers.add_parser('plans')

    # current command
    subparsers.add_parser('current')

    # set-plan command
    plan_parser = subparsers.add_parser('set-plan')
    plan_parser.add_argument('--name', required=True)

    # report command
    report_parser = subparsers.add_parser('report')
    report_parser.add_argument('--output', help='Output path')

    args = parser.parse_args()

    if args.command == 'status':
        print(get_status())
    elif args.command == 'history':
        print(get_history())
    elif args.command == 'plans':
        print(list_plans())
    elif args.command == 'current':
        print(get_current_plan())
    elif args.command == 'set-plan':
        print(set_plan(args.name))
    elif args.command == 'report':
        print(generate_report(args.output))

if __name__ == '__main__':
    main()
