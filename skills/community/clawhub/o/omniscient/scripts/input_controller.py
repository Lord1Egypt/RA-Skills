#!/usr/bin/env python3
"""
Input Controller - Enumerate keyboard, mouse, and gamepad devices.

Capabilities:
  - List keyboards (name, status, connectivity)
  - List mice/pointing devices (name, status, buttons, DPI if available)
  - List gamepads (name, status, connected via XInput)
  - List all input devices in one view

Requirements: Windows 10/11, PowerShell 5.1+
Dependencies: None (gamepads use WMI/PnP; no XInput library needed)
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


# ========== Keyboards ==========

def list_keyboards():
    """List all keyboard devices."""
    script = r"""
$devices = Get-WmiObject Win32_Keyboard 2>$null
if ($devices) {
    $devices | ForEach-Object {
        [PSCustomObject]@{
            Name = $_.Name
            Status = $_.Status
            Layout = $_.Layout
            NumberOfFunctionKeys = $_.NumberOfFunctionKeys
            DeviceID = $_.DeviceID
        }
    } | ConvertTo-Json -Compress
} else {
    # Fallback: use PnP devices
    Get-PnpDevice -Class Keyboard -PresentOnly -ErrorAction SilentlyContinue |
        Where-Object { $_.Status -eq 'OK' } |
        Select-Object FriendlyName, Status, InstanceId |
        ForEach-Object {
            [PSCustomObject]@{
                Name = $_.FriendlyName
                Status = $_.Status
                Layout = "N/A"
                NumberOfFunctionKeys = "N/A"
                DeviceID = $_.InstanceId
            }
        } | ConvertTo-Json -Compress
}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


# ========== Mice / Pointing Devices ==========

def list_mice():
    """List all mouse/pointing devices."""
    script = r"""
$devices = Get-WmiObject Win32_PointingDevice 2>$null
if ($devices) {
    $devices | ForEach-Object {
        [PSCustomObject]@{
            Name = $_.Name
            Status = $_.Status
            DeviceType = $_.DeviceInterface
            Buttons = $_.NumberOfButtons
            HardwareType = $_.HardwareType
            DeviceID = $_.DeviceID
        }
    } | ConvertTo-Json -Compress
} else {
    Get-PnpDevice -Class Mouse -PresentOnly -ErrorAction SilentlyContinue |
        Where-Object { $_.Status -eq 'OK' } |
        Select-Object FriendlyName, Status, InstanceId |
        ForEach-Object {
            [PSCustomObject]@{
                Name = $_.FriendlyName
                Status = $_.Status
                DeviceType = "N/A"
                Buttons = "N/A"
                HardwareType = "N/A"
                DeviceID = $_.InstanceId
            }
        } | ConvertTo-Json -Compress
}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


# ========== Gamepads ==========

def list_gamepads():
    """List connected game controllers/gamepads."""
    script = r"""
try {
    # Method 1: PnP HID game controllers
    $hidDevices = Get-PnpDevice -PresentOnly -ErrorAction SilentlyContinue |
        Where-Object { $_.Class -eq 'HIDClass' -and $_.InstanceId -match 'IG_' } |
        Select-Object FriendlyName, Status, InstanceId

    # Method 2: XInput check via WMI
    $xinputDevices = Get-WmiObject Win32_PnPEntity 2>$null |
        Where-Object { $_.Name -match 'Xbox|XInput|Gamepad|Controller|Joystick|Game.*Controller' } |
        Select-Object Name, Status, DeviceID

    $results = @()

    if ($xinputDevices) {
        foreach ($d in $xinputDevices) {
            $results += [PSCustomObject]@{
                Name = $d.Name
                Status = $d.Status
                Type = "Game Controller"
                Source = "XInput/WMI"
                DeviceID = $d.DeviceID
            }
        }
    }

    if ($hidDevices) {
        foreach ($d in $hidDevices) {
            # Avoid duplicates with XInput results
            if (-not ($results | Where-Object { $_.DeviceID -eq $d.InstanceId })) {
                $results += [PSCustomObject]@{
                    Name = $d.FriendlyName
                    Status = $d.Status
                    Type = "HID Game Controller"
                    Source = "PnP"
                    DeviceID = $d.InstanceId
                }
            }
        }
    }

    if ($results.Count -eq 0) {
        Write-Output '{"Note":"No game controllers detected"}'
    } else {
        $results | ConvertTo-Json -Compress
    }
} catch {
    Write-Output '{"Error":"Could not enumerate game controllers"}'
}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


# ========== All Input Devices ==========

def list_all():
    """List all input devices (keyboards + mice + gamepads) in one view."""
    script = r"""
try {
    $keyboards = Get-WmiObject Win32_Keyboard 2>$null |
        ForEach-Object { [PSCustomObject]@{ Type = "Keyboard"; Name = $_.Name; Status = $_.Status } }

    $mice = Get-WmiObject Win32_PointingDevice 2>$null |
        ForEach-Object { [PSCustomObject]@{ Type = "Mouse"; Name = $_.Name; Status = $_.Status } }

    $gamepads = Get-WmiObject Win32_PnPEntity 2>$null |
        Where-Object { $_.Name -match 'Xbox|XInput|Gamepad|Controller|Joystick' } |
        ForEach-Object { [PSCustomObject]@{ Type = "Gamepad"; Name = $_.Name; Status = $_.Status } }

    $all = @()
    if ($keyboards) { $all += $keyboards }
    if ($mice) { $all += $mice }
    if ($gamepads) { $all += $gamepads }

    if ($all.Count -eq 0) {
        Write-Output '{"Note":"No input devices found"}'
    } else {
        $all | ConvertTo-Json -Compress
    }
} catch {
    Write-Output '{"Error":"Could not enumerate input devices"}'
}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


# ========== Main ==========

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Input Controller")
    sub = parser.add_subparsers(dest="action")

    sub.add_parser("keyboards", help="List keyboard devices")
    sub.add_parser("mice", help="List mouse/pointing devices")
    sub.add_parser("gamepads", help="List game controllers")
    sub.add_parser("all", help="List all input devices")

    args = parser.parse_args()

    if args.action == "keyboards":
        print(list_keyboards())
    elif args.action == "mice":
        print(list_mice())
    elif args.action == "gamepads":
        print(list_gamepads())
    elif args.action == "all":
        print(list_all())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
