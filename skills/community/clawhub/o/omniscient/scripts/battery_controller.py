#!/usr/bin/env python3
"""
Battery & Power Plan Controller - Monitor battery and manage power plans on Windows.

Capabilities:
  - Battery status (percentage, charging state, health)
  - List available power plans
  - Switch power plans
  - Generate battery report

Requirements: Windows 10/11, PowerShell 5.1+
Dependencies: None (uses Windows built-in powercfg)
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


def _escape_ps_regex(s):
    """Escape a string for safe use inside a PowerShell -match regex operand."""
    # PowerShell -match uses .NET regex; escape all special chars
    if s is None:
        return None
    return re.sub(r'[.*+?^${}()|[\]\\]', r'\\\g<0>', s)


def _ensure_psutil():
    try:
        import psutil
        return psutil
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil>=5.9.8,<7", "-q"])
        import psutil
        return psutil


# ========== Battery Status ==========

def battery_status():
    """Get battery status using psutil + WMI."""
    psutil = _ensure_psutil()
    bat = psutil.sensors_battery()
    if bat is None:
        # No battery detected, try WMI for more info
        script = r"""
try {
    $batt = Get-CimInstance Win32_Battery -ErrorAction Stop
    [PSCustomObject]@{
        Status = if ($batt.BatteryStatus -eq 2) { 'Charging' }
                 elseif ($batt.BatteryStatus -eq 1) { 'Discharging' }
                 elseif ($batt.BatteryStatus -eq 3) { 'Fully Charged' }
                 else { "Other($($batt.BatteryStatus))" }
        EstimatedChargeRemaining = $batt.EstimatedChargeRemaining
        EstimatedRunTime = $batt.EstimatedRunTime
        DesignCapacity = $batt.DesignCapacity
        FullChargeCapacity = $batt.FullChargeCapacity
        HealthPercent = if ($batt.DesignCapacity -gt 0) { [math]::Round($batt.FullChargeCapacity / $batt.DesignCapacity * 100, 1) } else { $null }
        Name = $batt.Name
        Chemistry = $batt.Chemistry
    } | ConvertTo-Json
} catch {
    Write-Output '{"Error":"No battery detected on this system"}'
}
"""
        stdout, _, _ = _run_ps(script, timeout=10)
        return stdout

    secs_left = bat.secsleft if bat.secsleft >= 0 else None
    result = {
        "Percent": bat.percent,
        "Plugged": bat.power_plugged,
        "Status": "Charging" if bat.power_plugged else ("Discharging" if secs_left else "Full"),
    }
    if secs_left is not None:
        hours, remainder = divmod(secs_left, 3600)
        minutes, _ = divmod(remainder, 60)
        result["TimeRemaining"] = f"{hours}h {minutes}m"

    # Get additional WMI info
    script = r"""
try {
    $batt = Get-CimInstance Win32_Battery -ErrorAction Stop
    [PSCustomObject]@{
        DesignCapacity = $batt.DesignCapacity
        FullChargeCapacity = $batt.FullChargeCapacity
        HealthPercent = if ($batt.DesignCapacity -gt 0) { [math]::Round($batt.FullChargeCapacity / $batt.DesignCapacity * 100, 1) } else { $null }
        Name = $batt.Name
        Chemistry = $batt.Chemistry
    } | ConvertTo-Json -Compress
} catch { Write-Output '{}' }
"""
    stdout, _, _ = _run_ps(script, timeout=10)
    if stdout and stdout != '{}':
        try:
            import json
            extra = json.loads(stdout)
            result.update(extra)
        except Exception:
            pass

    import json
    return json.dumps(result, indent=2, ensure_ascii=False)


# ========== Battery History ==========

def battery_history():
    """Get battery charge/discharge history and health details."""
    script = r"""
try {
    $batt = Get-CimInstance Win32_Battery -ErrorAction Stop
    [PSCustomObject]@{
        Name = $batt.Name
        Status = switch ($batt.BatteryStatus) { 1 { 'Discharging' } 2 { 'AC Power' } 3 { 'Fully Charged' } default { "Other($($batt.BatteryStatus))" } }
        ChargeRemaining = "$($batt.EstimatedChargeRemaining)%"
        DesignVoltage_mV = $batt.DesignVoltage
        CurrentVoltage_mV = if ($batt.DesignVoltage) { $batt.DesignVoltage } else { $null }
        DesignCapacity_mWh = $batt.DesignCapacity
        FullChargeCapacity_mWh = $batt.FullChargeCapacity
        Degradation = if ($batt.DesignCapacity -gt 0) { [math]::Round((1 - $batt.FullChargeCapacity / $batt.DesignCapacity) * 100, 1) } else { $null }
    } | ConvertTo-Json
} catch {
    Write-Output '{"Error":"Battery information unavailable"}'
}
"""
    stdout, _, _ = _run_ps(script, timeout=10)
    return stdout


# ========== Power Plans ==========

def list_plans():
    """List all available power plans."""
    script = r"""
