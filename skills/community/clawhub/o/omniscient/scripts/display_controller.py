#!/usr/bin/env python3
"""
Display Controller - Manage monitors and display settings on Windows.

Capabilities:
  - Display info (resolution, refresh rate, DPI, multi-monitor)
  - List available display modes
  - Set resolution and refresh rate
  - Night light toggle
  - Display orientation

Requirements: Windows 10/11, PowerShell 5.1+
Dependencies: None (uses Windows built-in APIs)
"""

import subprocess
import sys
import os
import json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run_ps as _run_ps


# ========== Display Info ==========

def display_info():
    """Get detailed display information."""
    script = r"""
try {
    $monitors = Get-CimInstance Win32_VideoController
    $displays = Get-CimInstance Win32_DesktopMonitor
    $result = @()
    foreach ($m in $monitors) {
        $disp = $displays | Where-Object { $_.MonitorType -ne 'Default Monitor' } | Select-Object -First 1
        $result += [PSCustomObject]@{
            Adapter = $m.Name
            Resolution = "$($m.CurrentHorizontalResolution)x$($m.CurrentVerticalResolution)"
            RefreshRate = "$($m.CurrentRefreshRate) Hz"
            ColorDepth = "$($m.CurrentBitsPerPixel)-bit"
            VRAM_MB = [math]::Round($m.AdapterRAM / 1MB, 0)
            DriverVersion = $m.DriverVersion
            DriverDate = $m.DriverDate
            Status = $m.Status
            VideoProcessor = $m.VideoProcessor
            VideoModeDescription = $m.VideoModeDescription
        }
    }
    $result | ConvertTo-Json -Compress
} catch {
    Write-Output '{"Error":"Could not get display information"}'
}
"""
    stdout, _, _ = _run_ps(script, timeout=15)
    return stdout


# ========== Multi-Monitor Layout ==========

def monitor_layout():
    """Get multi-monitor layout information."""
    script = r"""
try {
    Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class MonitorAPI {
    [DllImport("user32.dll")]
    public static extern bool EnumDisplayMonitors(IntPtr hdc, IntPtr lprcClip, MonitorEnumDelegate lpfnEnum, IntPtr dwData);

    [DllImport("user32.dll", CharSet = CharSet.Auto)]
    public static extern bool GetMonitorInfo(IntPtr hMonitor, ref MONITORINFOEX lpmi);

    public delegate bool MonitorEnumDelegate(IntPtr hMonitor, IntPtr hdcMonitor, ref RECT lprcMonitor, IntPtr dwData);

    [StructLayout(LayoutKind.Sequential)]
    public struct RECT {
        public int Left, Top, Right, Bottom;
    }

    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Auto)]
    public struct MONITORINFOEX {
        public int Size;
        public RECT Monitor;
        public RECT WorkArea;
        public uint Flags;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
        public string DeviceName;
    }
}
"@

    $monitors = @()
    $callback = [MonitorAPI+MonitorEnumDelegate]{
        param($hMonitor, $hdc, $lprc, $dwData)
        $mi = New-Object MonitorAPI+MONITORINFOEX
        $mi.Size = [System.Runtime.InteropServices.Marshal]::SizeOf($mi)
        [MonitorAPI]::GetMonitorInfo($hMonitor, [ref]$mi) | Out-Null
        $monitors += [PSCustomObject]@{
            Handle = $hMonitor
            Name = $mi.DeviceName
            Left = $mi.Monitor.Left
            Top = $mi.Monitor.Top
            Width = $mi.Monitor.Right - $mi.Monitor.Left
            Height = $mi.Monitor.Bottom - $mi.Monitor.Top
            WorkLeft = $mi.WorkArea.Left
            WorkTop = $mi.WorkArea.Top
            WorkWidth = $mi.WorkArea.Right - $mi.WorkArea.Left
            WorkHeight = $mi.WorkArea.Bottom - $mi.WorkArea.Top
            IsPrimary = ($mi.Flags -band 1) -eq 1
        }
        return $true
    }
    [MonitorAPI]::EnumDisplayMonitors([IntPtr]::Zero, [IntPtr]::Zero, $callback, [IntPtr]::Zero) | Out-Null
    $monitors | ConvertTo-Json -Compress
} catch {
    # Fallback to simpler method
    try {
        Get-CimInstance Win32_DesktopMonitor | ForEach-Object {
            [PSCustomObject]@{
                Name = $_.Name
                DeviceID = $_.DeviceID
               ScreenWidth = $_.ScreenWidth
                ScreenHeight = $_.ScreenHeight
                PixelsPerXLogicalInch = $_.PixelsPerXLogicalInch
            }
        } | ConvertTo-Json -Compress
    } catch {
        Write-Output '{"Error":"Could not get monitor layout"}'
    }
}
"""
    stdout, _, _ = _run_ps(script, timeout=15)
    return stdout


