#!/usr/bin/env python3
"""
GPU Controller - Monitor and control NVIDIA GPUs on Windows.

Capabilities:
  - GPU overview (model, driver, VRAM)
  - Real-time monitoring (utilization, temperature, power, memory)
  - GPU process listing
  - VRAM details and usage
  - Temperature monitoring
  - Power consumption and fan info
  - Clock speed info
  - Set power mode (performance/power-save)
  - Custom nvidia-smi query
  - List all GPUs with indices

Requirements: Windows 10/11, NVIDIA GPU with nvidia-smi
Dependencies: None (uses nvidia-smi from NVIDIA driver)
"""

import subprocess
import sys
import os
import json
import time
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run_ps as _run_ps, run_cmd as _run_cmd


def _validate_nvidia_query_fields(query_fields):
    """Validate nvidia-smi query fields to prevent injection.

    Only allows alphanumeric characters, dots, underscores, hyphens, commas, and spaces.
    """
    if not query_fields or not isinstance(query_fields, str):
        return None
    # Only allow safe characters: letters, digits, dot, underscore, hyphen, comma, space
    if not re.match(r'^[a-zA-Z0-9._\-,\s]+$', query_fields):
        return None
    return query_fields.strip()


def _has_nvidia_smi():
    """Check if nvidia-smi is available."""
    _, _, rc = _run_cmd("nvidia-smi --query-gpu=name --format=csv,noheader,nounits", 5)
    return rc == 0


def _nvidia_query(query_str, fmt="csv,noheader,nounits", gpu_id=None):
    """Execute nvidia-smi query and return results per GPU."""
    gpu_flag = f"-i {int(gpu_id)}" if gpu_id is not None else ""
    cmd = f"nvidia-smi --query-gpu={query_str} --format={fmt} {gpu_flag}"
    stdout, _, rc = _run_cmd(cmd, 10)
    if rc != 0 or not stdout:
        return []
    return [line.strip() for line in stdout.split("\n") if line.strip()]


def _parse_size(size_str):
    """Parse size string to MiB."""
    size_str = str(size_str).strip()
    for unit, factor in [("GiB", 1024), ("GB", 1000), ("MiB", 1), ("MB", 1)]:
        if size_str.upper().endswith(unit.upper()):
            try:
                return float(size_str[: -len(unit)].strip()) * factor
            except ValueError:
                return 0
    try:
        return float(size_str)
    except ValueError:
        return 0


def _bar(value, max_val, width=30):
    """Generate a progress bar string."""
    if max_val <= 0:
        max_val = 1
    pct = min(value / max_val, 1.0)
    filled = int(pct * width)
    empty = width - filled
    return f"[{'█' * filled}{'░' * empty}] {pct*100:.1f}%"


# ========== GPU Info ==========

def gpu_info(gpu_id=None):
    """Get GPU overview information."""
    if not _has_nvidia_smi():
        # Try WMI for non-NVIDIA GPUs
        script = r"""
try {
    Get-CimInstance Win32_VideoController | ForEach-Object {
        [PSCustomObject]@{
            Name = $_.Name
            AdapterRAM_MB = [math]::Round($_.AdapterRAM / 1MB, 0)
            DriverVersion = $_.DriverVersion
            VideoProcessor = $_.VideoProcessor
        }
    } | ConvertTo-Json
} catch {
    Write-Output '{"Error":"No GPU detected"}'
}
"""
        stdout, _, _ = _run_ps(script, timeout=10)
        return stdout

    gpu_flag = gpu_id
    names = _nvidia_query("name", gpu_id=gpu_flag)
    drivers = _nvidia_query("driver_version", gpu_id=gpu_flag)
    cuda = _nvidia_query("cuda_version", gpu_id=gpu_flag)
    mems = _nvidia_query("memory.total", gpu_id=gpu_flag)

    results = []
    for i in range(len(names)):
        info = {"GPU": i, "Model": names[i]}
        if drivers and i < len(drivers):
            info["DriverVersion"] = drivers[i]
        if cuda and i < len(cuda):
            info["CUDAVersion"] = cuda[i]
        if mems and i < len(mems):
            info["VRAMTotal"] = mems[i]
        pci = _nvidia_query("pcie.link.gen.current,pcie.link.width.current", gpu_id=gpu_flag)
        if pci and i < len(pci):
            info["PCIe"] = pci[i]
        results.append(info)

    return json.dumps(results, indent=2, ensure_ascii=False)


