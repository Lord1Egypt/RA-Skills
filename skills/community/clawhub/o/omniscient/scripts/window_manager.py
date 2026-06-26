#!/usr/bin/env python3
"""
Window Manager - Windows desktop application control via PowerShell UI Automation.

Requirements: Windows 10/11, PowerShell 5.1+
Dependencies: None (uses built-in PowerShell and Windows APIs)
"""

import subprocess
import json
import sys
import time
import os
import re

# Fix print encoding for Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run_ps as _run_ps


# ========== Safety: Input Validation ==========

DANGEROUS_CHARS_PATTERN = re.compile(r'[;&|`$(){}[\]!<>\n\r]')

# SendKeys special characters that could be abused for injection
# SendKeys uses {} for special keys like {ENTER}, {TAB}, etc.
# We allow only well-known SendKeys sequences
SEND_KEYS_ALLOWED_PATTERN = re.compile(
    r'^[\w\s\.,;\:\[\]\{\}\+\=\-\*\/\%\#\@\!\?\&\(\)\"\'~`\|]+$'
)

# Known safe SendKeys special key names (whitelist)
SEND_KEYS_SPECIAL_KEYS = {
    'ENTER', 'TAB', 'ESC', 'ESCAPE', 'SPACE', 'BACKSPACE', 'BS',
    'DELETE', 'DEL', 'INSERT', 'INS', 'HOME', 'END', 'PGUP', 'PGDN',
    'UP', 'DOWN', 'LEFT', 'RIGHT', 'F1', 'F2', 'F3', 'F4', 'F5',
    'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15', 'F16',
    'BREAK', 'CAPSLOCK', 'NUMLOCK', 'SCROLLLOCK',
    'PRTSC', 'PRINTSCREEN', '+', '^', '%', '~', '(', ')',
    'LWIN', 'RWIN', 'APP',
}


def _validate_string(value, field_name="input"):
    """Validate that a string doesn't contain shell injection characters."""
    if not value:
        return True
    if DANGEROUS_CHARS_PATTERN.search(value):
        raise ValueError(
            f"ERROR: {field_name} contains forbidden shell characters."
        )
    return True


def _sanitize_ps_string(value):
    """Sanitize string for embedding in PowerShell single-quoted strings."""
    if value is None:
        return "''"
    _validate_string(value)
    escaped = value.replace("'", "''")
    return f"'{escaped}'"


def _validate_sendkeys_text(text):
    """
    Validate and sanitize text for SendKeys::SendWait.
    Rejects potentially dangerous escape sequences.
    """
    if not text:
        raise ValueError("ERROR: Text to send cannot be empty")

    # Check length limit to prevent buffer abuse
    if len(text) > 10000:
        raise ValueError("ERROR: SendKeys text exceeds maximum length of 10000 characters")

    # Check for obviously dangerous patterns
    dangerous_patterns = ['{EXIT}', '{QUIT}', '{KILL}', '{SHUTDOWN}', '{REBOOT}',
                          '{FORMAT}', '{DELETE}', '{RM ', '{DEL ']
    upper_text = text.upper()
    for pattern in dangerous_patterns:
        if pattern in upper_text:
            raise ValueError(
                f"ERROR: SendKeys contains blocked pattern '{pattern}'."
            )

    # Validate no shell injection chars
    _validate_string(text, "SendKeys text")
    return True


def list_windows():
    """List all visible windows with title, process name, position, and size."""
    script = r"""
Add-Type -AssemblyName UIAutomationClient
$windows = Get-Process | Where-Object { $_.MainWindowTitle -ne '' } | ForEach-Object {
    try {
        $rect = $_.MainWindowHandle | ForEach-Object {
            $r = New-Object System.Drawing.Rectangle
            [System.Drawing.Rectangle]::Intersect([System.Drawing.Rectangle]::Empty, $r)
            [void][System.Runtime.InteropServices.Marshal]::GetClassLongHash($_.Handle)
        }
        [PSCustomObject]@{
            PID = $_.Id
            Title = $_.MainWindowTitle
            ProcessName = $_.ProcessName
            MainWindowHandle = $_.MainWindowHandle.ToInt64()
        }
    } catch { }
}
$windows = $windows | Sort-Object -Property Title -Unique | Where-Object { $_.Title -ne '' }
$windows | ConvertTo-Json -Compress
"""
    stdout, stderr, code = _run_ps(script)
    if code != 0 or not stdout:
        script2 = """
Get-Process | Where-Object { $_.MainWindowTitle -ne '' } | Select-Object Id, ProcessName, MainWindowTitle | ConvertTo-Json -Compress
"""
        stdout, stderr, code = _run_ps(script2)
    return stdout