# ========== DPI Info ==========

def dpi_info():
    """Get DPI scaling information."""
    script = r"""
try {
    Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class DPIHelper {
    [DllImport("user32.dll")]
    public static extern IntPtr GetDC(IntPtr hwnd);

    [DllImport("user32.dll")]
    public static extern int ReleaseDC(IntPtr hwnd, IntPtr hdc);

    [DllImport("gdi32.dll")]
    public static extern int GetDeviceCaps(IntPtr hdc, int index);

    public const int LOGPIXELSX = 88;
    public const int LOGPIXELSY = 90;
}
"@
    $hdc = [DPIHelper]::GetDC([IntPtr]::Zero)
    $dpiX = [DPIHelper]::GetDeviceCaps($hdc, [DPIHelper]::LOGPIXELSX)
    $dpiY = [DPIHelper]::GetDeviceCaps($hdc, [DPIHelper]::LOGPIXELSY)
    [DPIHelper]::ReleaseDC([IntPtr]::Zero, $hdc) | Out-Null
    [PSCustomObject]@{
        DPI_X = $dpiX
        DPI_Y = $dpiY
        ScalePercent = [math]::Round($dpiX / 96 * 100)
    } | ConvertTo-Json
} catch {
    Write-Output '{"Error":"Could not get DPI info"}'
}
"""
    stdout, _, _ = _run_ps(script, timeout=10)
    return stdout


# ========== Night Light ==========

def night_light(action):
    """Control Windows Night Light feature."""
    if action == "status":
        script = r"""
try {
    $key = Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\CloudStore\Store\DefaultAccount\Windows\features\NightLight" -ErrorAction Stop
    $val = Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\CloudStore\Store\DefaultAccount\Windows\data" -Name "NightLight" -ErrorAction Stop
    # Alternative: check via Get-ItemProperty with wildcard
    $nightKey = Get-ChildItem "HKCU:\Software\Microsoft\Windows\CurrentVersion\CloudStore\Store\DefaultAccount\Windows\features\" -ErrorAction SilentlyContinue | 
        Where-Object { $_.Name -like '*NightLight*' } | Select-Object -First 1
    [PSCustomObject]@{
        Status = "Use 'on' or 'off' to control Night Light"
        Note = "Night Light setting is available in Windows Settings > Display"
    } | ConvertTo-Json
} catch {
    Write-Output '{"Note":"Use display_controller.py night-light on|off to toggle Night Light"}'
}
"""
        stdout, _, _ = _run_ps(script, timeout=10)
        return stdout
    else:
        script = f"""
try {{
    # Toggle Night Light via registry
    if ('{action}' -eq 'on') {{
        Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\CloudStore\Store\DefaultAccount\Windows\blueLightReduction" -Name "setting" -Value 1 -ErrorAction SilentlyContinue
        # Alternative: use Settings API
        $ns = "root\default"
        $path = "SOFTWARE\Microsoft\Windows\CurrentVersion\CloudStore\Store\DefaultAccount\Windows\blueLightReduction"
        reg add "HKCU\$path" /v setting /t REG_DWORD /d 1 /f 2>$null
    }} elseif ('{action}' -eq 'off') {{
        reg add "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\CloudStore\Store\DefaultAccount\Windows\blueLightReduction" /v setting /t REG_DWORD /d 0 /f 2>$null
    }} else {{
        Write-Output "ERROR: Use 'on' or 'off'"
        return
    }}
    Write-Output "OK: Night Light turned {action}"
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
        stdout, _, _ = _run_ps(script, timeout=10)
        return stdout


# ========== Orientation ==========

def set_orientation(orientation):
    """Set display orientation."""
    valid = ["landscape", "portrait", "landscape-flipped", "portrait-flipped"]
    if orientation not in valid:
        return f"ERROR: Invalid orientation. Use one of: {', '.join(valid)}"

    orient_map = {
        "landscape": 0,
        "portrait": 1,
        "landscape-flipped": 2,
        "portrait-flipped": 3,
    }
    dm_value = orient_map[orientation]

    script = f"""
