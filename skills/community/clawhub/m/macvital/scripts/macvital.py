#!/usr/bin/env python3
"""
macvital - macOS hardware health monitor for AI agents
Checks CPU, RAM, disk, temperature, and top processes.

Commands:
  status      One-line health summary (good/warn/critical)
  detail      Full breakdown of all metrics
  top         Top CPU and RAM processes
  temp        CPU/GPU temperature (Apple Silicon)
  watch       Continuous monitoring mode
  check       Exit 0=healthy, 1=warn, 2=critical (for scripts)
"""

import sys
import os
import json
import subprocess
import re
import time
import argparse
from datetime import datetime

# Thresholds
CPU_WARN = 70
CPU_CRIT = 90
RAM_WARN = 75
RAM_CRIT = 90
DISK_WARN = 80
DISK_CRIT = 90
TEMP_WARN = 80   # Celsius
TEMP_CRIT = 95


def run(cmd, timeout=10):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, shell=isinstance(cmd, str))
        return r.stdout.strip()
    except Exception:
        return ''


def get_cpu_usage():
    """Get overall CPU usage % (average over 1 sample)."""
    out = run('top -l 2 -n 0 -s 1')
    # Look for the second "CPU usage" line (first sample is often 0)
    lines = [l for l in out.splitlines() if 'CPU usage' in l]
    if len(lines) >= 2:
        line = lines[-1]
    elif lines:
        line = lines[0]
    else:
        return None

    # Parse: "CPU usage: 12.50% user, 8.33% sys, 79.16% idle"
    idle_match = re.search(r'([\d.]+)%\s+idle', line)
    if idle_match:
        return round(100 - float(idle_match.group(1)), 1)
    return None


def get_ram():
    """Get RAM stats from vm_stat. Returns dict with used_pct, used_gb, total_gb, pressure."""
    out = run('vm_stat')
    page_size = 16384  # Apple Silicon default

    stats = {}
    for line in out.splitlines():
        m = re.match(r'^(.+?):\s+(\d+)', line)
        if m:
            stats[m.group(1).strip()] = int(m.group(2))

    # Pages
    active = stats.get('Pages active', 0)
    wired = stats.get('Pages wired down', 0)
    compressed = stats.get('Pages occupied by compressor', 0)
    free = stats.get('Pages free', 0)
    inactive = stats.get('Pages inactive', 0)
    speculative = stats.get('Pages speculative', 0)

    used_pages = active + wired + compressed
    total_pages = used_pages + free + inactive + speculative

    used_gb = (used_pages * page_size) / (1024**3)
    total_gb = (total_pages * page_size) / (1024**3)

    # Also get total RAM from sysctl
    hw_mem = run('sysctl -n hw.memsize')
    if hw_mem:
        total_gb = int(hw_mem) / (1024**3)

    used_pct = round((used_pages * page_size) / (total_gb * 1024**3) * 100, 1)

    # Memory pressure indicator
    if used_pct > RAM_CRIT:
        pressure = 'critical'
    elif used_pct > RAM_WARN:
        pressure = 'high'
    else:
        pressure = 'normal'

    return {
        'used_pct': used_pct,
        'used_gb': round(used_gb, 1),
        'total_gb': round(total_gb, 1),
        'pressure': pressure,
        'wired_gb': round((wired * page_size) / (1024**3), 1),
        'compressed_gb': round((compressed * page_size) / (1024**3), 1),
    }


def get_disk(path='/'):
    """Get disk usage for a path."""
    out = run(f'df -k {path}')
    lines = out.splitlines()
    if len(lines) < 2:
        return None
    parts = lines[1].split()
    if len(parts) < 5:
        return None
    total_kb = int(parts[1])
    used_kb = int(parts[2])
    avail_kb = int(parts[3])
    used_pct = round(used_kb / total_kb * 100, 1) if total_kb else 0

    return {
        'used_pct': used_pct,
        'used_gb': round(used_kb / (1024**2), 1),
        'total_gb': round(total_kb / (1024**2), 1),
        'avail_gb': round(avail_kb / (1024**2), 1),
        'path': path,
    }


