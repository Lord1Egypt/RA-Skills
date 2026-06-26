#!/usr/bin/env python3
"""
Thermal Controller - Monitor system temperatures and fan speeds on Windows.

Capabilities:
  - System temperature overview (CPU, GPU if available)
  - Fan speed information
  - Real-time temperature monitoring

Requirements: Windows 10/11, PowerShell 5.1+
Dependencies: psutil (auto-installed); for detailed temps requires OpenHardwareMonitor or LibreHardwareMonitor
"""

import subprocess
import sys
import os
import json
import time

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run_ps as _run_ps


def _ensure_psutil():
    try:
        import psutil
        return psutil
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil>=5.9.8,<7", "-q"])
        import psutil
        return psutil


# ========== Temperature Status ==========

def thermal_status():
    """Get system temperature overview from available sources."""
    results = {}

    # 1. psutil temperatures (Linux/macOS mainly, but try)
    psutil = _ensure_psutil()
    temps = psutil.sensors_temperatures()
    if temps:
        results["psutil"] = {}
        for name, entries in temps.items():
            results["psutil"][name] = [
                {"Label": e.label or "N/A", "Current": e.current, "High": e.high, "Critical": e.critical}
                for e in entries
            ]

    # 2. WMI - MSAcpi_ThermalZoneTemperature (limited on most systems)
    script = r"""
try {
    $zones = Get-CimInstance MSAcpi_ThermalZoneTemperature -Namespace "root\wmi" -ErrorAction Stop
    $wmi_temps = @()
    foreach ($z in $zones) {
        # WMI returns temperature in tenths of Kelvin
        $celsius = [math]::Round(($z.CurrentTemperature - 2732) / 10, 1)
        $wmi_temps += [PSCustomObject]@{
            InstanceName = $z.InstanceName
            Temperature_C = $celsius
            Active = $z.Active
        }
    }
    if ($wmi_temps.Count -gt 0) {
        $wmi_temps | ConvertTo-Json -Compress
    } else {
        Write-Output '{}'
    }
} catch {
    Write-Output '{}'
}
"""
    stdout, _, _ = _run_ps(script, timeout=10)
    if stdout and stdout != '{}':
        try:
            results["wmi_thermal_zone"] = json.loads(stdout)
        except Exception:
            pass

    # 3. CPU temp via WMI (Win32_PerfFormattedData_Counters_ThermalZoneInformation)
    script2 = r"""
try {
    $cpu = Get-CimInstance Win32_Processor -ErrorAction Stop
    [PSCustomObject]@{
        Name = $cpu.Name
        LoadPercentage = $cpu.LoadPercentage
        NumberOfCores = $cpu.NumberOfCores
        MaxClockSpeed_MHz = $cpu.MaxClockSpeed
        CurrentClockSpeed_MHz = $cpu.CurrentClockSpeed
        Note = "CPU temperature not available via standard WMI. Install OpenHardwareMonitor or LibreHardwareMonitor for detailed temps."
    } | ConvertTo-Json -Compress
} catch {
    Write-Output '{}'
}
"""
    stdout2, _, _ = _run_ps(script2, timeout=10)
    if stdout2 and stdout2 != '{}':
        try:
            results["cpu"] = json.loads(stdout2)
        except Exception:
            pass

    # 4. GPU temp via nvidia-smi (if NVIDIA GPU present)
    script3 = r"""
try {
    $nvidia = & nvidia-smi --query-gpu=name,temperature.gpu,fan.speed,power.draw,power.limit --format=csv,noheader,nounits 2>$null
    if ($nvidia) {
        $line = $nvidia.Trim()
        $parts = $line -split ',\s*'
        if ($parts.Count -ge 5) {
            [PSCustomObject]@{
                GPU = $parts[0].Trim()
                Temperature_C = [int]$parts[1].Trim()
                FanSpeed_Pct = if ($parts[2].Trim() -eq '[N/A]') { $null } else { [int]$parts[2].Trim() }
                PowerDraw_W = [double]$parts[3].Trim()
                PowerLimit_W = if ($parts[4].Trim() -eq '[N/A]') { $null } else { [double]$parts[4].Trim() }
            } | ConvertTo-Json
        } else {
            Write-Output '{}'
        }
    } else {
        Write-Output '{}'
    }
} catch {
    Write-Output '{}'
}
"""
    stdout3, _, _ = _run_ps(script3, timeout=10)
    if stdout3 and stdout3 != '{}':
        try:
            results["gpu_nvidia"] = json.loads(stdout3)
        except Exception:
            pass

    if not results:
        return json.dumps({
            "Warning": "No temperature data available from standard sources.",
            "Suggestion": "Install OpenHardwareMonitor (openhardwaremonitor.org) or LibreHardwareMonitor for detailed hardware monitoring."
        }, indent=2, ensure_ascii=False)

    return json.dumps(results, indent=2, ensure_ascii=False)