def list_gpus():
    """List all GPUs with indices."""
    if not _has_nvidia_smi():
        return json.dumps({"Error": "No NVIDIA GPU detected"})

    names = _nvidia_query("name")
    uuids = _nvidia_query("uuid")
    mems = _nvidia_query("memory.total")

    results = []
    for i in range(len(names)):
        uuid_short = (uuids[i] if i < len(uuids) else "N/A")[-12:]
        mem = mems[i] if i < len(mems) else "N/A"
        results.append({
            "Index": i,
            "Model": names[i],
            "VRAM": mem,
            "UUID": f"...{uuid_short}"
        })

    return json.dumps(results, indent=2, ensure_ascii=False)


# ========== Real-time Monitoring ==========

def gpu_monitor(interval=2, count=5, gpu_id=None):
    """Monitor GPU state in real-time."""
    if not _has_nvidia_smi():
        return json.dumps({"Error": "No NVIDIA GPU detected"})

    results = []
    for tick in range(1, count + 1):
        entry = {"sample": tick}

        utils = _nvidia_query("utilization.gpu,utilization.memory", gpu_id=gpu_id)
        mems = _nvidia_query("memory.used,memory.total", gpu_id=gpu_id)
        temps = _nvidia_query("temperature.gpu", gpu_id=gpu_id)
        powers = _nvidia_query("power.draw,power.limit", gpu_id=gpu_id)

        for i in range(len(utils)):
            parts = utils[i].split(", ") if ", " in utils[i] else utils[i].split(", ")
            gpu_util = float(parts[0]) if parts else 0
            mem_util = float(parts[1]) if len(parts) > 1 else 0

            mem_parts = mems[i].split(", ") if ", " in mems[i] else mems[i].split(", ")
            mem_used = _parse_size(mem_parts[0]) if mem_parts else 0
            mem_total = _parse_size(mem_parts[1]) if len(mem_parts) > 1 else 1

            temp = int(temps[i]) if i < len(temps) else 0

            gpu_entry = {
                "GPU": i,
                "ComputeUtil": f"{gpu_util:.0f}%",
                "MemoryUtil": f"{mem_util:.0f}%",
                "MemoryUsed": f"{mem_used:.0f}/{mem_total:.0f} MiB",
                "Temperature": f"{temp}°C",
            }

            if i < len(powers):
                pw_parts = powers[i].split(", ") if ", " in powers[i] else powers[i].split(", ")
                if pw_parts:
                    pw = float(pw_parts[0]) if pw_parts[0] not in ("[N/A]", "") else 0
                    pw_limit = float(pw_parts[1]) if len(pw_parts) > 1 and pw_parts[1] not in ("[N/A]", "") else 1
                    gpu_entry["Power"] = f"{pw:.0f}/{pw_limit:.0f} W"

            entry[f"GPU{i}"] = gpu_entry

        results.append(entry)
        if tick < count:
            time.sleep(interval)

    return json.dumps(results, indent=2, ensure_ascii=False)


