#!/usr/bin/env python3
"""Printer Controller - Linux version."""
import subprocess, json, sys, os, argparse
from common import run_cmd

def list_printers():
    """List all printers."""
    stdout, _, code = run_cmd(['lpstat', '-p'])
    return json.dumps({"printers": stdout if code == 0 else "error"}, indent=2)

def set_default(name):
    """Set default printer."""
    stdout, _, code = run_cmd(['lpoptions', '-d', name])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def get_queue():
    """Get print queue."""
    stdout, _, code = run_cmd(['lpstat', '-o'])
    return json.dumps({"queue": stdout if code == 0 else "error"}, indent=2)

def cancel_job(job_id=None):
    """Cancel print job."""
    if job_id:
        stdout, _, code = run_cmd(['cancel', job_id])
    else:
        stdout, _, code = run_cmd(['cancel', '-a'])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def get_capabilities():
    """Get printer capabilities."""
    stdout, _, code = run_cmd(['lpstat', '-v'])
    return json.dumps({"capabilities": stdout if code == 0 else "error"}, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Printer Controller')
    subparsers = parser.add_subparsers(dest='command')

    # list command
    subparsers.add_parser('list')

    # set-default command
    default_parser = subparsers.add_parser('set-default')
    default_parser.add_argument('--name', required=True)

    # queue command
    subparsers.add_parser('queue')

    # cancel command
    cancel_parser = subparsers.add_parser('cancel')
    cancel_parser.add_argument('--job-id', help='Job ID')

    # capabilities command
    subparsers.add_parser('capabilities')

    args = parser.parse_args()

    if args.command == 'list':
        print(list_printers())
    elif args.command == 'set-default':
        print(set_default(args.name))
    elif args.command == 'queue':
        print(get_queue())
    elif args.command == 'cancel':
        print(cancel_job(args.job_id))
    elif args.command == 'capabilities':
        print(get_capabilities())

if __name__ == '__main__':
    main()
