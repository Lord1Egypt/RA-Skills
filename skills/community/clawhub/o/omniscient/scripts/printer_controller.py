#!/usr/bin/env python3
"""
Printer Controller - Manage printers and print jobs on Windows.

Capabilities:
  - List all printers
  - Get/set default printer
  - List print jobs
  - Cancel print jobs
  - Printer status and capabilities

Requirements: Windows 10/11, PowerShell 5.1+
Dependencies: None (uses Windows built-in print commands)
"""

import subprocess
import sys
import os

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run_ps as _run_ps


# ========== List Printers ==========

def list_printers():
    """List all installed printers with status."""
    script = r"""
try {
    Get-CimInstance Win32_Printer | ForEach-Object {
        $isDefault = $_.Default
        [PSCustomObject]@{
            Name = $_.Name
            ShareName = if ($_.ShareName) { $_.ShareName } else { $null }
            PortName = $_.PortName
            DriverName = $_.DriverName
            Status = $_.PrinterStatus
            StatusText = switch ($_.PrinterStatus) {
                0 { 'Other' } 1 { 'Unknown' } 2 { 'Idle' } 3 { 'Printing' }
                4 { 'Warmup' } 5 { 'Stopped' } 6 { 'Offline' }
                default { "Status($($_.PrinterStatus))" }
            }
            IsDefault = [bool]$isDefault
            IsNetwork = $_.Network
            IsShared = [bool]$_.Shared
            Location = if ($_.Location) { $_.Location } else { $null }
            Comment = if ($_.Comment) { $_.Comment } else { $null }
        }
    } | ConvertTo-Json -Compress
} catch {
    Write-Output '{"Error":"Could not enumerate printers"}'
}
"""
    stdout, _, _ = _run_ps(script, timeout=15)
    return stdout


# ========== Default Printer ==========

def get_default_printer():
    """Get the current default printer."""
    script = r"""
try {
    $default = Get-CimInstance Win32_Printer -Filter "Default=True" -ErrorAction Stop
    if ($default) {
        [PSCustomObject]@{
            Name = $default.Name
            PortName = $default.PortName
            DriverName = $default.DriverName
            Status = $default.PrinterStatus
        } | ConvertTo-Json
    } else {
        Write-Output '{"Warning":"No default printer set"}'
    }
} catch {
    Write-Output '{"Error":"Could not get default printer"}'
}
"""
    stdout, _, _ = _run_ps(script, timeout=10)
    return stdout


def set_default_printer(name):
    """Set the default printer."""
    escaped = name.replace("'", "''")
    script = f"""
try {{
    $printer = Get-CimInstance Win32_Printer -Filter "Name='{escaped}'" -ErrorAction Stop
    if (-not $printer) {{
        $printer = Get-CimInstance Win32_Printer | Where-Object {{ $_.Name -like '*{escaped}*' }} | Select-Object -First 1
    }}
    if ($printer) {{
        $printer.SetDefaultPrinter() | Out-Null
        Write-Output "OK: Default printer set to '$($printer.Name)'"
    }} else {{
        $all = (Get-CimInstance Win32_Printer | Select-Object -ExpandProperty Name) -join "`n  "
        Write-Output "ERROR: Printer '{name}' not found.`nAvailable printers:`n  $all"
    }}
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    stdout, _, _ = _run_ps(script, timeout=10)
    return stdout


# ========== Print Jobs ==========

def list_jobs(printer_name=None):
    """List all print jobs, optionally filtered by printer."""
    filter_clause = ""
    if printer_name:
        escaped = printer_name.replace("'", "''")
        filter_clause = f"-Filter \"Name='{escaped}'\""

    script = f"""
try {{
    $printers = Get-CimInstance Win32_Printer {filter_clause} -ErrorAction Stop
    $allJobs = @()
    foreach ($p in $printers) {{
        $jobs = Get-CimInstance Win32_PrintJob -Filter "Name LIKE '$($p.Name)%'" -ErrorAction SilentlyContinue
        foreach ($j in $jobs) {{
            $allJobs += [PSCustomObject]@{{
                Printer = $p.Name
                JobID = $j.JobId
                Document = $j.Document
                Status = $j.JobStatus
                Owner = $j.Owner
                Size_KB = [math]::Round($j.Size / 1KB, 1)
                Pages = $j.TotalPages
                Submitted = $j.TimeSubmitted
            }}
        }}
    }}
    if ($allJobs.Count -eq 0) {{
        Write-Output '{{"Note":"No active print jobs"}}'
    }} else {{
        $allJobs | ConvertTo-Json -Compress
    }}
}} catch {{
    Write-Output '{{"Error":"Could not list print jobs"}}'
}}
"""
    stdout, _, _ = _run_ps(script, timeout=10)
    return stdout


# ========== Cancel Jobs ==========

def cancel_job(job_id=None, printer_name=None):
    """Cancel a specific print job or all jobs on a printer."""
    if job_id is not None:
        script = f"""
