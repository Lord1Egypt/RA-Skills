#!/usr/bin/env python3
"""Display Controller - Linux version."""
import subprocess, json, sys, os, argparse
from common import run_cmd

def get_info():
    """Get display resolution/refresh rate."""
    stdout, _, code = run_cmd(['xrandr'])
    return json.dumps({"display": stdout if code == 0 else "error"}, indent=2)

def get_layout():
    """Get multi-monitor layout."""
    stdout, _, code = run_cmd(['xrandr', '--query'])
    return json.dumps({"layout": stdout if code == 0 else "error"}, indent=2)

def get_dpi():
    """Get DPI and scaling percentage."""
    stdout, _, code = run_cmd(['xdpyinfo', '|', 'grep', 'resolution'])
    return json.dumps({"dpi": stdout if code == 0 else "error"}, indent=2)

def night_light(action):
    """Toggle night light."""
    if action == 'on':
        stdout, _, code = run_cmd(['gsettings', 'set', 'org.gnome.settings-daemon.plugins.color', 'night-light-enabled', 'true'])
    elif action == 'off':
        stdout, _, code = run_cmd(['gsettings', 'set', 'org.gnome.settings-daemon.plugins.color', 'night-light-enabled', 'false'])
    else:
        stdout, _, code = run_cmd(['gsettings', 'get', 'org.gnome.settings-daemon.plugins.color', 'night-light-enabled'])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Display Controller')
    subparsers = parser.add_subparsers(dest='command')

    # info command
    subparsers.add_parser('info')

    # layout command
    subparsers.add_parser('layout')

    # dpi command
    subparsers.add_parser('dpi')

    # night-light command
    nl_parser = subparsers.add_parser('night-light')
    nl_parser.add_argument('action', choices=['on', 'off', 'status'])

    args = parser.parse_args()

    if args.command == 'info':
        print(get_info())
    elif args.command == 'layout':
        print(get_layout())
    elif args.command == 'dpi':
        print(get_dpi())
    elif args.command == 'night-light':
        print(night_light(args.action))

if __name__ == '__main__':
    main()