def gpu_processes(gpu_id=None):
    """List processes using GPU."""
    if not _has_nvidia_smi():
        return json.dumps({"Error": "No NVIDIA GPU detected"})

    gpu_flag = f"-i {gpu_id}" if gpu_id is not None else ""
    stdout, _, rc = _run_cmd(
        f"nvidia-smi {gpu_flag} --query-compute-apps=pid,process_name,used_memory,gpu_uuid "
        f"--format=csv,noheader,nounits",
        10
    )

    if not stdout:
        return json.dumps({"Info": "No processes using GPU"})

    lines = [l.strip() for l in stdout.split("\n") if l.strip()]
    procs = []
    total_mem = 0
    for line in lines:
        parts = [p.strip() for p in line.split(", ")]
        if len(parts) >= 3:
            pid, name, mem = parts[0], parts[1], parts[2]
            try:
                mem_val = float(mem)
                total_mem += mem_val
                mem_str = f"{mem_val:.0f} MiB"
            except ValueError:
                mem_str = mem
            procs.append({
                "PID": pid,
                "Process": name,
                "VRAM": mem_str,
            })

    result = {"ProcessCount": len(procs), "TotalVRAM_MiB": f"{total_mem:.0f}", "Processes": procs}
    return json.dumps(result, indent=2, ensure_ascii=False)


# ========== Detailed Info ==========

def gpu_memory(gpu_id=None):
    """Get VRAM details."""
    if not _has_nvidia_smi():
        return json.dumps({"Error": "No NVIDIA GPU detected"})

    totals = _nvidia_query("memory.total", gpu_id=gpu_id)
    useds = _nvidia_query("memory.used", gpu_id=gpu_id)
    frees = _nvidia_query("memory.free", gpu_id=gpu_id)

    results = []
    for i in range(len(totals)):
        total = _parse_size(totals[i])
        used = _parse_size(useds[i])
        free = _parse_size(frees[i])
        pct = (used / total * 100) if total > 0 else 0
        results.append({
            "GPU": i,
            "Total_MiB": f"{total:.0f}",
            "Total_GiB": f"{total/1024:.2f}",
            "Used_MiB": f"{used:.0f}",
            "Used_GiB": f"{used/1024:.2f}",
            "Free_MiB": f"{free:.0f}",
            "Free_GiB": f"{free/1024:.2f}",
            "UsagePercent": f"{pct:.1f}",
        })

    return json.dumps(results, indent=2, ensure_ascii=False)


def gpu_temperature(gpu_id=None):
    """Get GPU temperature info."""
    if not _has_nvidia_smi():
        return json.dumps({"Error": "No NVIDIA GPU detected"})

    temps = _nvidia_query("temperature.gpu", gpu_id=gpu_id)
    slowdowns = _nvidia_query("temperature.gpu.slowdown", gpu_id=gpu_id)

    results = []
    for i in range(len(temps)):
        temp = int(temps[i])
        slowdown = int(slowdowns[i]) if i < len(slowdowns) else 100

        if temp < 60:
            status = "Normal"
        elif temp < 80:
            status = "Warm"
        elif temp < slowdown:
            status = "Hot"
        else:
            status = "Throttling"

        results.append({
            "GPU": i,
            "Temperature_C": temp,
            "SlowdownThreshold_C": slowdown,
            "Status": status,
        })

    return json.dumps(results, indent=2, ensure_ascii=False)


def gpu_power(gpu_id=None):
    """Get power consumption and fan info."""
    if not _has_nvidia_smi():
        return json.dumps({"Error": "No NVIDIA GPU detected"})

    powers = _nvidia_query("power.draw,power.limit,power.min_limit,power.max_limit", gpu_id=gpu_id)
    fans = _nvidia_query("fan.speed", gpu_id=gpu_id)

    results = []
    for i in range(len(powers)):
        parts = [p.strip() for p in powers[i].split(", ")]
        draw = float(parts[0]) if parts[0] not in ("[N/A]", "") else 0
        limit = float(parts[1]) if len(parts) > 1 and parts[1] not in ("[N/A]", "") else 0
        min_lim = float(parts[2]) if len(parts) > 2 and parts[2] not in ("[N/A]", "") else 0
        max_lim = float(parts[3]) if len(parts) > 3 and parts[3] not in ("[N/A]", "") else 0

        entry = {
            "GPU": i,
            "PowerDraw_W": f"{draw:.0f}",
            "PowerLimit_W": f"{limit:.0f}",
        }
        if min_lim > 0 and max_lim > 0:
            entry["PowerRange_W"] = f"{min_lim:.0f} ~ {max_lim:.0f}"

        if i < len(fans) and fans[i] not in ("[N/A]", "[Not Supported]", ""):
            entry["FanSpeed"] = f"{fans[i]}%"

        results.append(entry)

    return json.dumps(results, indent=2, ensure_ascii=False)