def get_temps():
    """Get thermal info. Die temps need sudo; pressure state is always available."""
    temps = {}

    # Thermal pressure state (no sudo needed) via notarization
    try:
        # macOS thermal pressure: 0=nominal, 1=fair, 2=serious, 3=critical
        ioreg_out = run(
            '/usr/sbin/ioreg -r -d 1 -n "AppleARMPMU" 2>/dev/null | grep -i thermal',
            timeout=5
        )
        pressure_match = re.search(r'thermalPressureLevel.*?(\d+)', ioreg_out)
        if pressure_match:
            levels = {0: 'nominal', 1: 'fair', 2: 'serious', 3: 'critical'}
            level = int(pressure_match.group(1))
            temps['pressure'] = levels.get(level, str(level))
    except Exception:
        pass

    # Try powermetrics for actual die temps (requires sudo)
    pm_out = run('sudo powermetrics -n 1 -i 500 --samplers cpu_power 2>/dev/null', timeout=8)
    if pm_out:
        cpu_match = re.search(r'CPU die temperature:\s+([\d.]+)', pm_out)
        gpu_match = re.search(r'GPU die temperature:\s+([\d.]+)', pm_out)
        if cpu_match:
            temps['cpu_die_c'] = float(cpu_match.group(1))
        if gpu_match:
            temps['gpu_die_c'] = float(gpu_match.group(1))

    return temps


def get_top_processes(n=5):
    """Get top CPU and RAM processes."""
    # Top CPU
    cpu_out = run(f'ps -Acro pid,pcpu,pmem,comm -r | head -{n + 1}')
    cpu_procs = []
    for line in cpu_out.splitlines()[1:]:
        parts = line.strip().split(None, 3)
        if len(parts) >= 4:
            cpu_procs.append({'pid': parts[0], 'cpu': parts[1], 'mem': parts[2], 'name': parts[3]})

    # Top RAM
    mem_out = run(f'ps -Acro pid,pmem,pcpu,comm -m | head -{n + 1}')
    mem_procs = []
    for line in mem_out.splitlines()[1:]:
        parts = line.strip().split(None, 3)
        if len(parts) >= 4:
            mem_procs.append({'pid': parts[0], 'mem': parts[1], 'cpu': parts[2], 'name': parts[3]})

    return {'cpu': cpu_procs, 'mem': mem_procs}


def classify(val, warn, crit, higher_is_worse=True):
    if higher_is_worse:
        if val >= crit:
            return 'critical', '🔴'
        elif val >= warn:
            return 'warn', '🟡'
        return 'ok', '🟢'
    else:
        if val <= crit:
            return 'critical', '🔴'
        elif val <= warn:
            return 'warn', '🟡'
        return 'ok', '🟢'


def status(json_out=False, quiet=False):
    """One-line health summary."""
    cpu = get_cpu_usage()
    ram = get_ram()
    disk = get_disk('/')

    issues = []
    overall = 'ok'

    cpu_state, cpu_icon = classify(cpu or 0, CPU_WARN, CPU_CRIT)
    ram_state, ram_icon = classify(ram['used_pct'], RAM_WARN, RAM_CRIT)
    disk_state, disk_icon = classify(disk['used_pct'] if disk else 0, DISK_WARN, DISK_CRIT)

    for state in [cpu_state, ram_state, disk_state]:
        if state == 'critical':
            overall = 'critical'
        elif state == 'warn' and overall == 'ok':
            overall = 'warn'

    if json_out:
        print(json.dumps({
            'status': overall,
            'cpu_pct': cpu,
            'ram_pct': ram['used_pct'],
            'ram_used_gb': ram['used_gb'],
            'ram_total_gb': ram['total_gb'],
            'disk_pct': disk['used_pct'] if disk else None,
            'disk_avail_gb': disk['avail_gb'] if disk else None,
            'timestamp': datetime.now().isoformat(),
        }))
        return overall

    if not quiet:
        overall_icon = '🟢' if overall == 'ok' else ('🟡' if overall == 'warn' else '🔴')
        cpu_str = f"{cpu}%" if cpu is not None else "n/a"
        ram_str = f"{ram['used_gb']}/{ram['total_gb']}GB ({ram['used_pct']}%)"
        disk_str = f"{disk['avail_gb']}GB free ({disk['used_pct']}% used)" if disk else "n/a"

        print(f"{overall_icon} macvital  CPU {cpu_icon} {cpu_str}  RAM {ram_icon} {ram_str}  Disk {disk_icon} {disk_str}")

    return overall


