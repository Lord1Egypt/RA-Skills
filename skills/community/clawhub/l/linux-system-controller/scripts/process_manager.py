#!/usr/bin/env python3
"""
Process Manager - List, start, stop, and monitor system processes on Linux.

Requirements: Linux with standard tools (ps, pgrep, pkill)
Dependencies: None
"""

import subprocess
import json
import sys
import os

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


def run_command(cmd, timeout=30):
    """Execute shell command with proper encoding."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace"
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "ERROR: Command timed out", -1
    except Exception as e:
        return "", f"ERROR: {e}", -1


def list_processes(name=None):
    """List running processes. Optionally filter by name."""
    if name:
        cmd = f"pgrep -fl {name}"
        stdout, stderr, code = run_command(cmd)
        if code != 0:
            return {"error": f"No processes found with name: {name}", "processes": []}

        processes = []
        for line in stdout.split('\n'):
            if not line.strip():
                continue
            parts = line.split(None, 1)
            if len(parts) == 2:
                pid = parts[0]
                cmd_line = parts[1]
                processes.append({
                    "pid": int(pid),
                    "name": cmd_line.split()[0] if cmd_line else "",
                    "command": cmd_line
                })
        return {"processes": processes}
    else:
        cmd = "ps aux --sort=-%cpu | head -20"
        stdout, stderr, code = run_command(cmd)
        if code != 0:
            return {"error": f"Failed to list processes: {stderr}"}

        processes = []
        lines = stdout.split('\n')[1:]  # Skip header
        for line in lines:
            if not line.strip():
                continue
            parts = line.split(None, 10)
            if len(parts) >= 11:
                processes.append({
                    "user": parts[0],
                    "pid": int(parts[1]),
                    "cpu": float(parts[2]),
                    "mem": float(parts[3]),
                    "vsz": int(parts[4]),
                    "rss": int(parts[5]),
                    "tty": parts[6],
                    "stat": parts[7],
                    "start": parts[8],
                    "time": parts[9],
                    "command": parts[10] if len(parts) > 10 else ""
                })
        return {"processes": processes}


def kill_process(pid=None, name=None):
    """Kill a process by PID or name."""
    if name:
        cmd = f"pkill -f {name}"
    elif pid:
        cmd = f"kill {pid}"
    else:
        return {"error": "Either --pid or --name is required"}

    stdout, stderr, code = run_command(cmd)
    if code == 0:
        killed_by = name if name else pid
        return {"success": True, "killed": killed_by}
    else:
        return {"error": f"Failed to kill process: {stderr}"}


def start_process(command):
    """Start a process."""
    try:
        # Use nohup to run in background
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        return {"success": True, "pid": process.pid, "command": command}
    except Exception as e:
        return {"error": f"Failed to start process: {e}"}


def get_process_info(pid):
    """Get detailed information about a process."""
    cmd = f"ps -p {pid} -o pid,ppid,user,%cpu,%mem,vsz,rss,tty,stat,start,time,comm --no-headers"
    stdout, stderr, code = run_command(cmd)
    if code != 0:
        return {"error": f"Process {pid} not found"}

    parts = stdout.split()
    return {
        "pid": int(parts[0]),
        "ppid": int(parts[1]),
        "user": parts[2],
        "cpu": float(parts[3]),
        "mem": float(parts[4]),
        "vsz": int(parts[5]),
        "rss": int(parts[6]),
        "tty": parts[7],
        "stat": parts[8],
        "start": parts[9],
        "time": parts[10],
        "command": parts[11] if len(parts) > 11 else ""
    }


def system_info():
    """Get overall system information."""
    # CPU info
    cpu_info_cmd = "nproc"
    cpu_count, _, _ = run_command(cpu_info_cmd)

    # Memory info
    mem_info_cmd = "free -h | grep Mem"
    mem_info, _, _ = run_command(mem_info_cmd)

    # Load average
    load_cmd = "uptime | awk -F'load average:' '{print $2}'"
    load_avg, _, _ = run_command(load_cmd)

    # Process count
    proc_cmd = "ps aux | wc -l"
    proc_count, _, _ = run_command(proc_cmd)

    return {
        "cpu_cores": int(cpu_count) if cpu_count else 0,
        "memory": mem_info,
        "load_average": load_avg,
        "process_count": int(proc_count) if proc_count else 0
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Process Manager for Linux")
    subparsers = parser.add_subparsers(dest='action', help='Action to perform')

    # List processes
    parser_list = subparsers.add_parser('list', help='List processes')
    parser_list.add_argument('--name', help='Filter by process name')

    # Kill process
    parser_kill = subparsers.add_parser('kill', help='Kill a process')
    parser_kill.add_argument('--pid', type=int, help='Process ID')
    parser_kill.add_argument('--name', help='Process name')

    # Start process
    parser_start = subparsers.add_parser('start', help='Start a process')
    parser_start.add_argument('command', help='Command to execute')

    # Get process info
    parser_info = subparsers.add_parser('info', help='Get process info')
    parser_info.add_argument('--pid', type=int, required=True, help='Process ID')

    # System info
    parser_system = subparsers.add_parser('system', help='Get system information')

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    result = {}
    if args.action == 'list':
        result = list_processes(name=args.name)
    elif args.action == 'kill':
        result = kill_process(pid=args.pid, name=args.name)
    elif args.action == 'start':
        result = start_process(args.command)
    elif args.action == 'info':
        result = get_process_info(args.pid)
    elif args.action == 'system':
        result = system_info()

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
