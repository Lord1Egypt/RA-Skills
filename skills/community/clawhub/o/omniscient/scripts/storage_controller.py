#!/usr/bin/env python3
"""
Storage Controller - Manage disk drives and storage on Windows.

Capabilities:
  - List all drives with usage info
  - Detailed drive info (filesystem, type, serial)
  - Disk health / SMART status
  - Find largest files on a drive
  - Folder size analysis

Requirements: Windows 10/11, PowerShell 5.1+
Dependencies: psutil (auto-installed)
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


def _validate_drive(drive):
    """Validate drive letter input to prevent command injection."""
    if drive is None:
        return None
    # Only allow single drive letter with optional colon
    if not re.match(r'^[A-Za-z]:?$', drive.strip()):
        return None
    return drive.strip().upper()


def _validate_path(path):
    """Validate path to prevent path traversal attacks."""
    if path is None:
        return None
    resolved = os.path.realpath(os.path.expanduser(path))
    # Reject paths that attempt to traverse above their root or contain suspicious patterns
    normalized = os.path.normpath(path)
    # Reject obviously malicious patterns
    if re.search(r'\.\.[\\/]', normalized) or re.search(r'\.\.$', normalized):
        return None
    return resolved


def _sanitize_ps_string(s):
    """Sanitize a string for safe embedding in PowerShell single-quoted strings."""
    if s is None:
        return None
    # In PowerShell single-quoted strings, only single quote needs escaping (double it)
    return s.replace("'", "''")


def _ensure_psutil():
    try:
        import psutil
        return psutil
    except ImportError:
        import subprocess as sp
        sp.check_call([sys.executable, "-m", "pip", "install", "psutil>=5.9.8,<7", "-q"])
        import psutil
        return psutil


# ========== Drive List ==========

def list_drives():
    """List all drives with usage info."""
    psutil = _ensure_psutil()
    drives = []
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
            drives.append({
                "Drive": part.mountpoint,
                "Filesystem": part.fstype or "Unknown",
                "Type": "Removable" if 'removable' in (part.opts or '').lower() else "Fixed",
                "Total_GB": round(usage.total / (1024**3), 1),
                "Used_GB": round(usage.used / (1024**3), 1),
                "Free_GB": round(usage.free / (1024**3), 1),
                "UsedPercent": round(usage.percent, 1)
            })
        except (PermissionError, OSError):
            drives.append({
                "Drive": part.mountpoint,
                "Filesystem": part.fstype or "Unknown",
                "Type": "Inaccessible",
                "Total_GB": None,
                "Used_GB": None,
                "Free_GB": None,
                "UsedPercent": None
            })
    import json
    return json.dumps(drives, indent=2, ensure_ascii=False)


# ========== Drive Info ==========

def drive_info(drive=None):
    """Get detailed drive information."""
    target = _validate_drive(drive)
    if target is None:
        return 'ERROR: Invalid drive letter. Use format like "C:" or "C"'
    if not target.endswith(':'):
        target += ':'
    safe_target = _sanitize_ps_string(target)
    script = f"""
try {{
    $disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='{safe_target}'" -ErrorAction Stop
    if (-not $disk) {{
        # Try physical disk
        $phys = Get-CimInstance Win32_DiskDrive | Where-Object {{ $_.DeviceID -like '%{safe_target.rstrip(":")}%' -or $_.MediaType -like '%Fixed%' }} | Select-Object -First 1
        if ($phys) {{
            [PSCustomObject]@{{
                Device = $phys.DeviceID
                Model = $phys.Model
                Serial = $phys.SerialNumber
                Size_GB = [math]::Round($phys.Size / 1GB, 1)
                MediaType = $phys.MediaType
                InterfaceType = $phys.InterfaceType
                Status = $phys.Status
                Partitions = $phys.Partitions
            }} | ConvertTo-Json
            return
        }}
        Write-Output '{{"Error":"Drive {safe_target} not found"}}'
        return
    }}
    [PSCustomObject]@{{
        DeviceID = $disk.DeviceID
        FileSystem = $disk.FileSystem
        VolumeName = $disk.VolumeName
        TotalSize_GB = [math]::Round($disk.Size / 1GB, 1)
        FreeSpace_GB = [math]::Round($disk.FreeSpace / 1GB, 1)
        DriveType = switch ($disk.DriveType) {{ 2 {{ 'Removable' }} 3 {{ 'Local Disk' }} 4 {{ 'Network' }} 5 {{ 'CD-ROM' }} default {{ "Unknown($($disk.DriveType))" }} }}
        VolumeSerialNumber = $disk.VolumeSerialNumber
        Compressed = $disk.Compressed
        SupportsFileCompression = $disk.SupportsFileCompression
    }} | ConvertTo-Json
}} catch {{
    Write-Output "{{\"Error\":\"$($_.Exception.Message)\"}}"
}}
"""
    stdout, _, _ = _run_ps(script, timeout=15)
    return stdout


# ========== Disk Health (SMART) ==========

def disk_health(drive=None):
    """Get disk health / SMART status."""
    target = drive or "C:"
    script = f"""
