#!/usr/bin/env python3
"""
Scanner Controller - Enumerate and manage scanner devices on Windows.

Capabilities:
  - List scanner devices (WIA / WSD)
  - Scanner device info (name, type, status, driver)
  - Check scanner availability

Requirements: Windows 10/11, PowerShell 5.1+
Dependencies: None (uses Windows WIA/WSD built-in support)
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


def list_scanners():
    """List all scanner devices on the system."""
    script = r"""
try {
    # Method 1: WIA Device Manager (COM object)
    $wiaDevices = @()
    try {
        $wiaManager = New-Object -ComObject WIA.DeviceManager -ErrorAction Stop
        foreach ($devInfo in $wiaManager.DeviceInfos) {
            $wiaDevices += [PSCustomObject]@{
                Name = $devInfo.Properties("Name").Value
                Type = $devInfo.Type
                DeviceID = $devInfo.DeviceID
                Source = "WIA"
            }
        }
    } catch {
        # WIA COM not available or no devices
    }

    # Method 2: Check WSD (Web Services for Devices) scanners
    $wsdScanners = @()
    try {
        $wsdScanners = Get-ChildItem "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WSD\Scanners" -ErrorAction SilentlyContinue |
            ForEach-Object {
                $props = Get-ItemProperty $_.PSPath -ErrorAction SilentlyContinue
                [PSCustomObject]@{
                    Name = if ($props.FriendlyName) { $props.FriendlyName } else { $_.PSChildName }
                    Type = "WSD"
                    DeviceID = $_.PSChildName
                    Source = "WSD"
                }
            }
    } catch {}

    # Method 3: PnP image devices
    $pnpScanners = @()
    try {
        $pnpScanners = Get-PnpDevice -PresentOnly -ErrorAction SilentlyContinue |
            Where-Object {
                $_.Class -eq 'Image' -and $_.Status -eq 'OK'
            }
    } catch {}

    $results = @()

    foreach ($d in $wiaDevices) {
        $results += [PSCustomObject]@{
            Name = $d.Name
            Type = switch ($d.Type) { 1 { "Scanner" } 2 { "Camera" } default { "Unknown($($d.Type))" } }
            Status = "Available"
            Source = $d.Source
            DeviceID = $d.DeviceID
        }
    }

    foreach ($d in $wsdScanners) {
        if (-not ($results | Where-Object { $_.DeviceID -eq $d.DeviceID })) {
            $results += [PSCustomObject]@{
                Name = $d.Name
                Type = "Scanner"
                Status = "Available"
                Source = $d.Source
                DeviceID = $d.DeviceID
            }
        }
    }

    foreach ($d in $pnpScanners) {
        if (-not ($results | Where-Object { $_.DeviceID -like "*$($d.InstanceId)*" })) {
            $results += [PSCustomObject]@{
                Name = $d.FriendlyName
                Type = "Image Device"
                Status = $d.Status
                Source = "PnP"
                DeviceID = $d.InstanceId
            }
        }
    }

    if ($results.Count -eq 0) {
        Write-Output '{"Note":"No scanner devices found"}'
    } else {
        $results | ConvertTo-Json -Compress
    }
} catch {
    Write-Output '{"Error":"Could not enumerate scanner devices"}'
}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def scanner_info():
    """Get detailed information about the first available scanner."""
    script = r"""
try {
    $wiaManager = New-Object -ComObject WIA.DeviceManager -ErrorAction Stop
    $devices = @()
    foreach ($devInfo in $wiaManager.DeviceInfos) {
        $dev = $devInfo.Connect()
        $devices += [PSCustomObject]@{
            Name = $devInfo.Properties("Name").Value
            Type = switch ($devInfo.Type) { 1 { "Scanner" } 2 { "Camera" } default { "Unknown" } }
            DeviceID = $devInfo.DeviceID
            Manufacturer = $dev.Properties("Manufacturer").Value
            Description = $dev.Properties("Description").Value
            Port = $dev.Properties("Port").Value
            PropertyCount = $dev.Properties.Count
        }
    }
    if ($devices.Count -eq 0) {
        Write-Output '{"Note":"No WIA scanner devices available for detailed info"}'
    } else {
        $devices | ConvertTo-Json -Compress
    }
} catch {
    Write-Output '{"Error":"Could not retrieve scanner info. WIA may not be available."}'
}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def check_wia():
    """Check if WIA (Windows Image Acquisition) service is available."""
    script = r"""
try {
    $svc = Get-Service -Name 'stisvc' -ErrorAction Stop
    [PSCustomObject]@{
        WIADisplayName = $svc.DisplayName
        Status = $svc.Status.ToString()
        StartType = $svc.StartType.ToString()
        Available = ($svc.Status -eq 'Running')
    } | ConvertTo-Json
} catch {
    Write-Output '{"WIA":"Not available","Status":"Service not found"}'
}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Scanner Controller")
    sub = parser.add_subparsers(dest="action")

    sub.add_parser("list", help="List scanner devices")
    sub.add_parser("info", help="Detailed scanner info (WIA)")
    sub.add_parser("wia", help="Check WIA service status")

    args = parser.parse_args()

    if args.action == "list":
        print(list_scanners())
    elif args.action == "info":
        print(scanner_info())
    elif args.action == "wia":
        print(check_wia())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