# ========== CPU Info (thermal context) ==========

def cpu_info():
    """Get CPU info relevant to thermal monitoring."""
    script = r"""
try {
    $cpu = Get-CimInstance Win32_Processor -ErrorAction Stop
    [PSCustomObject]@{
        Name = $cpu.Name
        Cores = $cpu.NumberOfCores
        LogicalProcessors = $cpu.NumberOfLogicalProcessors
        MaxClockSpeed_MHz = $cpu.MaxClockSpeed
        CurrentClockSpeed_MHz = $cpu.CurrentClockSpeed
        LoadPercentage = $cpu.LoadPercentage
        L2CacheSize_KB = $cpu.L2CacheSize
        L3CacheSize_KB = $cpu.L3CacheSize
        VoltageCaps = $cpu.VoltageCaps
    } | ConvertTo-Json
} catch {
    Write-Output '{"Error":"Could not get CPU info"}'
}
"""
    stdout, _, _ = _run_ps(script, timeout=10)
    return stdout


# ========== Fan Speed ==========

def fan_info():
    """Get fan speed information."""
    # Try nvidia-smi for GPU fans
    script = r"""
try {
    $fanInfo = & nvidia-smi --query-gpu=name,fan.speed --format=csv,noheader,nounits 2>$null
    if ($fanInfo) {
        $results = @()
        foreach ($line in $fanInfo) {
            $parts = $line.Trim() -split ',\s*'
            $results += [PSCustomObject]@{
                Device = $parts[0].Trim()
                FanSpeed_Pct = if ($parts[1].Trim() -eq '[N/A]') { $null } else { [int]$parts[1].Trim() }
                Type = "GPU Fan"
            }
        }
        $results | ConvertTo-Json -Compress
    } else {
        @([PSCustomObject]@{
            Note = "No fan data available from nvidia-smi"
            Suggestion = "Install OpenHardwareMonitor for system fan monitoring"
        }) | ConvertTo-Json -Compress
    }
} catch {
    Write-Output '{"Note":"Fan data unavailable","Suggestion":"Install OpenHardwareMonitor"}'
}
"""
    stdout, _, _ = _run_ps(script, timeout=10)
    return stdout


# ========== Real-time Monitor ==========

def thermal_monitor(interval=2, count=5):
    """Monitor temperatures in real-time."""
    results = []
    for i in range(count):
        psutil = _ensure_psutil()
        entry = {"sample": i + 1, "timestamp": time.strftime("%H:%M:%S")}

        # CPU load
        entry["cpu_load_pct"] = psutil.cpu_percent(interval=0.1)

        # Memory usage
        mem = psutil.virtual_memory()
        entry["memory_used_pct"] = mem.percent

        # GPU temp via nvidia-smi (quick single query)
        try:
            script = """
$nvidia = & nvidia-smi --query-gpu=temperature.gpu,utilization.gpu,power.draw --format=csv,noheader,nounits 2>$null
if ($nvidia) { $nvidia.Trim() } else { '' }
"""
            stdout, _, _ = _run_ps(script, timeout=5)
            if stdout:
                parts = stdout.strip().split(", ")
                if len(parts) >= 3:
                    entry["gpu_temp_c"] = int(parts[0])
                    entry["gpu_load_pct"] = int(parts[1])
                    entry["gpu_power_w"] = float(parts[2])
        except Exception:
            pass

        results.append(entry)
        if i < count - 1:
            time.sleep(interval)

    return json.dumps(results, indent=2, ensure_ascii=False)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Thermal Controller")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="Temperature overview")
    sub.add_parser("cpu", help="CPU info (thermal context)")
    sub.add_parser("fans", help="Fan speed info")

    p_mon = sub.add_parser("monitor", help="Real-time monitoring")
    p_mon.add_argument("--interval", type=int, default=2, help="Seconds between samples")
    p_mon.add_argument("--count", type=int, default=5, help="Number of samples")

    args = parser.parse_args()

    if args.command == "status":
        print(thermal_status())
    elif args.command == "cpu":
        print(cpu_info())
    elif args.command == "fans":
        print(fan_info())
    elif args.command == "monitor":
        print(thermal_monitor(args.interval, args.count))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