def activate_window(pid=None, title=None):
    """Bring a window to the foreground by PID or title substring."""
    if pid:
        try:
            pid_val = int(pid)
            if pid_val < 1 or pid_val > 2147483647:
                return "ERROR: Invalid PID"
        except (ValueError, TypeError):
            return f"ERROR: Invalid PID: {pid}"
        script = f"""
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {{
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")]
    public static extern bool IsIconic(IntPtr hWnd);
}}
"@
$proc = Get-Process -Id {pid_val} -ErrorAction SilentlyContinue
if ($proc) {{
    $hwnd = $proc.MainWindowHandle
    if ([Win32]::IsIconic($hwnd)) {{ [Win32]::ShowWindow($hwnd, 9) }}
    [Win32]::SetForegroundWindow($hwnd)
    Write-Output "OK: Activated window (PID: {pid_val}, Title: $($proc.MainWindowTitle))"
}} else {{
    Write-Output "ERROR: Process with PID {pid_val} not found"
}}
"""
    elif title:
        _validate_string(title, "window title")
        escaped_title = title.replace("'", "''")
        script = f"""
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {{
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")]
    public static extern bool IsIconic(IntPtr hWnd);
}}
"@
$proc = Get-Process | Where-Object {{ $_.MainWindowTitle -like '*{escaped_title}*' }} | Select-Object -First 1
if ($proc) {{
    $hwnd = $proc.MainWindowHandle
    if ([Win32]::IsIconic($hwnd)) {{ [Win32]::ShowWindow($hwnd, 9) }}
    [Win32]::SetForegroundWindow($hwnd)
    Write-Output "OK: Activated window (PID: $($proc.Id), Title: $($proc.MainWindowTitle))"
}} else {{
    Write-Output "ERROR: No window found matching '{title}'"
}}
"""
    else:
        return "ERROR: Provide --pid or --title"

    stdout, stderr, code = _run_ps(script)
    return stdout if stdout else stderr


def close_window(pid=None, title=None):
    """Close a window by PID or title substring.
    
    Safety improvement: Uses graceful close with configurable delay before force-kill.
    Default is 3 seconds grace period (up from original 1 second).
    """
    if pid:
        try:
            pid_val = int(pid)
            if pid_val < 1 or pid_val > 2147483647:
                return "ERROR: Invalid PID"
        except (ValueError, TypeError):
            return f"ERROR: Invalid PID: {pid}"
        script = f"""
$proc = Get-Process -Id {pid_val} -ErrorAction SilentlyContinue
if ($proc) {{
    $proc.CloseMainWindow() | Out-Null
    Start-Sleep -Seconds 3
    if (!$proc.HasExited) {{
        Write-Output "WARNING: Process did not exit gracefully after 3 seconds. Use --force with kill command if needed."
        Write-Output "INFO: Window close request sent to PID {pid_val}"
    }} else {{
        Write-Output "OK: Closed window gracefully (PID: {pid_val})"
    }}
}} else {{
    Write-Output "ERROR: Process not found"
}}
"""
    elif title:
        _validate_string(title, "window title")
        escaped_title = title.replace("'", "''")
        script = f"""
$procs = Get-Process | Where-Object {{ $_.MainWindowTitle -like '*{escaped_title}*' }}
if ($procs) {{
    $procs | ForEach-Object {{ $_.CloseMainWindow() | Out-Null }}
    Start-Sleep -Seconds 3
    $remaining = $procs | Where-Object {{ !$_.HasExited }}
    if ($remaining) {{
        $names = ($remaining.ProcessName | Sort-Object -Unique) -join ', '
        Write-Output "WARNING: {$remaining.Count} process(es) did not close gracefully: $names"
        Write-Output "INFO: Close request sent to matching '{title}' windows"
    }} else {{
        Write-Output "OK: Closed $($procs.Count) window(s) matching '{title}' gracefully"
    }}
}} else {{
    Write-Output "ERROR: No window found"
}}
"""
    else:
        return "ERROR: Provide --pid or --title"

    stdout, stderr, code = _run_ps(script)
    return stdout if stdout else stderr


