#!/usr/bin/env python3
"""Monitor local RAG indexing progress, logs, and errors.

Usage:
    monitor.py              # Show current status
    monitor.py --watch      # Auto-refresh every 10s
    monitor.py --log        # Show last 50 log lines
    monitor.py --log -n 100 # Show last N log lines
    monitor.py --errors     # Show only errors from log
    monitor.py --git        # Show git history (checkpoints)
"""

import argparse
import os
import subprocess
import sys
import time

DB_DIR = os.path.expanduser("~/.local/share/local-rag/chromadb")
LOG_FILE = os.path.expanduser("~/.local/share/local-rag/index-batch.log")
LOCK_FILE = os.path.expanduser("~/.local/share/local-rag/index.lock")


def get_db_stats():
    """Get ChromaDB collection counts."""
    try:
        import chromadb
        c = chromadb.PersistentClient(path=DB_DIR)
        parents = c.get_or_create_collection("parents").count()
        children = c.get_or_create_collection("children").count()
        return parents, children
    except Exception as e:
        return None, str(e)


def get_process_info():
    """Check if indexing is running."""
    try:
        result = subprocess.run(
            ["ps", "aux"], capture_output=True, text=True, timeout=5
        )
        lines = [l for l in result.stdout.splitlines() if "index.py" in l and "grep" not in l]
        if lines:
            parts = lines[0].split()
            pid = parts[1]
            cpu = parts[2]
            mem = parts[3]
            rss_mb = int(parts[5]) / 1024
            elapsed = parts[9]
            return {"running": True, "pid": pid, "cpu": cpu, "mem": mem, "rss_mb": rss_mb, "elapsed": elapsed}
    except Exception:
        pass
    return {"running": False}


def get_system_mem():
    """Get system memory info."""
    try:
        with open("/proc/meminfo") as f:
            lines = f.readlines()
        info = {}
        for line in lines:
            parts = line.split()
            if "MemTotal" in line:
                info["total_mb"] = int(parts[1]) / 1024
            elif "MemAvailable" in line:
                info["available_mb"] = int(parts[1]) / 1024
            elif "SwapTotal" in line:
                info["swap_total_mb"] = int(parts[1]) / 1024
            elif "SwapFree" in line:
                info["swap_free_mb"] = int(parts[1]) / 1024
        return info
    except Exception:
        return {}


def get_git_log():
    """Get git log of checkpoints."""
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-10"],
            capture_output=True, text=True, cwd=DB_DIR, timeout=5
        )
        return result.stdout.strip().splitlines()
    except Exception:
        return ["(git not available)"]


def get_disk_usage():
    """Get DB size on disk."""
    try:
        result = subprocess.run(
            ["du", "-sh", DB_DIR], capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip().split()[0]
    except Exception:
        return "?"


def show_status():
    """Print current status."""
    proc = get_process_info()
    parents, children = get_db_stats()
    mem = get_system_mem()
    disk = get_disk_usage()

    print("╔══════════════════════════════════════════╗")
    print("║     📊 Local RAG Index Monitor           ║")
    print("╠══════════════════════════════════════════╣")

    # Process status
    if proc["running"]:
        print(f"║ 🔵 RUNNING  PID {proc['pid']}  CPU {proc['cpu']}%  MEM {proc['rss_mb']:.0f}MB")
    else:
        print(f"║ ⚪ IDLE")

    # DB stats
    if parents is not None:
        print(f"║ Parents: {parents:,}  Children: {children:,}")
    else:
        print(f"║ DB: {children}")

    # Disk
    print(f"║ Disk: {disk}")

    # Memory
    if mem:
        used = mem.get("total_mb", 0) - mem.get("available_mb", 0)
        pct = (used / mem["total_mb"] * 100) if mem["total_mb"] > 0 else 0
        print(f"║ RAM: {used:.0f}/{mem['total_mb']:.0f}MB ({pct:.0f}%)  Available: {mem.get('available_mb', 0):.0f}MB")
        swap_used = mem.get("swap_total_mb", 0) - mem.get("swap_free_mb", 0)
        print(f"║ Swap: {swap_used:.0f}/{mem.get('swap_total_mb', 0):.0f}MB")

    # Lock
    locked = "🔒 Locked" if os.path.exists(LOCK_FILE) else "🔓 No lock"
    print(f"║ {locked}")

    print("╚══════════════════════════════════════════╝")


def show_log(lines=50, errors_only=False):
    """Show log file contents."""
    if not os.path.exists(LOG_FILE):
        print("(no log file yet)")
        return

    with open(LOG_FILE) as f:
        all_lines = f.readlines()

    if errors_only:
        all_lines = [l for l in all_lines if "❌" in l or "ERROR" in l or "FAILED" in l or "OOM" in l or "SIGKILL" in l]

    for line in all_lines[-lines:]:
        print(line.rstrip())


def show_git():
    """Show git checkpoint history."""
    commits = get_git_log()
    print("Git checkpoints (newest first):")
    for c in commits:
        print(f"  {c}")


def main():
    parser = argparse.ArgumentParser(description="Monitor local RAG indexing")
    parser.add_argument("--watch", action="store_true", help="Auto-refresh every 10s")
    parser.add_argument("--log", action="store_true", help="Show log")
    parser.add_argument("-n", type=int, default=50, help="Number of log lines")
    parser.add_argument("--errors", action="store_true", help="Show only errors")
    parser.add_argument("--git", action="store_true", help="Show git checkpoints")
    args = parser.parse_args()

    if args.log:
        show_log(args.n, args.errors)
    elif args.git:
        show_git()
    elif args.watch:
        while True:
            os.system("clear")
            show_status()
            print()
            show_git()
            print("\nRefreshing in 10s... (Ctrl+C to stop)")
            try:
                time.sleep(10)
            except KeyboardInterrupt:
                break
    else:
        show_status()


if __name__ == "__main__":
    main()
