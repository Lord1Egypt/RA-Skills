#!/usr/bin/env python3
"""Window Manager - Linux version via wmctrl/xdotool."""
import subprocess, json, sys, os, argparse
from common import run_cmd

def list_windows():
    """List all visible windows."""
    stdout, _, code = run_cmd(['wmctrl', '-l'])
    windows = []
    if code == 0:
        for line in stdout.split('\n'):
            if line.strip():
                parts = line.split(maxsplit=3)
                if len(parts) >= 4:
                    windows.append({"id": parts[0], "title": parts[3]})
    return json.dumps(windows, indent=2)

def activate_window(title=None, pid=None):
    """Activate a window by title or pid."""
    if title:
        stdout, _, code = run_cmd(['wmctrl', '-a', title])
    elif pid:
        # Find window by pid and activate
        stdout, _, code = run_cmd(['wmctrl', '-l', '-p'])
        if code == 0:
            for line in stdout.split('\n'):
                if str(pid) in line:
                    win_id = line.split()[0]
                    stdout, _, code = run_cmd(['wmctrl', '-i', '-a', win_id])
                    break
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def close_window(title=None, pid=None):
    """Close a window by title or pid."""
    if title:
        stdout, _, code = run_cmd(['wmctrl', '-c', title])
    elif pid:
        stdout, _, code = run_cmd(['wmctrl', '-l', '-p'])
        if code == 0:
            for line in stdout.split('\n'):
                if str(pid) in line:
                    win_id = line.split()[0]
                    stdout, _, code = run_cmd(['wmctrl', '-i', '-c', win_id])
                    break
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def minimize_window(title=None, pid=None):
    """Minimize a window."""
    if title:
        result = find_window_by_title(title)
    else:
        result = find_window_by_pid(pid)
    if result:
        stdout, _, code = run_cmd(['xdotool', 'windowminimize', result])
        return json.dumps({"success": code == 0}, indent=2)
    return json.dumps({"success": False, "message": "Window not found"}, indent=2)

def maximize_window(title=None, pid=None):
    """Maximize a window."""
    if title:
        result = find_window_by_title(title)
    else:
        result = find_window_by_pid(pid)
    if result:
        stdout, _, code = run_cmd(['wmctrl', '-i', '-r', result, '-b', 'add,maximized_vert,maximized_horz'])
        return json.dumps({"success": code == 0}, indent=2)
    return json.dumps({"success": False, "message": "Window not found"}, indent=2)

def resize_window(pid, x, y, width, height):
    """Resize and move window."""
    stdout, _, code = run_cmd(['wmctrl', '-l', '-p'])
    if code == 0:
        for line in stdout.split('\n'):
            if str(pid) in line:
                win_id = line.split()[0]
                cmd = ['wmctrl', '-i', '-r', win_id, '-e', f'0,{x},{y},{width},{height}']
                stdout, _, code = run_cmd(cmd)
                return json.dumps({"success": code == 0}, indent=2)
    return json.dumps({"success": False, "message": "Window not found"}, indent=2)

def send_keys(title, text):
    """Send keystrokes to window."""
    result = find_window_by_title(title)
    if result:
        stdout, _, code = run_cmd(['xdotool', 'type', '--window', result, text])
        return json.dumps({"success": code == 0}, indent=2)
    return json.dumps({"success": False, "message": "Window not found"}, indent=2)

def find_window_by_title(title):
    """Find window id by title."""
    stdout, _, code = run_cmd(['wmctrl', '-l'])
    if code == 0:
        for line in stdout.split('\n'):
            if title.lower() in line.lower():
                return line.split()[0]
    return None

def find_window_by_pid(pid):
    """Find window id by pid."""
    stdout, _, code = run_cmd(['wmctrl', '-l', '-p'])
    if code == 0:
        for line in stdout.split('\n'):
            if str(pid) in line:
                return line.split()[0]
    return None

def main():
    parser = argparse.ArgumentParser(description='Window Manager')
    subparsers = parser.add_subparsers(dest='command')

    # list command
    subparsers.add_parser('list')

    # activate command
    activate_parser = subparsers.add_parser('activate')
    activate_parser.add_argument('--title', help='Window title')
    activate_parser.add_argument('--pid', type=int, help='Process ID')

    # close command
    close_parser = subparsers.add_parser('close')
    close_parser.add_argument('--title', help='Window title')
    close_parser.add_argument('--pid', type=int, help='Process ID')

    # minimize command
    minimize_parser = subparsers.add_parser('minimize')
    minimize_parser.add_argument('--title', help='Window title')
    minimize_parser.add_argument('--pid', type=int, help='Process ID')

    # maximize command
    maximize_parser = subparsers.add_parser('maximize')
    maximize_parser.add_argument('--title', help='Window title')
    maximize_parser.add_argument('--pid', type=int, help='Process ID')

    # resize command
    resize_parser = subparsers.add_parser('resize')
    resize_parser.add_argument('--pid', type=int, required=True)
    resize_parser.add_argument('--x', type=int, required=True)
    resize_parser.add_argument('--y', type=int, required=True)
    resize_parser.add_argument('--width', type=int, required=True)
    resize_parser.add_argument('--height', type=int, required=True)

    # send-keys command
    keys_parser = subparsers.add_parser('send-keys')
    keys_parser.add_argument('--title', required=True, help='Window title')
    keys_parser.add_argument('--text', required=True, help='Text to send')

    args = parser.parse_args()

    if args.command == 'list':
        print(list_windows())
    elif args.command == 'activate':
        print(activate_window(args.title, args.pid))
    elif args.command == 'close':
        print(close_window(args.title, args.pid))
    elif args.command == 'minimize':
        print(minimize_window(args.title, args.pid))
    elif args.command == 'maximize':
        print(maximize_window(args.title, args.pid))
    elif args.command == 'resize':
        print(resize_window(args.pid, args.x, args.y, args.width, args.height))
    elif args.command == 'send-keys':
        print(send_keys(args.title, args.text))

if __name__ == '__main__':
    main()
