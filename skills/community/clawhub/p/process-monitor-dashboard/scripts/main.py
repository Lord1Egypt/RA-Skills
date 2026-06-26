#!/usr/bin/env python3
"""
Process Monitor Dashboard - Real-time system monitoring CLI
"""
import argparse
import json
import time
import sys
import os
from datetime import datetime

try:
    import psutil
except ImportError:
    print("Error: psutil library not installed. Install with: pip install psutil")
    sys.exit(1)


def get_cpu_stats():
    """Get CPU usage statistics"""
    stats = {
        'total_percent': psutil.cpu_percent(interval=0.1),
        'per_core': psutil.cpu_percent(interval=0.1, percpu=True),
        'load_avg': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else [0, 0, 0]
    }
    return stats


def get_memory_stats():
    """Get memory usage statistics"""
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    stats = {
        'total_gb': mem.total / (1024**3),
        'used_gb': mem.used / (1024**3),
        'percent': mem.percent,
        'swap_used_gb': swap.used / (1024**3),
        'swap_percent': swap.percent if swap.total > 0 else 0
    }
    return stats


def get_disk_stats():
    """Get disk usage and I/O statistics"""
    partitions = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            partitions.append({
                'mountpoint': part.mountpoint,
                'total_gb': usage.total / (1024**3),
                'used_gb': usage.used / (1024**3),
                'percent': usage.percent
            })
        except:
            continue
    
    # Disk I/O
    try:
        io = psutil.disk_io_counters()
        disk_io = {
            'read_mb': io.read_bytes / (1024**2),
            'write_mb': io.write_bytes / (1024**2),
            'read_count': io.read_count,
            'write_count': io.write_count
        }
    except:
        disk_io = {}
    
    return {'partitions': partitions, 'io': disk_io}


def get_network_stats():
    """Get network statistics"""
    try:
        net = psutil.net_io_counters()
        stats = {
            'bytes_sent_mb': net.bytes_sent / (1024**2),
            'bytes_recv_mb': net.bytes_recv / (1024**2),
            'packets_sent': net.packets_sent,
            'packets_recv': net.packets_recv
        }
    except:
        stats = {}
    return stats


