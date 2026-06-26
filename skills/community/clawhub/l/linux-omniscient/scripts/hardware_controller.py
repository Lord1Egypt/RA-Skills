#!/usr/bin/env python3
"""Hardware Controller - Linux version."""
import subprocess, json, sys, os, argparse, time
from common import run_cmd, is_windows

def get_volume():
    """Get current volume level."""
    if is_windows():
        return json.dumps({"volume": "Windows not supported"}, indent=2)
    stdout, _, code = run_cmd(['pactl', 'get-sink-volume', '@DEFAULT_SINK@'])
    return json.dumps({"volume": stdout if code == 0 else "error"}, indent=2)

def set_volume(level):
    """Set volume level (0-100)."""
    if is_windows():
        return json.dumps({"success": False, "message": "Windows not supported"}, indent=2)
    # Convert to pactl format (65536 = 100%)
    pactl_level = int(level * 655.36)
    stdout, _, code = run_cmd(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', f'{pactl_level}'])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def mute_volume():
    """Mute audio."""
    if is_windows():
        return json.dumps({"success": False, "message": "Windows not supported"}, indent=2)
    stdout, _, code = run_cmd(['pactl', 'set-sink-mute', '@DEFAULT_SINK@', 'toggle'])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def get_brightness():
    """Get screen brightness."""
    stdout, _, code = run_cmd(['brightnessctl', 'get'])
    if code == 0:
        return json.dumps({"brightness": stdout.strip()}, indent=2)
    return json.dumps({"brightness": "error"}, indent=2)

def set_brightness(level):
    """Set screen brightness (0-100)."""
    stdout, _, code = run_cmd(['brightnessctl', 'set', f'{level}%'])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def get_screen_info():
    """Get monitor info."""
    stdout, _, code = run_cmd(['xrandr'])
    return json.dumps({"info": stdout if code == 0 else "error"}, indent=2)

def lock_screen():
    """Lock screen."""
    stdout, _, code = run_cmd(['xdg-screensaver', 'lock'])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def sleep_system():
    """Suspend system."""
    stdout, _, code = run_cmd(['systemctl', 'suspend'])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def hibernate_system():
    """Hibernate system."""
    stdout, _, code = run_cmd(['systemctl', 'hibernate'])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def shutdown_system(delay=0):
    """Shutdown system."""
    if delay > 0:
        stdout, _, code = run_cmd(['shutdown', '-h', f'+{delay//60}'])
    else:
        stdout, _, code = run_cmd(['shutdown', '-h', 'now'])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def restart_system(delay=0):
    """Restart system."""
    if delay > 0:
        stdout, _, code = run_cmd(['shutdown', '-r', f'+{delay//60}'])
    else:
        stdout, _, code = run_cmd(['shutdown', '-r', 'now'])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def cancel_power_action():
    """Cancel scheduled shutdown/reboot."""
    stdout, _, code = run_cmd(['shutdown', '-c'])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def list_usb_devices():
    """List USB devices."""
    stdout, _, code = run_cmd(['lsusb'])
    return json.dumps({"usb_devices": stdout if code == 0 else "error"}, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Hardware Controller')
    subparsers = parser.add_subparsers(dest='command')

    # volume commands
    volume_parser = subparsers.add_parser('volume')
    volume_subparsers = volume_parser.add_subparsers(dest='volume_cmd')
    volume_get = volume_subparsers.add_parser('get')
    volume_set = volume_subparsers.add_parser('set')
    volume_set.add_argument('--level', type=int, required=True)
    volume_mute = volume_subparsers.add_parser('mute')

    # screen commands
    screen_parser = subparsers.add_parser('screen')
    screen_subparsers = screen_parser.add_subparsers(dest='screen_cmd')
    screen_bright = screen_subparsers.add_parser('brightness')
    screen_bright.add_argument('--level', type=int, default=0)
    screen_info = screen_subparsers.add_parser('info')

    # power commands
    power_parser = subparsers.add_parser('power')
    power_subparsers = power_parser.add_subparsers(dest='power_cmd')
    power_subparsers.add_parser('lock')
    power_subparsers.add_parser('sleep')
    power_subparsers.add_parser('hibernate')
    power_shutdown = power_subparsers.add_parser('shutdown')
    power_shutdown.add_argument('--delay', type=int, default=0)
    power_restart = power_subparsers.add_parser('restart')
    power_restart.add_argument('--delay', type=int, default=0)
    power_subparsers.add_parser('cancel')

    # usb commands
    usb_parser = subparsers.add_parser('usb')
    usb_subparsers = usb_parser.add_subparsers(dest='usb_cmd')
    usb_subparsers.add_parser('list')

    args = parser.parse_args()

    if args.command == 'volume':
        if args.volume_cmd == 'get':
            print(get_volume())
        elif args.volume_cmd == 'set':
            print(set_volume(args.level))
        elif args.volume_cmd == 'mute':
            print(mute_volume())
    elif args.command == 'screen':
        if args.screen_cmd == 'brightness':
            if args.level > 0:
                print(set_brightness(args.level))
            else:
                print(get_brightness())
        elif args.screen_cmd == 'info':
            print(get_screen_info())
    elif args.command == 'power':
        if args.power_cmd == 'lock':
            print(lock_screen())
        elif args.power_cmd == 'sleep':
            print(sleep_system())
        elif args.power_cmd == 'hibernate':
            print(hibernate_system())
        elif args.power_cmd == 'shutdown':
            print(shutdown_system(args.delay))
        elif args.power_cmd == 'restart':
            print(restart_system(args.delay))
        elif args.power_cmd == 'cancel':
            print(cancel_power_action())
    elif args.command == 'usb':
        if args.usb_cmd == 'list':
            print(list_usb_devices())

if __name__ == '__main__':
    main()
