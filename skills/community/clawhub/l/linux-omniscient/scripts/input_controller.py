#!/usr/bin/env python3
"""Input Controller - Linux version."""
import subprocess, json, sys, os, argparse
from common import run_cmd

def list_keyboards():
    """List keyboard devices."""
    stdout, _, code = run_cmd(['xinput', 'list', '|', 'grep', 'keyboard'])
    return json.dumps({"keyboards": stdout if code == 0 else "error"}, indent=2)

def list_mice():
    """List mouse/pointer devices."""
    stdout, _, code = run_cmd(['xinput', 'list', '|', 'grep', 'mouse'])
    return json.dumps({"mice": stdout if code == 0 else "error"}, indent=2)

def list_gamepads():
    """List gamepad devices."""
    stdout, _, code = run_cmd(['xinput', 'list', '|', 'grep', 'Gamepad'])
    return json.dumps({"gamepads": stdout if code == 0 else "error"}, indent=2)

def list_all():
    """List all input devices."""
    stdout, _, code = run_cmd(['xinput', 'list'])
    return json.dumps({"devices": stdout if code == 0 else "error"}, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Input Controller')
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('keyboards')
    subparsers.add_parser('mice')
    subparsers.add_parser('gamepads')
    subparsers.add_parser('all')

    args = parser.parse_args()

    if args.command == 'keyboards':
        print(list_keyboards())
    elif args.command == 'mice':
        print(list_mice())
    elif args.command == 'gamepads':
        print(list_gamepads())
    elif args.command == 'all':
        print(list_all())

if __name__ == '__main__':
    main()
