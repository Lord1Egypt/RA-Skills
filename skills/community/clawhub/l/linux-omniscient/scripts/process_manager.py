#!/usr/bin/env python3
"""Process Manager - Linux version (cross-platform)."""
import subprocess, json, sys, os, argparse, signal
from common import run_cmd, is_windows

def list_processes(name=None):
    """List all processes or filter by name."""
    if name:
        stdout, _, code = run_cmd(['ps', 'aux', '|', 'grep', name])
    else:
        stdout, _, code = run_cmd(['ps', 'aux'])
    return json.dumps({"processes": stdout if code == 0 else "error"}, indent=2)

def start_process(command, work_dir=None):
    """Start a process."""
    if work_dir:
        os.chdir(work_dir)
    stdout, _, code = run_cmd(command.split())
    return json.dumps({"success": code == 0, "output": stdout}, indent=2)

def get_process_info(pid):
    """Get detailed process info."""
    stdout, _, code = run_cmd(['ps', '-p', str(pid), '-o', 'pid,ppid,cmd,%mem,%cpu'])
    return json.dumps({"info": stdout if code == 0 else "error"}, indent=2)

def kill_process(name=None, pid=None, force=False):
    """Kill a process by name or pid."""
    if name:
        # Find pid by name
        stdout, _, code = run_cmd(['pgrep', name])
        if code == 0 and stdout:
            pids = stdout.strip().split('\n')
            for p in pids:
                sig = signal.SIGKILL if force else signal.SIGTERM
                os.kill(int(p), sig)
            return json.dumps({"success": True, "killed": pids}, indent=2)
    elif pid:
        sig = signal.SIGKILL if force else signal.SIGTERM
        os.kill(pid, sig)
        return json.dumps({"success": True, "killed": [pid]}, indent=2)
    return json.dumps({"success": False, "message": "Process not found"}, indent=2)

def system_overview():
    """Get system resource overview."""
    stdout, _, code = run_cmd(['free', '-h'])
    mem = stdout if code == 0 else "error"
    stdout2, _, code2 = run_cmd(['df', '-h'])
    disk = stdout2 if code2 == 0 else "error"
    return json.dumps({"memory": mem, "disk": disk}, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Process Manager')
    subparsers = parser.add_subparsers(dest='command')

    # list command
    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('--name', help='Filter by name')

    # start command
    start_parser = subparsers.add_parser('start')
    start_parser.add_argument('command', help='Command to execute')
    start_parser.add_argument('--dir', help='Working directory')

    # info command
    info_parser = subparsers.add_parser('info')
    info_parser.add_argument('--pid', type=int, required=True)

    # kill command
    kill_parser = subparsers.add_parser('kill')
    kill_parser.add_argument('--name', help='Process name')
    kill_parser.add_argument('--pid', type=int, help='Process ID')
    kill_parser.add_argument('--force', action='store_true')

    # system command
    subparsers.add_parser('system')

    args = parser.parse_args()

    if args.command == 'list':
        print(list_processes(args.name))
    elif args.command == 'start':
        print(start_process(args.command, args.dir))
    elif args.command == 'info':
        print(get_process_info(args.pid))
    elif args.command == 'kill':
        print(kill_process(args.name, args.pid, args.force))
    elif args.command == 'system':
        print(system_overview())

if __name__ == '__main__':
    main()
