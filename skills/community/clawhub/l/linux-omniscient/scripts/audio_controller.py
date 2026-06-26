#!/usr/bin/env python3
"""Audio Controller - Linux version."""
import subprocess, json, sys, os, argparse, tempfile, time
from common import run_cmd

def list_devices():
    """List all audio devices (WMI equivalent)."""
    stdout, _, code = run_cmd(['pactl', 'list', 'sinks', 'short'])
    return json.dumps({"devices": stdout if code == 0 else "error"}, indent=2)

def devices():
    """Get COM detailed list (output+input)."""
    stdout, _, code = run_cmd(['pactl', 'list', 'sinks'])
    stdout2, _, code2 = run_cmd(['pactl', 'list', 'sources'])
    return json.dumps({"output_devices": stdout if code == 0 else "error",
                      "input_devices": stdout2 if code2 == 0 else "error"}, indent=2)

def set_default_device(index=None, name=None, device_type='output'):
    """Set default audio device."""
    if index is not None:
        if device_type == 'input':
            stdout, _, code = run_cmd(['pactl', 'set-default-source', str(index)])
        else:
            stdout, _, code = run_cmd(['pactl', 'set-default-sink', str(index)])
    elif name:
        if device_type == 'input':
            stdout, _, code = run_cmd(['pactl', 'set-default-source', name])
        else:
            stdout, _, code = run_cmd(['pactl', 'set-default-sink', name])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def get_volume():
    """Get current volume."""
    stdout, _, code = run_cmd(['pactl', 'get-sink-volume', '@DEFAULT_SINK@'])
    return json.dumps({"volume": stdout if code == 0 else "error"}, indent=2)

def set_volume(level):
    """Set volume level (0-100)."""
    pactl_level = int(level * 655.36)
    stdout, _, code = run_cmd(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', f'{pactl_level}'])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def record_audio(duration=10, output=None):
    """Record audio for specified duration."""
    output_file = output or f'/tmp/recording_{int(time.time())}.wav'
    stdout, _, code = run_cmd(['arecord', '-d', str(duration), '-f', 'cd', output_file])
    return json.dumps({"success": code == 0, "output": output_file, "message": stdout}, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Audio Controller')
    subparsers = parser.add_subparsers(dest='command')

    # list command
    subparsers.add_parser('list')

    # devices command
    subparsers.add_parser('devices')

    # set-default command
    default_parser = subparsers.add_parser('set-default')
    default_parser.add_argument('--index', type=int, help='Device index')
    default_parser.add_argument('--name', help='Device name')
    default_parser.add_argument('--type', default='output', choices=['input', 'output'])

    # volume commands
    volume_parser = subparsers.add_parser('volume')
    volume_subparsers = volume_parser.add_subparsers(dest='volume_cmd')
    volume_get = volume_subparsers.add_parser('get')
    volume_set = volume_subparsers.add_parser('set')
    volume_set.add_argument('--level', type=int, required=True)

    # record command
    record_parser = subparsers.add_parser('record')
    record_parser.add_argument('--duration', type=int, default=10)
    record_parser.add_argument('--output', help='Output path')

    args = parser.parse_args()

    if args.command == 'list':
        print(list_devices())
    elif args.command == 'devices':
        print(devices())
    elif args.command == 'set-default':
        print(set_default_device(args.index, args.name, args.type))
    elif args.command == 'volume':
        if args.volume_cmd == 'get':
            print(get_volume())
        elif args.volume_cmd == 'set':
            print(set_volume(args.level))
    elif args.command == 'record':
        print(record_audio(args.duration, args.output))

if __name__ == '__main__':
    main()
