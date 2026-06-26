#!/usr/bin/env python3
"""
Process Manager - List, start, stop, and monitor system processes.

Requirements: Windows 10/11, PowerShell 5.1+
Dependencies: None (uses built-in PowerShell)
"""

import subprocess
import sys
import os
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run_ps as _run_ps


# ========== Safety: Input Validation ==========

# Dangerous characters that should never appear in process names or commands
DANGEROUS_CHARS_PATTERN = re.compile(r'[;&|`$(){}[\]!<>\n\r]')

# Protected system processes that must not be killed
PROTECTED_PROCESSES = {
    'csrss', 'csrss.exe',
    'lsass', 'lsass.exe',
    'services', 'services.exe',
    'svchost', 'svchost.exe',
    'winlogon', 'winlogon.exe',
    'wininit', 'wininit.exe',
    'smss', 'smss.exe',
    'system', 'system.exe',
    'dwm', 'dwm.exe',
    'taskhostw', 'taskhostw.exe',
    'sihost', 'sihost.exe',
    'fontdrvhost', 'fontdrvhost.exe',
    'usermanager', 'usermanager.exe',
}

# Blocked command patterns for Start-Process
BLOCKED_COMMAND_PATTERNS = [
    '& ', '| ', '; ', '`', '$(', '${',
    'rm ', 'del ', 'format', 'shutdown', 'reboot',
    'mklink', 'icacls', 'reg delete', 'reg add',
]


def _validate_string(value, field_name="input"):
    """Validate that a string doesn't contain shell injection characters."""
    if not value:
        return True
    if DANGEROUS_CHARS_PATTERN.search(value):
        raise ValueError(
            f"ERROR: {field_name} contains forbidden shell characters. "
            f"Only alphanumeric, spaces, dots, hyphens, underscores, "
            f"slashes, backslashes, colons are allowed."
        )
    return True


def _sanitize_ps_string(value):
    """
    Sanitize a string for safe embedding in PowerShell single-quoted strings.
    Validates input first, then escapes single quotes.
    """
    if value is None:
        return "''"
    _validate_string(value)
    # In PowerShell single-quoted strings, only ' needs escaping -> ''
    escaped = value.replace("'", "''")
    return f"'{escaped}'"


def _validate_command_path(command):
    """Validate and sanitize a file path/command for Start-Process."""
    if not command:
        raise ValueError("ERROR: Command cannot be empty")
    command = command.strip()
    lower_cmd = command.lower()
    for pattern in BLOCKED_COMMAND_PATTERNS:
        if pattern in lower_cmd:
            raise ValueError(
                f"ERROR: Command blocked - contains dangerous pattern '{pattern}'. "
                f"Use the terminal directly for advanced commands."
            )
    _validate_string(command, "command")
    return command


def list_processes(name=None):
    """List running processes. Optionally filter by name."""
    if name:
        _validate_string(name, "process name")
        escaped = name.replace("'", "''")
        script = f"""
Get-Process -Name '*{escaped}*' -ErrorAction SilentlyContinue |
    Select-Object Id, ProcessName, CPU, WorkingSet64, MainWindowTitle |
    ForEach-Object {{
        [PSCustomObject]@{{
            PID = $_.Id
            Name = $_.ProcessName
            CPU_sec = [math]::Round($_.CPU, 2)
            Memory_MB = [math]::Round($_.WorkingSet64 / 1MB, 2)
            Window = if ($_.MainWindowTitle) {{ $_.MainWindowTitle }} else {{ '' }}
        }}
    }} | ConvertTo-Json -Compress
"""
    else:
        script = r"""
Get-Process | Select-Object Id, ProcessName, CPU, WorkingSet64, MainWindowTitle |
    ForEach-Object {
        [PSCustomObject]@{
            PID = $_.Id
            Name = $_.ProcessName
            CPU_sec = [math]::Round($_.CPU, 2)
            Memory_MB = [math]::Round($_.WorkingSet64 / 1MB, 2)
            Window = if ($_.MainWindowTitle) { $_.MainWindowTitle } else { '' }
        }
    } | ConvertTo-Json -Compress
"""
    stdout, stderr, code = _run_ps(script)
    if not stdout:
        return "[]"
    return stdout


def kill_process(pid=None, name=None, force=False):
    """Kill a process by PID or name. Protected system processes are blocked."""
    flag = "-Force" if force else ""

    if pid:
        try:
            pid_val = int(pid)
            if pid_val < 1 or pid_val > 2147483647:
                return f"ERROR: Invalid PID value: {pid}"
        except (ValueError, TypeError):
            return f"ERROR: PID must be an integer, got: {pid}"

        # Build protected list as PowerShell array string
        protected_items = sorted(PROTECTED_PROCESSES)
        protected_ps_array = ", ".join(f"'{p}'" for p in protected_items)

        script = f"""
$proc = Get-Process -Id {pid_val} -ErrorAction SilentlyContinue
if (-not $proc) {{
    Write-Output "ERROR: Process PID {pid_val} not found or access denied"
    exit 1
}}
$protected = @({protected_ps_array})
$pn = $proc.ProcessName.ToLower()
$pne = $pn + '.exe'
if ($protected -contains $pn -or $protected -contains $pne) {{
    Write-Output "ERROR: Process '$($proc.ProcessName)' (PID {pid_val}) is protected and cannot be killed"
    exit 2
}}
Stop-Process -Id {pid_val} {flag} -ErrorAction SilentlyContinue
if ($?) {{
    Write-Output "OK: Killed process PID {pid_val} ($($proc.ProcessName))"
}} else {{
    Write-Output "ERROR: Could not kill process PID {pid_val}"
}}
"""
    elif name:
        _validate_string(name, "process name")
        name_lower = name.lower().strip()

        # Fast reject from Python-level blacklist
        if name_lower in PROTECTED_PROCESSES or f"{name_lower}.exe" in PROTECTED_PROCESSES:
            return f"ERROR: Process '{name}' is a protected system process and cannot be killed"

        escaped = _sanitize_ps_string(name)
        protected_items = sorted(PROTECTED_PROCESSES)
        protected_ps_array = ", ".join(f"'{p}'" for p in protected_items)

        script = f"""
$procs = Get-Process -Name *{escaped}* -ErrorAction SilentlyContinue
$protected = @({protected_ps_array})
$targets = $procs | Where-Object {{
    $pn2 = $_.ProcessName.ToLower()
    $pne2 = $pn2 + '.exe'
    ($protected -notcontains $pn2) -and ($protected -notcontains $pne2)
}}
if ($targets) {{
    $targetNames = ($targets.ProcessName | Sort-Object -Unique) -join ', '
    $targets | Stop-Process {flag} -ErrorAction SilentlyContinue
    Write-Output "OK: Killed $($targets.Count) process(es): $targetNames"
}} else {{
    if ($procs) {{
        Write-Output "ERROR: All matching processes are protected system processes. No action taken."
    }} else {{
        Write-Output "ERROR: No process found matching '{name}'"
    }}
}}
"""
    else:
        return "ERROR: Provide --pid or --name"

    stdout, stderr, code = _run_ps(script)
    return stdout if stdout else stderr


