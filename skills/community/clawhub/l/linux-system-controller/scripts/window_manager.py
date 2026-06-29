#!/usr/bin/env python3
"""
Window Manager - Linux desktop application control via xdotool and wmctrl.

Requirements: Linux with X11/Wayland, xdotool, wmctrl
Dependencies: None (uses system tools)
"""

import subprocess
import json
import sys
import os

# Fix print encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


def run_command(cmd, timeout=30):
    """Execute shell command with proper encoding handling."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace"
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "ERROR: Command timed out", -1
    except Exception as e:
        return "", f"ERROR: {e}", -1


def list_windows():
    """List all visible windows with title, process name, and window ID."""
    stdout, stderr, code = run_command("wmctrl -l")
    if code != 0:
        return {"error": f"Failed to list windows: {stderr}"}

    windows = []
    for line in stdout.split('\n'):
        if not line.strip():
            continue
        parts = line.split(None, 3)  # Split into max 4 parts
        if len(parts) >= 4:
            window_id = parts[0]
            desktop = parts[1]
            pid = parts[2]
            title = parts[3] if len(parts) > 3 else ""
            windows.append({
                "window_id": window_id,
                "desktop": desktop,
                "pid": int(pid) if pid.isdigit() else 0,
                "title": title
            })

    return {"windows": windows}


def activate_window(window_id=None, title=None, pid=None):
    """Activate (bring to foreground) a window."""
    if not window_id:
        # Find window by title or pid
        result = list_windows()
        if "error" in result:
            return result

        for win in result["windows"]:
            if title and title.lower() in win["title"].lower():
                window_id = win["window_id"]
                break
            if pid and win["pid"] == pid:
                window_id = win["window_id"]
                break

    if not window_id:
        return {"error": "Window not found"}

    stdout, stderr, code = run_command(f"wmctrl -ia {window_id}")
    if code == 0:
        return {"success": True, "window_id": window_id}
    else:
        return {"error": f"Failed to activate window: {stderr}"}


def close_window(window_id=None, title=None, pid=None):
    """Close a window."""
    if not window_id:
        result = list_windows()
        if "error" in result:
            return result

        for win in result["windows"]:
            if title and title.lower() in win["title"].lower():
                window_id = win["window_id"]
                break
            if pid and win["pid"] == pid:
                window_id = win["window_id"]
                break

    if not window_id:
        return {"error": "Window not found"}

    stdout, stderr, code = run_command(f"wmctrl -ic {window_id}")
    if code == 0:
        return {"success": True, "window_id": window_id}
    else:
        return {"error": f"Failed to close window: {stderr}"}


def minimize_window(window_id=None, title=None, pid=None):
    """Minimize a window."""
    if not window_id:
        result = list_windows()
        if "error" in result:
            return result

        for win in result["windows"]:
            if title and title.lower() in win["title"].lower():
                window_id = win["window_id"]
                break
            if pid and win["pid"] == pid:
                window_id = win["window_id"]
                break

    if not window_id:
        return {"error": "Window not found"}

    stdout, stderr, code = run_command(f"xdotool windowminimize {window_id}")
    if code == 0:
        return {"success": True, "window_id": window_id}
    else:
        return {"error": f"Failed to minimize window: {stderr}"}


def maximize_window(window_id=None, title=None, pid=None):
    """Maximize a window."""
    if not window_id:
        result = list_windows()
        if "error" in result:
            return result

        for win in result["windows"]:
            if title and title.lower() in win["title"].lower():
                window_id = win["window_id"]
                break
            if pid and win["pid"] == pid:
                window_id = win["window_id"]
                break

    if not window_id:
        return {"error": "Window not found"}

    stdout, stderr, code = run_command(f"wmctrl -ir {window_id} -b add,maximized_vert,maximized_horz")
    if code == 0:
        return {"success": True, "window_id": window_id}
    else:
        return {"error": f"Failed to maximize window: {stderr}"}


def resize_window(window_id=None, title=None, pid=None, x=None, y=None, width=None, height=None):
    """Resize and move a window."""
    if not window_id:
        result = list_windows()
        if "error" in result:
            return result

        for win in result["windows"]:
            if title and title.lower() in win["title"].lower():
                window_id = win["window_id"]
                break
            if pid and win["pid"] == pid:
                window_id = win["window_id"]
                break

    if not window_id:
        return {"error": "Window not found"}

    # Format: gravity, X, Y, width, height
    # Using 0 for gravity (NorthWest)
    cmd = f"wmctrl -ir {window_id} -e 0,{x},{y},{width},{height}"
    stdout, stderr, code = run_command(cmd)
    if code == 0:
        return {"success": True, "window_id": window_id}
    else:
        return {"error": f"Failed to resize window: {stderr}"}


def move_window(window_id=None, title=None, pid=None, x=None, y=None):
    """Move a window to specified position."""
    if not window_id:
        result = list_windows()
        if "error" in result:
            return result

        for win in result["windows"]:
            if title and title.lower() in win["title"].lower():
                window_id = win["window_id"]
                break
            if pid and win["pid"] == pid:
                window_id = win["window_id"]
                break

    if not window_id:
        return {"error": "Window not found"}

    # Get current window geometry
    stdout, stderr, code = run_command(f"xdotool getwindowgeometry {window_id}")
    if code != 0:
        return {"error": f"Failed to get window geometry: {stderr}"}

    # Parse current geometry to get width and height
    import re
    geometry = re.search(r'Geometry: (\d+)x(\d+)', stdout)
    if not geometry:
        return {"error": "Failed to parse window geometry"}

    width = geometry.group(1)
    height = geometry.group(2)

    # Move and resize to preserve dimensions
    cmd = f"wmctrl -ir {window_id} -e 0,{x},{y},{width},{height}"
    stdout, stderr, code = run_command(cmd)
    if code == 0:
        return {"success": True, "window_id": window_id}
    else:
        return {"error": f"Failed to move window: {stderr}"}


def send_keys(window_id=None, title=None, pid=None, text=None):
    """Send keystrokes to a window."""
    if not window_id:
        result = list_windows()
        if "error" in result:
            return result

        for win in result["windows"]:
            if title and title.lower() in win["title"].lower():
                window_id = win["window_id"]
                break
            if pid and win["pid"] == pid:
                window_id = win["window_id"]
                break

    if not window_id:
        return {"error": "Window not found"}

    # Activate window first
    activate_window(window_id=window_id)

    # Type the text (xdotool uses --delay to avoid issues with special chars)
    escaped_text = text.replace("'", "'\\''")
    stdout, stderr, code = run_command(f"xdotool type --delay 10 '{escaped_text}'")
    if code == 0:
        return {"success": True, "window_id": window_id}
    else:
        return {"error": f"Failed to send keys: {stderr}"}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Window Manager for Linux")
    subparsers = parser.add_subparsers(dest='action', help='Action to perform')

    # List windows
    parser_list = subparsers.add_parser('list', help='List all windows')

    # Activate window
    parser_activate = subparsers.add_parser('activate', help='Activate a window')
    parser_activate.add_argument('--title', help='Window title to search')
    parser_activate.add_argument('--pid', type=int, help='Process ID')
    parser_activate.add_argument('--window-id', help='Window ID')

    # Close window
    parser_close = subparsers.add_parser('close', help='Close a window')
    parser_close.add_argument('--title', help='Window title to search')
    parser_close.add_argument('--pid', type=int, help='Process ID')
    parser_close.add_argument('--window-id', help='Window ID')

    # Minimize window
    parser_minimize = subparsers.add_parser('minimize', help='Minimize a window')
    parser_minimize.add_argument('--title', help='Window title to search')
    parser_minimize.add_argument('--pid', type=int, help='Process ID')
    parser_minimize.add_argument('--window-id', help='Window ID')

    # Maximize window
    parser_maximize = subparsers.add_parser('maximize', help='Maximize a window')
    parser_maximize.add_argument('--title', help='Window title to search')
    parser_maximize.add_argument('--pid', type=int, help='Process ID')
    parser_maximize.add_argument('--window-id', help='Window ID')

    # Resize window
    parser_resize = subparsers.add_parser('resize', help='Resize a window')
    parser_resize.add_argument('--title', help='Window title to search')
    parser_resize.add_argument('--pid', type=int, help='Process ID')
    parser_resize.add_argument('--window-id', help='Window ID')
    parser_resize.add_argument('--x', type=int, required=True, help='X position')
    parser_resize.add_argument('--y', type=int, required=True, help='Y position')
    parser_resize.add_argument('--width', type=int, required=True, help='Width')
    parser_resize.add_argument('--height', type=int, required=True, help='Height')

    # Move window
    parser_move = subparsers.add_parser('move', help='Move a window')
    parser_move.add_argument('--title', help='Window title to search')
    parser_move.add_argument('--pid', type=int, help='Process ID')
    parser_move.add_argument('--window-id', help='Window ID')
    parser_move.add_argument('--x', type=int, required=True, help='X position')
    parser_move.add_argument('--y', type=int, required=True, help='Y position')

    # Send keys
    parser_send_keys = subparsers.add_parser('send-keys', help='Send keystrokes to window')
    parser_send_keys.add_argument('--title', help='Window title to search')
    parser_send_keys.add_argument('--pid', type=int, help='Process ID')
    parser_send_keys.add_argument('--window-id', help='Window ID')
    parser_send_keys.add_argument('--text', required=True, help='Text to type')

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    result = {}
    if args.action == 'list':
        result = list_windows()
    elif args.action == 'activate':
        result = activate_window(window_id=args.window_id, title=args.title, pid=args.pid)
    elif args.action == 'close':
        result = close_window(window_id=args.window_id, title=args.title, pid=args.pid)
    elif args.action == 'minimize':
        result = minimize_window(window_id=args.window_id, title=args.title, pid=args.pid)
    elif args.action == 'maximize':
        result = maximize_window(window_id=args.window_id, title=args.title, pid=args.pid)
    elif args.action == 'resize':
        result = resize_window(window_id=args.window_id, title=args.title, pid=args.pid,
                              x=args.x, y=args.y, width=args.width, height=args.height)
    elif args.action == 'move':
        result = move_window(window_id=args.window_id, title=args.title, pid=args.pid,
                            x=args.x, y=args.y)
    elif args.action == 'send-keys':
        result = send_keys(window_id=args.window_id, title=args.title, pid=args.pid, text=args.text)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