try {
    $plans = powercfg /list 2>&1
    $results = @()
    foreach ($line in $plans) {
        if ($line -match 'GUID:\s*([0-9a-f-]+)\s+\((.+?)\)\s*\*?(.*)$') {
            $results += [PSCustomObject]@{
                GUID = $matches[1]
                Name = $matches[2]
                Active = if ($matches[3].Trim() -eq '*') { $true } else { $false }
            }
        }
    }
    if ($results.Count -eq 0) {
        Write-Output $plans
    } else {
        $results | ConvertTo-Json -Compress
    }
} catch {
    Write-Output '{"Error":"Could not list power plans"}'
}
"""
    stdout, _, _ = _run_ps(script, timeout=10)
    return stdout


def current_plan():
    """Get the currently active power plan."""
    script = r"""
try {
    $active = powercfg /getactivescheme 2>&1
    if ($active -match 'GUID:\s*([0-9a-f-]+)\s+\((.+?)\)') {
        [PSCustomObject]@{
            GUID = $matches[1]
            Name = $matches[2]
        } | ConvertTo-Json
    } else {
        Write-Output $active
    }
} catch {
    Write-Output '{"Error":"Could not get active power plan"}'
}
"""
    stdout, _, _ = _run_ps(script, timeout=10)
    return stdout


def set_plan(name):
    """Switch to a power plan by name."""
    # Escape for PowerShell single-quoted strings
    escaped = name.replace("'", "''")
    # Escape for PowerShell regex operands (-match)
    regex_safe = _escape_ps_regex(name)
    script = f"""
try {{
    $plan = powercfg /list 2>&1 | Where-Object {{ $_ -match '\({regex_safe}\)' }}
    if (-not $plan) {{
        # Try partial match
        $plan = powercfg /list 2>&1 | Where-Object {{ $_ -match '{regex_safe}' }}
    }}
    if ($plan -and $plan -match 'GUID:\s*([0-9a-f-]+)') {{
        $guid = $matches[1]
        powercfg /setactive $guid 2>&1 | Out-Null
        Write-Output "OK: Power plan switched to '{escaped}' ($guid)"
    }} else {{
        # List available plans for guidance
        $available = (powercfg /list 2>&1) -join "`n"
        Write-Output "ERROR: Power plan '{escaped}' not found.`nAvailable plans:`n$available"
    }}
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    stdout, _, _ = _run_ps(script, timeout=10)
    return stdout


# ========== Battery Report ==========

def battery_report(output_path=None):
    """Generate a detailed battery report."""
    if output_path is None:
        output_path = os.path.join(os.path.expanduser("~"), "battery-report.html")
    else:
        # Validate path: reject traversal, restrict to user directories
        resolved = os.path.realpath(os.path.expanduser(output_path))
        if '..' in os.path.normpath(output_path).replace(os.sep, '/').split('/'):
            return 'ERROR: Output path contains path traversal (..)'
        home = os.path.realpath(os.path.expanduser("~"))
        temp = os.path.realpath(os.environ.get('TEMP', os.environ.get('TMP', '')))
        cwd = os.path.realpath(os.getcwd())
        allowed = (resolved.startswith(home + os.sep) or resolved == home or
                   (temp and (resolved.startswith(temp + os.sep) or resolved == temp)) or
                   resolved.startswith(cwd + os.sep) or resolved == cwd)
        if not allowed:
            return 'ERROR: Output path is not allowed. Files can only be saved to user directories (Home, Temp, CWD).'
        output_path = resolved
    # Escape for PowerShell single-quoted string
    safe_path = output_path.replace("'", "''")
    script = f"""
try {{
    powercfg /batteryreport /output '{safe_path}' 2>&1 | Out-Null
    if (Test-Path '{safe_path}') {{
        Write-Output "OK: Battery report saved to '{safe_path}'"
    }} else {{
        Write-Output "ERROR: Failed to generate battery report"
    }}
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    stdout, _, _ = _run_ps(script, timeout=15)
    return stdout


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Battery & Power Plan Controller")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="Battery status")
    sub.add_parser("history", help="Battery health history")

    sub.add_parser("plans", help="List power plans")
    sub.add_parser("current", help="Current active plan")

    p_set = sub.add_parser("set-plan", help="Switch power plan")
    p_set.add_argument("--name", type=str, required=True, help="Plan name (supports partial match)")

    p_report = sub.add_parser("report", help="Generate battery report HTML")
    p_report.add_argument("--output", type=str, help="Output file path")

    args = parser.parse_args()

    if args.command == "status":
        print(battery_status())
    elif args.command == "history":
        print(battery_history())
    elif args.command == "plans":
        print(list_plans())
    elif args.command == "current":
        print(current_plan())
    elif args.command == "set-plan":
        print(set_plan(args.name))
    elif args.command == "report":
        print(battery_report(args.output))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