try {{
    $job = Get-CimInstance Win32_PrintJob -Filter "JobId={int(job_id)}" -ErrorAction Stop
    if ($job) {{
        $job.Cancel() | Out-Null
        Write-Output "OK: Print job {int(job_id)} ('{job.Document}') cancelled"
    }} else {{
        Write-Output "ERROR: Print job {int(job_id)} not found"
    }}
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    elif printer_name:
        escaped = printer_name.replace("'", "''")
        script = f"""
try {{
    $jobs = Get-CimInstance Win32_PrintJob -Filter "Name LIKE '%{escaped}%'" -ErrorAction Stop
    $count = 0
    foreach ($j in $jobs) {{
        $j.Cancel() | Out-Null
        $count++
    }}
    if ($count -gt 0) {{
        Write-Output "OK: Cancelled $count print job(s) on '{printer_name}'"
    }} else {{
        Write-Output "INFO: No active jobs found on '{printer_name}'"
    }}
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    else:
        return "ERROR: Specify --job-id or --printer"

    stdout, _, _ = _run_ps(script, timeout=10)
    return stdout


# ========== Printer Capabilities ==========

def printer_capabilities(printer_name=None):
    """Get printer capabilities (paper sizes, resolution, etc.)."""
    if printer_name:
        escaped = printer_name.replace("'", "''")
        filter_clause = f"-Filter \"Name='{escaped}'\""
    else:
        filter_clause = "-Filter \"Default=True\""

    script = f"""
try {{
    $printer = Get-CimInstance Win32_Printer {filter_clause} -ErrorAction Stop | Select-Object -First 1
    [PSCustomObject]@{{
        Name = $printer.Name
        DriverName = $printer.DriverName
        PortName = $printer.PortName
        PaperSize = $printer.PaperSize
        PaperLength = $printer.PaperLength
        PaperWidth = $printer.PaperWidth
        PrintQuality = switch ($printer.PrintQuality) {{
            -1 {{ 'Draft' }} -2 {{ 'Low' }} -3 {{ 'Medium' }} -4 {{ 'High' }}
            -5 {{ 'Normal' }} default {{ $printer.PrintQuality }}
        }}
        Color = $printer.Color
        Duplex = $printer.Duplex
        Collate = $printer.Collate
        Orientation = $printer.Orientation
        Copies = $printer.Copies
        HorizontalResolution = $printer.HorizontalResolution
        VerticalResolution = $printer.VerticalResolution
    }} | ConvertTo-Json
}} catch {{
    Write-Output '{{"Error":"Could not get printer capabilities. Specify a printer name if no default is set."}}'
}}
"""
    stdout, _, _ = _run_ps(script, timeout=10)
    return stdout


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Printer Controller")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List all printers")
    sub.add_parser("default", help="Get default printer")

    p_set = sub.add_parser("set-default", help="Set default printer")
    p_set.add_argument("--name", type=str, required=True, help="Printer name (supports partial match)")

    p_jobs = sub.add_parser("jobs", help="List print jobs")
    p_jobs.add_argument("--printer", type=str, help="Filter by printer name")

    p_cancel = sub.add_parser("cancel", help="Cancel print job(s)")
    p_cancel.add_argument("--job-id", type=int, help="Specific job ID")
    p_cancel.add_argument("--printer", type=str, help="Cancel all jobs on a printer")

    p_caps = sub.add_parser("capabilities", help="Printer capabilities")
    p_caps.add_argument("--printer", type=str, help="Printer name (default: default printer)")

    args = parser.parse_args()

    if args.command == "list":
        print(list_printers())
    elif args.command == "default":
        print(get_default_printer())
    elif args.command == "set-default":
        print(set_default_printer(args.name))
    elif args.command == "jobs":
        print(list_jobs(args.printer))
    elif args.command == "cancel":
        print(cancel_job(args.job_id, args.printer))
    elif args.command == "capabilities":
        print(printer_capabilities(args.printer))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
