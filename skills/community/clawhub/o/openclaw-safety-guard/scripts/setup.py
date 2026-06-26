#!/usr/bin/env python3
"""
openclaw-watchdog one-time setup script.

Usage (called by the agent after clawhub install):
    python3 {baseDir}/scripts/setup.py --receive_id <feishu_open_id>

What this does:
  1. Reads FEISHU_APP_ID + FEISHU_APP_SECRET from environment
  2. Writes config.json with the caller's receive_id
  3. Registers the daily cron job in .openclaw/state/cron/jobs.json
  4. Immediately runs run_pipeline.py (first scan + Feishu notification)
     → User receives their first health report within ~60 seconds
"""
import os
import sys
import json
import uuid
import shutil
import subprocess
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.path.join(SKILL_DIR, "config.json")
CONFIG_EXAMPLE_PATH = os.path.join(SKILL_DIR, "config.example.json")
FRONTEND_DIR = os.path.join(SKILL_DIR, "frontend")


# ── 1. Parse arguments ──────────────────────────────────────────────────────

def parse_args():
    receive_id = None
    cron_expr = "0 0 10 * * 1-5"   # default: weekdays 10:00 Asia/Shanghai
    cron_tz = "Asia/Shanghai"
    agent_id = "main"               # default agent to run the scan

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--receive_id" and i + 1 < len(args):
            receive_id = args[i + 1]; i += 2
        elif args[i] == "--cron" and i + 1 < len(args):
            cron_expr = args[i + 1]; i += 2
        elif args[i] == "--tz" and i + 1 < len(args):
            cron_tz = args[i + 1]; i += 2
        elif args[i] == "--agent" and i + 1 < len(args):
            agent_id = args[i + 1]; i += 2
        else:
            i += 1
    return receive_id, cron_expr, cron_tz, agent_id


# ── 2. Validate environment ──────────────────────────────────────────────────

def check_env():
    app_id = os.environ.get("FEISHU_APP_ID", "")
    app_secret = os.environ.get("FEISHU_APP_SECRET", "")
    missing = []
    if not app_id:
        missing.append("FEISHU_APP_ID")
    if not app_secret:
        missing.append("FEISHU_APP_SECRET")
    if missing:
        print(f"ERROR: Missing environment variables: {', '.join(missing)}")
        print("These should be set in your Gateway plist's EnvironmentVariables.")
        sys.exit(1)
    return app_id, app_secret


# ── 3. Prepare frontend deps ─────────────────────────────────────────────────

def ensure_frontend_deps():
    vite_bin = os.path.join(FRONTEND_DIR, "node_modules", ".bin", "vite")
    if os.path.exists(vite_bin):
        return

    npm_bin = shutil.which("npm")
    if not npm_bin:
        print("ERROR: npm is required for the first dashboard build, but was not found in PATH.")
        sys.exit(1)

    print("\n📦 Installing frontend dependencies for first dashboard build...")
    result = subprocess.run([npm_bin, "install"], cwd=FRONTEND_DIR)
    if result.returncode != 0:
        print("ERROR: npm install failed, aborting setup.")
        sys.exit(result.returncode)


# ── 4. Write config.json ─────────────────────────────────────────────────────

def write_config(receive_id: str):
    template_path = CONFIG_EXAMPLE_PATH if os.path.exists(CONFIG_EXAMPLE_PATH) else None

    if template_path:
        with open(template_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    else:
        # Minimal default config
        cfg = {
            "project_name": "OpenClaw 安全卫士",
            "workspace_root": ".",
            "agents": "auto",
            "security": {"checks": [
                {"id": "plist_permissions", "enabled": True, "target": "~/Library/LaunchAgents/ai.openclaw.gateway.plist"},
                {"id": "git_commit_lag", "enabled": True, "target": ".", "threshold_days": 7},
                {"id": "exec_approvals", "enabled": True, "target": "~/.openclaw/exec-approvals.json"},
                {"id": "api_key_in_git", "enabled": True, "target": ".", "patterns": ["sk-", "Bearer "]},
                {"id": "doctor_health", "enabled": True},
            ]},
            "memory": {"checks": [
                {"id": "memory_staleness", "enabled": True, "threshold_days": 14},
                {"id": "memory_bloat", "enabled": True, "memory_md_max_lines": 120},
            ]},
            "cron": {"target": ".openclaw/state/cron", "max_consecutive_failures": 3},
            "notify": {
                "enabled": True,
                "app_id_env": "FEISHU_APP_ID",
                "app_secret_env": "FEISHU_APP_SECRET",
                "receive_id_type": "open_id",
                "receive_id": "",
                "score_recovery_threshold": 3,
            },
        }

    cfg["notify"]["receive_id"] = receive_id
    cfg["notify"]["enabled"] = True

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    print(f"✅ config.json written (receive_id: {receive_id[:12]}...)")


# ── 5. Register cron job ─────────────────────────────────────────────────────

def find_cron_jobs_path():
    """Walk up from skill dir to find .openclaw/state/cron/jobs.json"""
    current = SKILL_DIR
    while current != os.path.expanduser("~") and current != "/":
        candidate = os.path.join(current, ".openclaw", "state", "cron", "jobs.json")
        if os.path.exists(candidate):
            return candidate
        # also check if .openclaw is current dir
        candidate2 = os.path.join(current, "state", "cron", "jobs.json")
        if os.path.exists(candidate2) and os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(current)))) == ".openclaw":
            return candidate2
        current = os.path.dirname(current)
    return None


