#!/usr/bin/env python3
"""
Orchestrates the full watchdog pipeline:
  1. Run all 7 scanners
  2. Aggregate results  (outputs score_delta)
  3. Generate dashboard HTML
  4. Archive daily log to data/logs/YYYY-MM-DD_HH-MM_scan.json
  5. Send Feishu notification (notify_feishu.py)
"""
import os
import sys
import subprocess
import json
import shutil
from datetime import datetime


def run_script(script_path: str) -> bool:
    """Run a Python script, return True on success."""
    if not os.path.exists(script_path):
        print(f"WARN: {os.path.basename(script_path)} not found, skipping")
        return False
    print(f"Running {os.path.basename(script_path)}...")
    result = subprocess.run([sys.executable, script_path], cwd=os.path.dirname(script_path))
    if result.returncode != 0:
        print(f"WARN: {os.path.basename(script_path)} exited with code {result.returncode}")
        return False
    return True


def archive_daily_log(data_dir: str):
    """Copy all latest_*.json + latest_status.json into data/logs/YYYY-MM-DD_HH-MM/ folder."""
    now = datetime.now()
    log_folder_name = now.strftime("%Y-%m-%d_%H-%M")
    logs_dir = os.path.join(data_dir, "logs", log_folder_name)
    os.makedirs(logs_dir, exist_ok=True)

    import glob
    for fpath in glob.glob(os.path.join(data_dir, "latest_*.json")):
        shutil.copy2(fpath, logs_dir)

    # Keep only last 30 daily logs (each run = 1 folder)
    parent_logs = os.path.join(data_dir, "logs")
    all_folders = sorted([
        d for d in os.listdir(parent_logs)
        if os.path.isdir(os.path.join(parent_logs, d))
    ])
    while len(all_folders) > 30:
        oldest = os.path.join(parent_logs, all_folders.pop(0))
        shutil.rmtree(oldest, ignore_errors=True)

    print(f"Daily log archived to: {logs_dir}")
    return logs_dir


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    scanners = [
        "scan_heartbeat.py",
        "scan_standards.py",
        "scan_memory.py",
        "scan_cron.py",
        "scan_shared.py",
        "scan_comm.py",
        "scan_security.py",
    ]

    print("=" * 60)
    print(f"🛡️  OpenClaw 安全卫士（openclaw-watchdog）  |  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    for s in scanners:
        run_script(os.path.join(script_dir, s))

    print("\nAggregating results...")
    run_script(os.path.join(script_dir, "aggregate_watchdog.py"))

    print("\nGenerating dashboard...")
    run_script(os.path.join(script_dir, "generate_dashboard.py"))

    # Archive daily log snapshot
    data_dir = os.path.join(os.path.dirname(script_dir), "data")
    try:
        archive_daily_log(data_dir)
    except Exception as e:
        print(f"WARN: Daily log archiving failed: {e}")

    # Print local summary
    latest_file = os.path.join(data_dir, "latest_status.json")
    if os.path.exists(latest_file):
        with open(latest_file, "r", encoding="utf-8") as f:
            status = json.load(f)
        score = status.get("global_score", 0)
        score_delta = status.get("score_delta", 0)
        open_issues = status.get("stats", {}).get("current_open", 0)
        delta_str = f" (↑+{score_delta})" if score_delta > 0 else (f" (↓{score_delta})" if score_delta < 0 else "")
        print(f"\n✅ 扫描完成  健康分: {score}/100{delta_str}  待处理: {open_issues} 个")

    # Send Feishu notification
    notify_script = os.path.join(script_dir, "notify_feishu.py")
    print("\nSending Feishu notification...")
    run_script(notify_script)

    # Apply GREEN auto-fixes (safe, non-business-logic only)
    green_script = os.path.join(script_dir, "fix_green.py")
    print("\nApplying GREEN auto-fixes...")
    run_script(green_script)

    print("=" * 60)
    print("Pipeline done.")
    print("=" * 60)


if __name__ == "__main__":
    main()