try {{
    # Try Win32_DiskDrive status
    $drives = Get-CimInstance Win32_DiskDrive
    $result = @()
    foreach ($d in $drives) {{
        $info = @{{
            Device = $d.DeviceID
            Model = $d.Model
            Status = $d.Status
            StatusInfo = if ($d.StatusInfo) {{ $d.StatusInfo }} else {{ 'N/A' }}
            LastErrorCode = if ($d.LastErrorCode) {{ $d.LastErrorCode }} else {{ 'OK' }}
            NeedsCleaning = $d.NeedsCleaning
        }}
        # Try to get media type and size
        $info.Size_GB = [math]::Round($d.Size / 1GB, 1)
        $info.MediaType = $d.MediaType
        $info.InterfaceType = $d.InterfaceType
        $result += [PSCustomObject]$info
    }}
    $result | ConvertTo-Json -Compress
}} catch {{
    Write-Output '{{"Error":"Could not read disk health information"}}'
}}
"""
    stdout, _, _ = _run_ps(script, timeout=15)
    return stdout


# ========== Big Files ==========

def big_files(drive=None, top=20):
    """Find the largest files on a drive."""
    target = _validate_drive(drive)
    if target is None:
        return 'ERROR: Invalid drive letter. Use format like "C:" or "C"'
    if not target.endswith(':'):
        target += ':'
    safe_target = _sanitize_ps_string(target)
    count = min(max(int(top), 1), 100)
    script = f"""
try {{
    Get-ChildItem -Path '{safe_target}\\' -Recurse -File -ErrorAction SilentlyContinue |
        Sort-Object Length -Descending |
        Select-Object -First {count} |
        ForEach-Object {{
            [PSCustomObject]@{{
                File = $_.FullName
                Size_MB = [math]::Round($_.Length / 1MB, 1)
                Extension = $_.Extension
                LastModified = $_.LastWriteTime.ToString('yyyy-MM-dd HH:mm')
            }}
        }} | ConvertTo-Json -Compress
}} catch {{
    Write-Output '{{"Error":"$($_.Exception.Message)"}}'
}}
"""
    stdout, _, _ = _run_ps(script, timeout=120)
    return stdout


# ========== Folder Usage ==========

def folder_usage(path=None, top=10):
    """Analyze folder sizes under a given path."""
    target = _validate_path(path)
    if target is None and path is not None:
        return 'ERROR: Invalid path (contains path traversal or does not exist)'
    if target is None:
        target = os.path.realpath(os.path.expanduser("~"))
    if not os.path.isdir(target):
        return f'ERROR: Path "{target}" does not exist or is not a directory'
    safe_target = _sanitize_ps_string(target)
    script = f"""
try {{
    Get-ChildItem -Path '{safe_target}' -Directory -ErrorAction SilentlyContinue |
        ForEach-Object {{
            $size = (Get-ChildItem -Path $_.FullName -Recurse -File -ErrorAction SilentlyContinue |
                Measure-Object -Property Length -Sum).Sum
            [PSCustomObject]@{{
                Folder = $_.Name
                FullPath = $_.FullName
                Size_MB = [math]::Round($size / 1MB, 1)
                Size_GB = [math]::Round($size / 1GB, 2)
                Files = (Get-ChildItem -Path $_.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
            }}
        }} | Sort-Object Size_MB -Descending |
        Select-Object -First {top} |
        ConvertTo-Json -Compress
}} catch {{
    Write-Output '{{"Error":"$($_.Exception.Message)"}}'
}}
"""
    stdout, _, _ = _run_ps(script, timeout=120)
    return stdout


# ========== Disk Partitions ==========

def partitions():
    """List all disk partitions with physical disk mapping."""
    script = r"""
try {
    $disks = Get-CimInstance Win32_DiskDrive
    foreach ($disk in $disks) {
        $parts = Get-CimInstance Win32_DiskPartition | Where-Object { $_.DiskIndex -eq $disk.Index }
        foreach ($part in $parts) {
            $logical = Get-CimInstance Win32_LogicalDiskToPartition | Where-Object { $_.Antecedent -eq $part.__PATH }
            $driveLetter = if ($logical) { 
                ($logical.Dependent | ForEach-Object { 
                    (Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='$(($_ -split '"')[1])'").DeviceID 
                }) -join ', '
            } else { 'None' }
            [PSCustomObject]@{
                Disk = $disk.DeviceID
                Model = $disk.Model
                PartitionNumber = $part.PartitionNumber
                Type = $part.Type
                Size_GB = [math]::Round($part.Size / 1GB, 1)
                Bootable = $part.Bootable
                DriveLetter = $driveLetter
            }
        }
    } | ConvertTo-Json -Compress
} catch {
    Write-Output '{"Error":"Could not enumerate partitions"}'
}
"""
    stdout, _, _ = _run_ps(script, timeout=20)
    return stdout


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Storage Controller")
    sub = parser.add_subparsers(dest="command")

    # list
    sub.add_parser("list", help="List all drives with usage")

    # info
    p_info = sub.add_parser("info", help="Drive details")
    p_info.add_argument("--drive", type=str, help="Drive letter (e.g. C:)")

    # health
    p_health = sub.add_parser("health", help="Disk health/SMART status")
    p_health.add_argument("--drive", type=str, help="Drive letter")

    # big-files
    p_big = sub.add_parser("big-files", help="Find largest files")
    p_big.add_argument("--drive", type=str, help="Drive letter")
    p_big.add_argument("--top", type=int, default=20, help="Number of results (max 100)")

    # usage
    p_usage = sub.add_parser("usage", help="Folder size analysis")
    p_usage.add_argument("--path", type=str, help="Path to analyze")
    p_usage.add_argument("--top", type=int, default=10, help="Number of folders")

    # partitions
    sub.add_parser("partitions", help="List disk partitions")

    args = parser.parse_args()

    if args.command == "list":
        print(list_drives())
    elif args.command == "info":
        print(drive_info(args.drive))
    elif args.command == "health":
        print(disk_health(args.drive))
    elif args.command == "big-files":
        print(big_files(args.drive, args.top))
    elif args.command == "usage":
        print(folder_usage(args.path, args.top))
    elif args.command == "partitions":
        print(partitions())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