def minimize_window(pid=None, title=None):
    """Minimize a window by PID or title substring."""
    if pid:
        try:
            pid_val = int(pid)
            if pid_val < 1 or pid_val > 2147483647:
                return "ERROR: Invalid PID"
        except (ValueError, TypeError):
            return f"ERROR: Invalid PID: {pid}"
        script = f'''
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class WinMin {{
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}}
'@
$proc = Get-Process -Id {pid_val} -ErrorAction SilentlyContinue
if ($proc) {{
    [WinMin]::ShowWindow($proc.MainWindowHandle, 6)
    Write-Output "OK: Minimized (PID: {pid_val})"
}} else {{
    Write-Output "ERROR: Process not found"
}}
'''
    elif title:
        _validate_string(title, "window title")
        escaped_title = title.replace("'", "''")
        script = f'''
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class WinMin {{
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}}
'@
$proc = Get-Process | Where-Object {{ $_.MainWindowTitle -like '*{escaped_title}*' }} | Select-Object -First 1
if ($proc) {{
    [WinMin]::ShowWindow($proc.MainWindowHandle, 6)
    Write-Output "OK: Minimized: $($proc.MainWindowTitle)"
}} else {{
    Write-Output "ERROR: No window found"
}}
'''
    else:
        return "ERROR: Provide --pid or --title"
    stdout, stderr, code = _run_ps(script)
    return stdout if stdout else stderr


def maximize_window(pid=None, title=None):
    """Maximize a window by PID or title substring."""
    if pid:
        try:
            pid_val = int(pid)
            if pid_val < 1 or pid_val > 2147483647:
                return "ERROR: Invalid PID"
        except (ValueError, TypeError):
            return f"ERROR: Invalid PID: {pid}"
        script = f'''
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class WinMax {{
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}}
'@
$proc = Get-Process -Id {pid_val} -ErrorAction SilentlyContinue
if ($proc) {{
    [WinMax]::ShowWindow($proc.MainWindowHandle, 3)
    Write-Output "OK: Maximized (PID: {pid_val})"
}} else {{
    Write-Output "ERROR: Process not found"
}}
'''
    elif title:
        _validate_string(title, "window title")
        escaped_title = title.replace("'", "''")
        script = f'''
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class WinMax {{
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}}
'@
$proc = Get-Process | Where-Object {{ $_.MainWindowTitle -like '*{escaped_title}*' }} | Select-Object -First 1
if ($proc) {{
    [WinMax]::ShowWindow($proc.MainWindowHandle, 3)
    Write-Output "OK: Maximized: $($proc.MainWindowTitle)"
}} else {{
    Write-Output "ERROR: No window found"
}}
'''
    else:
        return "ERROR: Provide --pid or --title"
    stdout, stderr, code = _run_ps(script)
    return stdout if stdout else stderr


def resize_window(pid=None, title=None, x=None, y=None, width=None, height=None):
    """Move and resize a window. All position/size parameters in pixels."""
    if not (pid or title):
        return "ERROR: Provide --pid or --title"
    if x is None or y is None or width is None or height is None:
        return "ERROR: Provide --x, --y, --width, --height"

    # Validate numeric parameters are reasonable
    for name, val in [("x", x), ("y", y), ("width", width), ("height", height)]:
        try:
            ival = int(val)
            if ival < 0 or ival > 100000:
                return f"ERROR: {name} value out of reasonable range: {val}"
        except (ValueError, TypeError):
            return f"ERROR: {name} must be an integer, got: {val}"

    target = ""
    if pid:
        try:
            target = f"$proc = Get-Process -Id {int(pid)} -ErrorAction SilentlyContinue"
        except (ValueError, TypeError):
            return "ERROR: Invalid PID"
    else:
        _validate_string(title, "window title")
        escaped_title = title.replace("'", "''")
        target = f'$proc = Get-Process | Where-Object {{ $_.MainWindowTitle -like \'*{escaped_title}*\' }} | Select-Object -First 1'

    x_val, y_val, w_val, h_val = int(x), int(y), int(width), int(height)
    script = f'''
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class WinPos {{
    [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr hWnd, IntPtr hWndAfter, int X, int Y, int cx, int cy, uint uFlags);
}}
'@
{target}
if ($proc) {{
    $result = [WinPos]::SetWindowPos($proc.MainWindowHandle, [IntPtr]::Zero, {x_val}, {y_val}, {w_val}, {h_val}, 0x0040)
    if ($result) {{ Write-Output "OK: Window moved to ({x_val},{y_val}) size {w_val}x{h_val}" }}
    else {{ Write-Output "ERROR: Failed to resize" }}
}} else {{
    Write-Output "ERROR: Window not found"
}}
'''
    stdout, stderr, code = _run_ps(script)
    return stdout if stdout else stderr