def start_process(command, working_dir=None, wait=False):
    """Start a new process with validated/sanitized input."""
    # Validate command path (raises ValueError on dangerous input)
    safe_command = _validate_command_path(command)

    # Sanitize for PowerShell using single-quote escaping
    safe_cmd_ps = _sanitize_ps_string(safe_command)

    dir_part = ""
    if working_dir:
        _validate_string(working_dir, "working directory")
        safe_dir = _sanitize_ps_string(working_dir)
        dir_part = f"-WorkingDirectory {safe_dir}"

    wait_part = "-Wait" if wait else ""

    script = f"""
try {{
    Start-Process -FilePath {safe_cmd_ps} {dir_part} {wait_part} -ErrorAction Stop
    Write-Output "OK: Started process"
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    stdout, stderr, code = _run_ps(script)
    return stdout if stdout else stderr


def get_process_info(pid):
    """Get detailed information about a specific process."""
    try:
        pid_val = int(pid)
        if pid_val < 1 or pid_val > 2147483647:
            return f"ERROR: Invalid PID value: {pid}"
    except (ValueError, TypeError):
        return f"ERROR: PID must be an integer, got: {pid}"

    script = f"""
$proc = Get-Process -Id {pid_val} -ErrorAction SilentlyContinue
if ($proc) {{
    [PSCustomObject]@{{
        PID = $proc.Id
        Name = $proc.ProcessName
        Path = $proc.Path
        StartTime = $proc.StartTime
        CPU_sec = [math]::Round($proc.CPU, 2)
        Memory_MB = [math]::Round($proc.WorkingSet64 / 1MB, 2)
        Threads = $proc.Threads.Count
        Handles = $proc.HandleCount
        MainWindowTitle = $proc.MainWindowTitle
        Responding = $proc.Responding
    }} | ConvertTo-Json
}} else {{
    Write-Output "ERROR: Process PID {pid_val} not found"
}}
"""
    stdout, stderr, code = _run_ps(script)
    return stdout if stdout else stderr


def get_system_info():
    """Get overall system resource usage."""
    script = r"""
$os = Get-CimInstance Win32_OperatingSystem
$totalGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
$freeGB = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
$usedGB = [math]::Round($totalGB - $freeGB, 2)
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
$uptime = (Get-Date) - $os.LastBootUpTime
[PSCustomObject]@{
    ComputerName = $env:COMPUTERNAME
    OS = $os.Caption
    CPU_Load_Pct = $cpu.LoadPercentage
    RAM_Total_GB = $totalGB
    RAM_Used_GB = $usedGB
    RAM_Free_GB = $freeGB
    RAM_Usage_Pct = [math]::Round($usedGB / $totalGB * 100, 1)
    Uptime_Days = [math]::Floor($uptime.TotalDays)
    Uptime_Hours = $uptime.Hours
    Process_Count = (Get-Process).Count
} | ConvertTo-Json
"""
    stdout, stderr, code = _run_ps(script)
    return stdout if stdout else stderr


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Process Manager")
    sub = parser.add_subparsers(dest="action")

    p_list = sub.add_parser("list", help="List processes")
    p_list.add_argument("--name", type=str, help="Filter by name")

    p_kill = sub.add_parser("kill", help="Kill a process")
    p_kill.add_argument("--pid", type=int)
    p_kill.add_argument("--name", type=str)
    p_kill.add_argument("--force", action="store_true")

    p_start = sub.add_parser("start", help="Start a process")
    p_start.add_argument("command", type=str)
    p_start.add_argument("--dir", type=str, help="Working directory")
    p_start.add_argument("--wait", action="store_true")

    p_info = sub.add_parser("info", help="Get process details")
    p_info.add_argument("--pid", type=int, required=True)

    p_sys = sub.add_parser("system", help="Get system resource info")

    args = parser.parse_args()

    if args.action == "list":
        print(list_processes(args.name))
    elif args.action == "kill":
        print(kill_process(args.pid, args.name, args.force))
    elif args.action == "start":
        try:
            print(start_process(args.command, args.dir, args.wait))
        except ValueError as e:
            print(str(e))
    elif args.action == "info":
        print(get_process_info(args.pid))
    elif args.action == "system":
        print(get_system_info())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