def register_cron(cron_expr: str, cron_tz: str, agent_id: str):
    jobs_path = find_cron_jobs_path()
    if not jobs_path:
        print("WARN: Could not find .openclaw/state/cron/jobs.json, skipping cron registration")
        print("  You can manually add the cron job later via: openclaw cron add")
        return False

    with open(jobs_path, "r", encoding="utf-8") as f:
        jobs_data = json.load(f)

    jobs = jobs_data.get("jobs") or jobs_data.get("list") or []

    # Remove any existing watchdog job to avoid duplicates
    jobs = [j for j in jobs if "watchdog" not in j.get("name", "").lower()
            and "watchdog" not in j.get("id", "").lower()]

    # Build workspace path for the run command
    workspace_dir = SKILL_DIR
    for _ in range(4):  # go up from scripts/ → skill/ → skills/ → workspace/
        workspace_dir = os.path.dirname(workspace_dir)
    skill_rel = os.path.relpath(SCRIPT_DIR, workspace_dir)
    run_cmd = f"cd {workspace_dir} && python3 {os.path.join(skill_rel, 'run_pipeline.py')}"

    new_job = {
        "id": f"openclaw-watchdog-daily-{uuid.uuid4().hex[:8]}",
        "agentId": agent_id,
        "name": "openclaw-watchdog-daily",
        "enabled": True,
        "createdAtMs": int(datetime.now().timestamp() * 1000),
        "updatedAtMs": int(datetime.now().timestamp() * 1000),
        "schedule": {
            "kind": "cron",
            "expr": cron_expr,
            "tz": cron_tz,
        },
        "sessionTarget": "isolated",
        "wakeMode": "now",
        "payload": {
            "kind": "agentTurn",
            "message": f"执行 Watchdog 全链路扫描（含飞书通知）：{run_cmd}",
            "timeoutSeconds": 360,
        },
        "delivery": {"mode": "none", "channel": "last"},
    }

    jobs.append(new_job)
    if "jobs" in jobs_data:
        jobs_data["jobs"] = jobs
    else:
        jobs_data["list"] = jobs

    with open(jobs_path, "w", encoding="utf-8") as f:
        json.dump(jobs_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Cron job registered: {cron_expr} ({cron_tz})")
    print(f"   ⚠️  Remember to restart Gateway for cron to take effect: openclaw gateway restart")
    return True


# ── 6. Run first scan immediately ────────────────────────────────────────────

def run_first_scan():
    run_pipeline = os.path.join(SCRIPT_DIR, "run_pipeline.py")
    if not os.path.exists(run_pipeline):
        print("WARN: run_pipeline.py not found, skipping first scan")
        return
    print("\n🔍 Running first scan now (this takes ~30 seconds)...")
    result = subprocess.run([sys.executable, run_pipeline], cwd=SCRIPT_DIR)
    if result.returncode != 0:
        print("WARN: First scan exited with errors, check output above")
    else:
        print("✅ First scan complete — check your Feishu for the health report!")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 56)
    print("🛡️  OpenClaw 安全卫士（openclaw-watchdog）— Setup")
    print("=" * 56)

    receive_id, cron_expr, cron_tz, agent_id = parse_args()

    if not receive_id:
        print("ERROR: --receive_id is required")
        print("Usage: python3 setup.py --receive_id <your_feishu_open_id>")
        print("")
        print("The agent calling this script should pass the current")
        print("conversation sender's open_id as the receive_id.")
        sys.exit(1)

    # Validate env
    check_env()

    # Prepare frontend deps
    ensure_frontend_deps()

    # Write config
    print("\n📝 Writing config.json...")
    write_config(receive_id)

    # Register cron
    print("\n⏰ Registering daily cron job...")
    register_cron(cron_expr, cron_tz, agent_id)

    # Run first scan immediately
    run_first_scan()

    print("\n" + "=" * 56)
    print("Setup complete!")
    print(f"  Feishu notifications → {receive_id[:16]}...")
    print(f"  Daily scan schedule  → {cron_expr} ({cron_tz})")
    print("=" * 56)


if __name__ == "__main__":
    main()