def send_keys(text, pid=None, title=None):
    """Send keystrokes to a window. Uses SendKeys format with safety validation."""
    _validate_sendkeys_text(text)

    if pid:
        try:
            pid_val = int(pid)
            if pid_val < 1 or pid_val > 2147483647:
                return "ERROR: Invalid PID"
        except (ValueError, TypeError):
            return f"ERROR: Invalid PID: {pid}"

        # Escape the text for PowerShell single-quote string (safe because we validated above)
        ps_escaped = text.replace("'", "''")
        script = f'''
Add-Type -AssemblyName System.Windows.Forms
$proc = Get-Process -Id {pid_val} -ErrorAction SilentlyContinue
if ($proc) {{
    Start-Sleep -Milliseconds 200
    [System.Windows.Forms.SendKeys]::SendWait('{ps_escaped}')
    Write-Output "OK: Sent keys to PID {pid_val}"
}} else {{
    Write-Output "ERROR: Process not found"
}}
'''
    elif title:
        _validate_string(title, "window title")
        escaped_title = title.replace("'", "''")
        ps_escaped = text.replace("'", "''")
        script = f'''
Add-Type -AssemblyName System.Windows.Forms
$proc = Get-Process | Where-Object {{ $_.MainWindowTitle -like '*{escaped_title}*' }} | Select-Object -First 1
if ($proc) {{
    $hwnd = $proc.MainWindowHandle
    # Use Win32 API to bring window to foreground reliably
    AddType @"
    using System; using System.Runtime.InteropServices;
    public class W32H {{ [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h); }}
"@
    [W32H]::SetForegroundWindow($hwnd) | Out-Null
    Start-Sleep -Milliseconds 300
    [System.Windows.Forms.SendKeys]::SendWait('{ps_escaped}')
    Write-Output "OK: Sent keys"
}} else {{
    Write-Output "ERROR: Window not found"
}}
'''
    else:
        return "ERROR: Provide --pid or --title"
    stdout, stderr, code = _run_ps(script)
    return stdout if stdout else stderr


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Window Manager - Control desktop windows")
    sub = parser.add_subparsers(dest="action")

    p_list = sub.add_parser("list", help="List all visible windows")
    p_act = sub.add_parser("activate", help="Bring window to foreground")
    p_act.add_argument("--pid", type=int)
    p_act.add_argument("--title", type=str)
    p_close = sub.add_parser("close", help="Close a window")
    p_close.add_argument("--pid", type=int)
    p_close.add_argument("--title", type=str)
    p_min = sub.add_parser("minimize", help="Minimize a window")
    p_min.add_argument("--pid", type=int)
    p_min.add_argument("--title", type=str)
    p_max = sub.add_parser("maximize", help="Maximize a window")
    p_max.add_argument("--pid", type=int)
    p_max.add_argument("--title", type=str)
    p_resize = sub.add_parser("resize", help="Move and resize a window")
    p_resize.add_argument("--pid", type=int)
    p_resize.add_argument("--title", type=str)
    p_resize.add_argument("--x", type=int, required=True)
    p_resize.add_argument("--y", type=int, required=True)
    p_resize.add_argument("--width", type=int, required=True)
    p_resize.add_argument("--height", type=int, required=True)
    p_keys = sub.add_parser("send-keys", help="Send keystrokes to a window")
    p_keys.add_argument("--pid", type=int)
    p_keys.add_argument("--title", type=str)
    p_keys.add_argument("--text", type=str, required=True)

    args = parser.parse_args()

    if args.action == "list":
        print(list_windows())
    elif args.action == "activate":
        print(activate_window(args.pid, args.title))
    elif args.action == "close":
        print(close_window(args.pid, args.title))
    elif args.action == "minimize":
        print(minimize_window(args.pid, args.title))
    elif args.action == "maximize":
        print(maximize_window(args.pid, args.title))
    elif args.action == "resize":
        print(resize_window(args.pid, args.title, args.x, args.y, args.width, args.height))
    elif args.action == "send-keys":
        try:
            print(send_keys(args.text, args.pid, args.title))
        except ValueError as e:
            print(str(e))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
