#!/usr/bin/env python3
"""Mega Pipeline — 全闭环自动化执行引擎"""
import json, os, subprocess, sys, time, uuid
from datetime import datetime

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
STATE_DIR = os.path.join(WORKSPACE, "state")
LOG_DIR = os.path.join(WORKSPACE, "state", "pipeline_logs")
os.makedirs(LOG_DIR, exist_ok=True)

SCRIPTS = {
    "hunter_scan":    "python3 ~/.openclaw/workspace/skills/hunter-plus-agent/scripts/hunter_scan.py",
    "dashboard":      "python3 ~/.openclaw/workspace/skills/dashboard-live/scripts/live_dashboard.py --json",
    "profit_report":  "python3 ~/.openclaw/workspace/skills/profit-agent/scripts/order_manager.py --report",
    "health_check":   "bash ~/.openclaw/workspace/skills/resilience-agent/scripts/health_monitor.sh",
    "orchestrator":   "python3 ~/.openclaw/workspace/skills/async-orchestrator/scripts/orchestrator.py --list",
}

def run_step(name, cmd, timeout=30):
    print(f"  ▶ [{name}]  执行中...", end=" ", flush=True)
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        status = "✅" if r.returncode == 0 else "⚠️"
        output = r.stdout[:200] + (r.stderr[:100] if r.stderr else "")
        print(f"{status} (code={r.returncode})")
        return {"name": name, "status": status, "output": output, "success": r.returncode == 0}
    except subprocess.TimeoutExpired:
        print("⏰ 超时")
        return {"name": name, "status": "⏰", "output": "timeout", "success": False}
    except Exception as e:
        print(f"💥 {e}")
        return {"name": name, "status": "💥", "output": str(e), "success": False}

def run_pipeline():
    pipeline_id = f"pipe_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:4]}"
    print(f"\n{'='*50}")
    print(f"🚀 MEGA PIPELINE [{pipeline_id}]")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")
    
    steps = ["hunter_scan", "orchestrator", "dashboard", "profit_report", "health_check"]
    results = []
    
    for step_name in steps:
        cmd = SCRIPTS[step_name]
        r = run_step(step_name, cmd)
        results.append(r)
    
    success = sum(1 for r in results if r["success"])
    print(f"\n{'='*50}")
    print(f"🏁 管道完成: {success}/{len(results)} 步骤成功")
    print(f"{'='*50}\n")
    
    # 保存日志
    log = {
        "pipeline_id": pipeline_id,
        "timestamp": datetime.now().isoformat(),
        "steps": results,
        "summary": f"{success}/{len(results)}"
    }
    log_path = os.path.join(LOG_DIR, f"{pipeline_id}.json")
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)
    print(f"  📝 日志: {log_path}")
    
    return success == len(results)

def show_status():
    logs = sorted([f for f in os.listdir(LOG_DIR) if f.endswith(".json")], reverse=True)[:10]
    print(f"=== 📊 管道运行记录 ({len(logs)}) ===")
    for log_file in logs:
        path = os.path.join(LOG_DIR, log_file)
        with open(path) as f:
            data = json.load(f)
        ts = data["timestamp"][:19].replace("T", " ")
        print(f"  {ts} | {data['pipeline_id']} | {data['summary']}")

def main():
    args = sys.argv[1:]
    if "--status" in args:
        show_status()
    else:
        run_pipeline()

if __name__ == "__main__":
    main()