def get_processes(limit=10, sort_by='cpu'):
    """Get top processes"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'username']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    # Sort
    if sort_by == 'cpu':
        processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
    elif sort_by == 'memory':
        processes.sort(key=lambda x: x.get('memory_percent', 0), reverse=True)
    elif sort_by == 'name':
        processes.sort(key=lambda x: x.get('name', '').lower())
    
    return processes[:limit]


def print_dashboard(interval=2, simple=False):
    """Print real-time dashboard"""
    try:
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            
            # Get stats
            cpu = get_cpu_stats()
            mem = get_memory_stats()
            disk = get_disk_stats()
            net = get_network_stats()
            processes = get_processes(limit=10, sort_by='cpu')
            
            # Header
            print("=" * 80)
            print(f" System Monitor | Refresh: {interval}s | {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
            print("=" * 80)
            
            # CPU
            cpu_bar = "█" * int(cpu['total_percent'] / 5) + "░" * (20 - int(cpu['total_percent'] / 5))
            print(f"CPU:  {cpu_bar} {cpu['total_percent']:.1f}%")
            
            if not simple and len(cpu['per_core']) <= 8:
                core_str = "  ".join([f"Core {i}: {c:.1f}%" for i, c in enumerate(cpu['per_core'])])
                print(f"      {core_str}")
            
            # Memory
            mem_bar = "█" * int(mem['percent'] / 5) + "░" * (20 - int(mem['percent'] / 5))
            print(f"Mem:  {mem_bar} {mem['percent']:.1f}% ({mem['used_gb']:.1f}/{mem['total_gb']:.1f} GB)")
            
            # Disk (main partition)
            if disk['partitions']:
                root = next((p for p in disk['partitions'] if p['mountpoint'] == '/'), disk['partitions'][0])
                disk_bar = "█" * int(root['percent'] / 5) + "░" * (20 - int(root['percent'] / 5))
                print(f"Disk: {disk_bar} {root['percent']:.1f}% ({root['used_gb']:.1f}/{root['total_gb']:.1f} GB) {root['mountpoint']}")
            
            # Network
            if net:
                print(f"Net:  ▲ {net.get('bytes_sent_mb', 0):.1f} MB/s  ▼ {net.get('bytes_recv_mb', 0):.1f} MB/s")
            
            # Processes
            print("\nTop Processes (by CPU):")
            print(f"{'PID':>6} {'USER':<10} {'CPU%':>6} {'MEM%':>6} {'COMMAND':<30}")
            print("-" * 80)
            for p in processes[:8]:
                pid = p.get('pid', 0)
                user = (p.get('username', '')[:8] + '..') if len(p.get('username', '')) > 8 else p.get('username', '')
                cpu_pct = p.get('cpu_percent', 0)
                mem_pct = p.get('memory_percent', 0)
                name = (p.get('name', '')[:28] + '..') if len(p.get('name', '')) > 28 else p.get('name', '')
                print(f"{pid:>6} {user:<10} {cpu_pct:>6.1f} {mem_pct:>6.1f} {name:<30}")
            
            print("=" * 80)
            print("Press Ctrl+C to exit")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\nDashboard stopped.")


def print_snapshot(json_output=False):
    """Print one-time snapshot"""
    cpu = get_cpu_stats()
    mem = get_memory_stats()
    disk = get_disk_stats()
    net = get_network_stats()
    processes = get_processes(limit=20, sort_by='cpu')
    
    if json_output:
        snapshot = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'cpu': cpu,
            'memory': mem,
            'disk': disk,
            'network': net,
            'processes': processes[:10]
        }
        print(json.dumps(snapshot, indent=2))
    else:
        print(f"Snapshot at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"CPU: {cpu['total_percent']:.1f}%")
        print(f"Memory: {mem['percent']:.1f}% ({mem['used_gb']:.1f}/{mem['total_gb']:.1f} GB)")
        if disk['partitions']:
            root = next((p for p in disk['partitions'] if p['mountpoint'] == '/'), disk['partitions'][0])
            print(f"Disk (/): {root['percent']:.1f}%")
        if processes:
            print(f"\nTop 5 processes:")
            for i, p in enumerate(processes[:5]):
                print(f"  {i+1}. {p.get('name', '')} (PID: {p.get('pid', '')}) - CPU: {p.get('cpu_percent', 0):.1f}%, MEM: {p.get('memory_percent', 0):.1f}%")


def print_top(sort_by='cpu', limit=10, json_output=False):
    """Print top processes"""
    processes = get_processes(limit=limit, sort_by=sort_by)
    
    if json_output:
        print(json.dumps(processes, indent=2))
    else:
        print(f"Top {limit} processes by {sort_by}:")
        print(f"{'PID':>6} {'USER':<10} {'CPU%':>6} {'MEM%':>6} {'COMMAND':<30}")
        print("-" * 80)
        for p in processes:
            pid = p.get('pid', 0)
            user = (p.get('username', '')[:8] + '..') if len(p.get('username', '')) > 8 else p.get('username', '')
            cpu_pct = p.get('cpu_percent', 0)
            mem_pct = p.get('memory_percent', 0)
            name = (p.get('name', '')[:28] + '..') if len(p.get('name', '')) > 28 else p.get('name', '')
            print(f"{pid:>6} {user:<10} {cpu_pct:>6.1f} {mem_pct:>6.1f} {name:<30}")


def main():
    parser = argparse.ArgumentParser(description='Process Monitor Dashboard')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Dashboard command
    dash_parser = subparsers.add_parser('dashboard', help='Start interactive real-time dashboard')
    dash_parser.add_argument('--interval', type=int, default=2, help='Refresh interval in seconds (default: 2)')
    dash_parser.add_argument('--simple', action='store_true', help='Simplified view (no per-core/disk details)')
    
    # Snapshot command
    snap_parser = subparsers.add_parser('snapshot', help='Print a one-time system snapshot')
    snap_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Top command
    top_parser = subparsers.add_parser('top', help='Show top processes')
    top_parser.add_argument('--by', choices=['cpu', 'memory', 'name'], default='cpu', help='Sort by (default: cpu)')
    top_parser.add_argument('--limit', type=int, default=10, help='Number of processes (default: 10)')
    top_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Monitor command (simplified)
    mon_parser = subparsers.add_parser('monitor', help='Monitor a specific process')
    mon_parser.add_argument('--pid', type=int, required=True, help='Process ID to monitor')
    mon_parser.add_argument('--interval', type=int, default=2, help='Refresh interval (default: 2)')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show system-wide statistics')
    stats_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Alert command (simplified)
    alert_parser = subparsers.add_parser('alert', help='Check for resource alerts')
    alert_parser.add_argument('--threshold-cpu', type=float, default=90, help='CPU alert threshold %% (default: 90)')
    alert_parser.add_argument('--threshold-memory', type=float, default=85, help='Memory alert threshold %% (default: 85)')
    
    # Help command
    help_parser = subparsers.add_parser('help', help='Show help')
    
    args = parser.parse_args()
    
    if not args.command or args.command == 'help':
        parser.print_help()
        return
    
    try:
        if args.command == 'dashboard':
            print_dashboard(interval=args.interval, simple=args.simple)
        elif args.command == 'snapshot':
            print_snapshot(json_output=args.json)
        elif args.command == 'top':
            print_top(sort_by=args.by, limit=args.limit, json_output=args.json)
        elif args.command == 'monitor':
            print(f"Monitoring PID {args.pid} (refresh: {args.interval}s)")
            print("Press Ctrl+C to stop")
            try:
                while True:
                    proc = psutil.Process(args.pid)
                    info = proc.as_dict(['pid', 'name', 'cpu_percent', 'memory_percent', 'num_threads'])
                    print(f"PID: {info['pid']} | Name: {info.get('name', 'N/A')} | CPU: {info.get('cpu_percent', 0):.1f}% | "
                          f"MEM: {info.get('memory_percent', 0):.1f}% | Threads: {info.get('num_threads', 0)}")
                    time.sleep(args.interval)
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                print(f"Error: {e}")
            except KeyboardInterrupt:
                print("\nMonitoring stopped.")
        elif args.command == 'stats':
            cpu = get_cpu_stats()
            mem = get_memory_stats()
            disk = get_disk_stats()
            net = get_network_stats()
            
            if args.json:
                stats = {
                    'cpu': cpu,
                    'memory': mem,
                    'disk': disk,
                    'network': net
                }
                print(json.dumps(stats, indent=2))
            else:
                print(f"CPU: {cpu['total_percent']:.1f}%")
                print(f"Memory: {mem['percent']:.1f}% ({mem['used_gb']:.1f}/{mem['total_gb']:.1f} GB)")
                if disk['partitions']:
                    for p in disk['partitions'][:3]:
                        print(f"Disk {p['mountpoint']}: {p['percent']:.1f}%")
                if net:
                    print(f"Network: Sent: {net.get('bytes_sent_mb', 0):.1f} MB, Recv: {net.get('bytes_recv_mb', 0):.1f} MB")
        elif args.command == 'alert':
            cpu = get_cpu_stats()
            mem = get_memory_stats()
            
            alerts = []
            if cpu['total_percent'] > args.threshold_cpu:
                alerts.append(f"CPU usage {cpu['total_percent']:.1f}% > {args.threshold_cpu}% threshold")
            if mem['percent'] > args.threshold_memory:
                alerts.append(f"Memory usage {mem['percent']:.1f}% > {args.threshold_memory}% threshold")
            
            if alerts:
                print("ALERTS:")
                for alert in alerts:
                    print(f"  ⚠ {alert}")
            else:
                print("No alerts - system within thresholds.")
    
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()