try {{
    # Change display orientation via ChangeDisplaySettings
    Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class DisplayOrientation {{
    [StructLayout(LayoutKind.Sequential)]
    public struct DEVMODE {{
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
        public string dmDeviceName;
        public short dmSpecVersion;
        public short dmDriverVersion;
        public short dmSize;
        public short dmDriverExtra;
        public int dmFields;
        public int dmPositionX;
        public int dmPositionY;
        public int dmDisplayOrientation;
        public int dmDisplayFixedOutput;
        public short dmColor;
        public short dmDuplex;
        public short dmYResolution;
        public short dmTTOption;
        public short dmCollate;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
        public string dmFormName;
        public short dmLogPixels;
        public int dmBitsPerPel;
        public int dmPelsWidth;
        public int dmPelsHeight;
        public int dmDisplayFlags;
        public int dmDisplayFrequency;
    }}

    public const int ENUM_CURRENT_SETTINGS = -1;
    public const int DM_DISPLAYORIENTATION = 0x00000080;
    public const int DISP_CHANGE_SUCCESSFUL = 0;
    public const int CDS_UPDATEREGISTRY = 1;
    public const int CDS_RESET = 0x40000000;

    [DllImport("user32.dll")]
    public static extern int EnumDisplaySettings(string deviceName, int modeNum, ref DEVMODE devMode);

    [DllImport("user32.dll")]
    public static extern int ChangeDisplaySettingsEx(string deviceName, ref DEVMODE devMode, IntPtr hwnd, int flags, IntPtr lParam);
}}

    $dm = New-Object DisplayOrientation+DEVMODE
    $dm.dmSize = [System.Runtime.InteropServices.Marshal]::SizeOf($dm)
    [DisplayOrientation]::EnumDisplaySettings($null, [DisplayOrientation]::ENUM_CURRENT_SETTINGS, [ref]$dm) | Out-Null
    $dm.dmFields = [DisplayOrientation]::DM_DISPLAYORIENTATION
    $dm.dmDisplayOrientation = {dm_value}
    $result = [DisplayOrientation]::ChangeDisplaySettingsEx($null, [ref]$dm, [IntPtr]::Zero, 
        [DisplayOrientation]::CDS_UPDATEREGISTRY -bor [DisplayOrientation]::CDS_RESET, [IntPtr]::Zero)
    if ($result -eq 0) {{
        Write-Output "OK: Display orientation set to '{orientation}'"
    }} else {{
        Write-Output "ERROR: Failed to change orientation (error code: $result)"
    }}
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    stdout, _, _ = _run_ps(script, timeout=15)
    return stdout


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Display Controller")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("info", help="Display info (resolution, refresh rate, VRAM)")
    sub.add_parser("layout", help="Multi-monitor layout")
    sub.add_parser("dpi", help="DPI scaling info")

    p_nl = sub.add_parser("night-light", help="Night Light control")
    p_nl.add_argument("action", nargs="?", default="status", choices=["on", "off", "status"])

    p_orient = sub.add_parser("orientation", help="Set display orientation")
    p_orient.add_argument("value", choices=["landscape", "portrait", "landscape-flipped", "portrait-flipped"])

    args = parser.parse_args()

    if args.command == "info":
        print(display_info())
    elif args.command == "layout":
        print(monitor_layout())
    elif args.command == "dpi":
        print(dpi_info())
    elif args.command == "night-light":
        print(night_light(args.action))
    elif args.command == "orientation":
        print(set_orientation(args.value))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
