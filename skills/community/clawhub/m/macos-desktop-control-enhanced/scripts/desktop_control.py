# scripts/desktop_control.py
"""
Unified macOS desktop control functions.
These functions wrap native macOS commands for screenshot, process,
clipboard, system info, app control and input simulation.
"""

import subprocess
import json
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Screenshot
# ---------------------------------------------------------------------------
def screenshot(region=None, file_path=None):
    """
    Capture the screen or a region.
    :param region: geometry string "x,y,w,h" or "x,y,w,h" for -r flag.
    :param file_path: destination path, defaults to /tmp/screenshot.png
    :return: path to saved image
    """
    cmd = ["screencapture"]
    if region:
        cmd.extend(["-r", region])
    target = file_path or "/tmp/screenshot.png"
    cmd.append(target)
    subprocess.run(cmd, check=True)
    return target

# ---------------------------------------------------------------------------
# Process Management
# ---------------------------------------------------------------------------
def get_front_process():
    """
    Get information about the frontmost process.
    :return: dict with pid, bundle_identifier, name
    """
    script = '''
    tell application "System Events"
        set frontApp to first process
        set frontAppName to name of frontApp
        set frontAppPID to pid of frontApp
        set frontAppBundleID to bundle identifier of frontApp
    end tell
    return {{
        "pid": frontAppPID,
        "bundle_id": frontAppBundleID,
        "name": frontAppName
    }}
    '''
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

def kill_process(pid):
    """Kill a process by PID."""
    subprocess.run(["kill", "-9", str(pid)], check=True)

def launch_app(bundle_id):
    """Launch an app by bundle identifier."""
    subprocess.run(["open", f"--b {bundle_id}"], check=True)

def terminate_app(bundle_id):
    """Force‑close an app by bundle identifier."""
    script = f'''
    pkill -f "{bundle_id}"
    '''
    subprocess.run(["osascript", "-e", script], check=True)

# ---------------------------------------------------------------------------
# Clipboard
# ---------------------------------------------------------------------------
def get_clipboard():
    """Get current clipboard text."""
    result = subprocess.run(["osascript", "-e", 'the clipboard as string'], capture_output=True, text=True, check=True)
    return result.stdout.strip()

def set_clipboard(text):
    """Set clipboard to given text."""
    script = f'set the clipboard to "{text}"'
    subprocess.run(["osascript", "-e", script], check=True)

# ---------------------------------------------------------------------------
# System Information
# ---------------------------------------------------------------------------
def get_system_info():
    """Return basic macOS system info (OS version, battery)."""
    # OS version
    os_ver = subprocess.run(["sw_vers", "-productVersion"], capture_output=True, text=True, check=True).stdout.strip()
    # Battery (using pmset)
    batt = subprocess.run(["pmset", "-g", "batt"], capture_output=True, text=True, check=True).stdout
    batt_percent = next((m.group(0) for m in [re.search(r'(\d+)%', line) for line in batt.splitlines()] if m), "unknown")
    return {"os_version": os_ver, "battery": batt_percent}

# ---------------------------------------------------------------------------
# Application Control
# ---------------------------------------------------------------------------
def focus_app(bundle_id):
    """Bring the given app to foreground."""
    subprocess.run(["osascript", "-e", f'tell application "{bundle_id}" to activate'], check=True)

def terminate_app(bundle_id):
    """Force‑close the given app."""
    script = f'''
    pkill -f "{bundle_id}"
    '''
    subprocess.run(["osascript", "-e", script], check=True)

# ---------------------------------------------------------------------------
# Mouse Control
# ---------------------------------------------------------------------------
def move_mouse(x, y):
    """Move cursor to screen coordinates (x, y)."""
    script = f'''
    tell application "System Events"
        set cursor to POSIX point {x}, {y}
    end tell
    '''
    subprocess.run(["osascript", "-e", script], check=True)

def click(x, y, button="left"):
    """Perform a mouse click at (x, y)."""
    down = f'''
    tell application "System Events"
        mouse down at POSIX point {x}, {y}
    end tell
    '''
    up = f'''
    tell application "System Events"
        mouse up at POSIX point {x}, {y}
    end tell
    '''
    subprocess.run(["osascript", "-e", down], check=True)
    subprocess.run(["osascript", "-e", up], check=True)

def drag(x1, y1, x2, y2, button="left"):
    """Drag from (x1, y1) to (x2, y2)."""
    # Simple implementation: move cursor then mouse down/up
    move_mouse(x2, y2)
    click(x2, y2, button)

# ---------------------------------------------------------------------------
# Keyboard Control
# ---------------------------------------------------------------------------
def type_text(text):
    """Type the given string."""
    script = f'''
    tell application "System Events"
        keystrokes "{text}"
    end tell
    '''
    subprocess.run(["osascript", "-e", script], check=True)

def press_key(key):
    """Press a single key (key code or name)."""
    script = f'''
    tell application "System Events"
        key code {key}
    end tell
    '''
    subprocess.run(["osascript", "-e", script], check=True)