def gpu_clock(gpu_id=None):
    """Get clock speed info."""
    if not _has_nvidia_smi():
        return json.dumps({"Error": "No NVIDIA GPU detected"})

    clocks = _nvidia_query("clocks.gr,clocks.mem,clocks.max.gr,clocks.max.mem", gpu_id=gpu_id)

    results = []
    for i in range(len(clocks)):
        parts = [p.strip() for p in clocks[i].split(", ")]
        results.append({
            "GPU": i,
            "CoreClock_MHz": parts[0] if parts else "N/A",
            "MemoryClock_MHz": parts[1] if len(parts) > 1 else "N/A",
            "MaxCoreClock_MHz": parts[2] if len(parts) > 2 else "N/A",
            "MaxMemoryClock_MHz": parts[3] if len(parts) > 3 else "N/A",
        })

    return json.dumps(results, indent=2, ensure_ascii=False)


# ========== Power Control ==========

def set_power_mode(mode, gpu_id=None):
    """Set GPU power mode (performance, power-save, default, or specific wattage)."""
    if not _has_nvidia_smi():
        return json.dumps({"Error": "No NVIDIA GPU detected"})

    gpu_flag = f"-i {gpu_id}" if gpu_id is not None else ""

    if mode in ("performance", "perf", "high"):
        limits = _nvidia_query("power.max_limit", gpu_id=gpu_id)
        if limits:
            max_w = int(float(limits[0]))
            cmd = f"nvidia-smi {gpu_flag} -pl {max_w}"
            stdout, stderr, rc = _run_cmd(cmd, 10)
            if rc == 0:
                return json.dumps({"OK": f"Set to max performance mode ({max_w} W)"})
            else:
                return json.dumps({"Error": stderr})
        else:
            return json.dumps({"Error": "Cannot query max power limit"})
    elif mode in ("power-save", "save", "low"):
        limits = _nvidia_query("power.min_limit", gpu_id=gpu_id)
        if limits:
            min_w = int(float(limits[0]))
            cmd = f"nvidia-smi {gpu_flag} -pl {min_w}"
            stdout, stderr, rc = _run_cmd(cmd, 10)
            if rc == 0:
                return json.dumps({"OK": f"Set to power-save mode ({min_w} W)"})
            else:
                return json.dumps({"Error": stderr})
        else:
            return json.dumps({"Error": "Cannot query min power limit"})
    elif mode == "default":
        stdout, stderr, rc = _run_cmd(f"nvidia-smi {gpu_flag} -pm 1 -pl 0", 10)
        if rc == 0:
            return json.dumps({"OK": "Reset to default power mode"})
        else:
            return json.dumps({"Error": stderr})
    else:
        try:
            watts = int(mode)
            cmd = f"nvidia-smi {gpu_flag} -pl {watts}"
            stdout, stderr, rc = _run_cmd(cmd, 10)
            if rc == 0:
                return json.dumps({"OK": f"Power limit set to {watts} W"})
            else:
                return json.dumps({"Error": stderr})
        except ValueError:
            return json.dumps({"Error": f"Unknown mode: {mode}", "Usage": "performance / power-save / default / <wattage>"})


# ========== Custom Query ==========