def detail():
    """Full health breakdown."""
    print(f"⚡ macvital — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # CPU
    cpu = get_cpu_usage()
    cpu_model = run('sysctl -n machdep.cpu.brand_string') or run('sysctl -n hw.model')
    cpu_cores = run('sysctl -n hw.physicalcpu')
    cpu_state, cpu_icon = classify(cpu or 0, CPU_WARN, CPU_CRIT)
    print(f"CPU  {cpu_icon}")
    print(f"  Usage:  {cpu}%")
    if cpu_model:
        print(f"  Model:  {cpu_model}")
    if cpu_cores:
        print(f"  Cores:  {cpu_cores} physical")

    # RAM
    print()
    ram = get_ram()
    ram_state, ram_icon = classify(ram['used_pct'], RAM_WARN, RAM_CRIT)
    print(f"RAM  {ram_icon}")
    print(f"  Used:       {ram['used_gb']} / {ram['total_gb']} GB  ({ram['used_pct']}%)")
    print(f"  Wired:      {ram['wired_gb']} GB")
    print(f"  Compressed: {ram['compressed_gb']} GB")
    print(f"  Pressure:   {ram['pressure']}")

    # Disk
    print()
    disk = get_disk('/')
    if disk:
        disk_state, disk_icon = classify(disk['used_pct'], DISK_WARN, DISK_CRIT)
        print(f"Disk  {disk_icon}")
        print(f"  Used:   {disk['used_gb']} / {disk['total_gb']} GB  ({disk['used_pct']}%)")
        print(f"  Free:   {disk['avail_gb']} GB")

    # Temps
    print()
    temps = get_temps()
    if temps:
        print(f"Temp")
        for sensor, val in temps.items():
            if sensor == 'pressure':
                icon = '🟢' if val == 'nominal' else ('🟡' if val == 'fair' else '🔴')
                print(f"  {'pressure':<12} {icon} {val}")
            else:
                t_state, t_icon = classify(val, TEMP_WARN, TEMP_CRIT)
                print(f"  {sensor:<12} {t_icon} {val:.1f}°C")
    else:
        print("Temp  (run with sudo for die temperature data)")


def top_procs(n=8):
    """Show top CPU and RAM processes."""
    procs = get_top_processes(n)

    print("🔥 Top CPU processes:")
    print(f"  {'PID':<8} {'CPU%':<8} {'MEM%':<8} Name")
    print(f"  {'-'*8} {'-'*8} {'-'*8} ----")
    for p in procs['cpu']:
        print(f"  {p['pid']:<8} {p['cpu']:<8} {p['mem']:<8} {p['name']}")

    print()
    print("💾 Top RAM processes:")
    print(f"  {'PID':<8} {'MEM%':<8} {'CPU%':<8} Name")
    print(f"  {'-'*8} {'-'*8} {'-'*8} ----")
    for p in procs['mem']:
        print(f"  {p['pid']:<8} {p['mem']:<8} {p['cpu']:<8} {p['name']}")


def watch(interval=5):
    """Continuous monitoring."""
    print(f"👁  Watch mode (every {interval}s) — Ctrl+C to stop\n")
    try:
        while True:
            status()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped.")


def check():
    """Return exit code: 0=ok, 1=warn, 2=critical."""
    result = status(quiet=True)
    if result == 'critical':
        sys.exit(2)
    elif result == 'warn':
        sys.exit(1)
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description='macvital — macOS hardware health')
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('status').add_argument('--json', action='store_true')
    subparsers.add_parser('detail')
    subparsers.add_parser('top').add_argument('--n', type=int, default=8)
    subparsers.add_parser('temp')
    subparsers.add_parser('check')
    watch_p = subparsers.add_parser('watch')
    watch_p.add_argument('--interval', type=int, default=5)

    args = parser.parse_args()

    if args.command == 'status':
        status(json_out=getattr(args, 'json', False))
    elif args.command == 'detail':
        detail()
    elif args.command == 'top':
        top_procs(n=args.n)
    elif args.command == 'temp':
        temps = get_temps()
        if temps:
            for k, v in temps.items():
                if k == 'pressure':
                    icon = '🟢' if v == 'nominal' else ('🟡' if v == 'fair' else '🔴')
                    print(f"{icon} thermal pressure: {v}")
                else:
                    icon = '🔴' if v >= TEMP_CRIT else ('🟡' if v >= TEMP_WARN else '🟢')
                    print(f"{icon} {k}: {v:.1f}°C")
        else:
            print("No temperature data available.")
    elif args.command == 'check':
        check()
    elif args.command == 'watch':
        watch(interval=args.interval)
    else:
        # Default: status
        status()


if __name__ == '__main__':
    main()