def custom_query(query_fields, gpu_id=None):
    """Execute a custom nvidia-smi query."""
    if not _has_nvidia_smi():
        return json.dumps({"Error": "No NVIDIA GPU detected"})

    if not query_fields:
        query_fields = "name,utilization.gpu,memory.used,memory.total,temperature.gpu"
    else:
        safe_fields = _validate_nvidia_query_fields(query_fields)
        if safe_fields is None:
            return json.dumps({"Error": "Invalid query fields. Only alphanumeric characters, dots, underscores, hyphens, and commas are allowed."})
        query_fields = safe_fields

    results_raw = _nvidia_query(query_fields, "csv,noheader", gpu_id=gpu_id)
    headers = query_fields.split(",")

    if not results_raw:
        return json.dumps({"Info": "No results"})

    results = []
    for i, row in enumerate(results_raw):
        parts = [p.strip() for p in row.split(", ")]
        entry = {"GPU": i}
        for j, header in enumerate(headers):
            entry[header.strip()] = parts[j] if j < len(parts) else "N/A"
        results.append(entry)

    return json.dumps(results, indent=2, ensure_ascii=False)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="GPU Controller")
    sub = parser.add_subparsers(dest="command")

    # info
    p_info = sub.add_parser("info", help="GPU overview")
    p_info.add_argument("--gpu", type=int, help="GPU index")

    # list-gpus
    sub.add_parser("list-gpus", help="List all GPUs with indices")

    # monitor
    p_mon = sub.add_parser("monitor", help="Real-time GPU monitoring")
    p_mon.add_argument("--interval", type=int, default=2, help="Seconds between samples")
    p_mon.add_argument("--count", type=int, default=5, help="Number of samples")
    p_mon.add_argument("--gpu", type=int, help="GPU index")

    # processes
    p_proc = sub.add_parser("processes", help="GPU process usage")
    p_proc.add_argument("--gpu", type=int, help="GPU index")

    # memory
    p_mem = sub.add_parser("memory", help="VRAM details")
    p_mem.add_argument("--gpu", type=int, help="GPU index")

    # temperature
    p_temp = sub.add_parser("temperature", help="GPU temperature")
    p_temp.add_argument("--gpu", type=int, help="GPU index")

    # power
    p_pow = sub.add_parser("power", help="Power and fan info")
    p_pow.add_argument("--gpu", type=int, help="GPU index")

    # clock
    p_clk = sub.add_parser("clock", help="Clock speed info")
    p_clk.add_argument("--gpu", type=int, help="GPU index")

    # set-power
    p_sp = sub.add_parser("set-power", help="Set power mode")
    p_sp.add_argument("mode", help="performance / power-save / default / <wattage>")
    p_sp.add_argument("--gpu", type=int, help="GPU index")

    # query
    p_q = sub.add_parser("query", help="Custom nvidia-smi query")
    p_q.add_argument("--format", help="Query fields, comma-separated")
    p_q.add_argument("--gpu", type=int, help="GPU index")

    args = parser.parse_args()

    if args.command == "info":
        gpu_id = args.gpu if hasattr(args, 'gpu') and args.gpu else None
        print(gpu_info(gpu_id))
    elif args.command == "list-gpus":
        print(list_gpus())
    elif args.command == "monitor":
        gpu_id = args.gpu if hasattr(args, 'gpu') and args.gpu else None
        print(gpu_monitor(args.interval, args.count, gpu_id))
    elif args.command == "processes":
        gpu_id = args.gpu if hasattr(args, 'gpu') and args.gpu else None
        print(gpu_processes(gpu_id))
    elif args.command == "memory":
        gpu_id = args.gpu if hasattr(args, 'gpu') and args.gpu else None
        print(gpu_memory(gpu_id))
    elif args.command == "temperature":
        gpu_id = args.gpu if hasattr(args, 'gpu') and args.gpu else None
        print(gpu_temperature(gpu_id))
    elif args.command == "power":
        gpu_id = args.gpu if hasattr(args, 'gpu') and args.gpu else None
        print(gpu_power(gpu_id))
    elif args.command == "clock":
        gpu_id = args.gpu if hasattr(args, 'gpu') and args.gpu else None
        print(gpu_clock(gpu_id))
    elif args.command == "set-power":
        gpu_id = args.gpu if hasattr(args, 'gpu') and args.gpu else None
        print(set_power_mode(args.mode, gpu_id))
    elif args.command == "query":
        gpu_id = args.gpu if hasattr(args, 'gpu') and args.gpu else None
        print(custom_query(args.format, gpu_id))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
