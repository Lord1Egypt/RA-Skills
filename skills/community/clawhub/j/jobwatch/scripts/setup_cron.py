#!/usr/bin/env python3
"""注册 3 个定时任务到 OpenClaw cron（单 agent 模式：唤醒的就是安装本 skill 的 agent）。

用法（须经主人同意后运行）：
  python3 scripts/setup_cron.py --agent <你的agentId> [--tz <IANA时区>]
改完提醒主人运行: openclaw gateway restart
"""
import argparse
import json
import os
import time
import uuid
from pathlib import Path

from common import ROOT, SKILL_DIR

OC = Path(os.environ.get("OPENCLAW_DIR", str(Path.home() / ".openclaw")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", required=True)
    ap.add_argument("--tz", default=None)
    args = ap.parse_args()
    tz = args.tz
    if not tz:
        lt = Path("/etc/localtime")
        tz = str(lt.readlink()).split("zoneinfo/")[-1] if lt.is_symlink() else "UTC"

    p = OC / "cron" / "jobs.json"
    p.parent.mkdir(exist_ok=True)
    data = json.loads(p.read_text()) if p.exists() else {"version": 1, "jobs": []}
    bak = p.with_suffix(f".json.bak.jobwatch-{int(time.time())}")
    bak.write_text(json.dumps(data, ensure_ascii=False))
    names = {j["name"] for j in data["jobs"]}

    def job(name, expr, message):
        return {"id": str(uuid.uuid4()), "agentId": args.agent, "name": name,
                "enabled": True, "deleteAfterRun": False,
                "createdAtMs": int(time.time() * 1000),
                "schedule": {"tz": tz, "expr": expr, "kind": "cron"},
                "sessionTarget": "isolated", "wakeMode": "now",
                "payload": {"kind": "agentTurn", "message": message},
                "delivery": {"mode": "none"}, "state": {}}

    cycle = (f"定时唤醒：按 jobwatch skill 的工作循环（{SKILL_DIR}/SKILL.md 的 Work Cycle 一节）"
             f"执行：cd {ROOT} && python3 {SKILL_DIR}/scripts/pipeline.py，"
             f"随后按 SKILL.md 处理待判清单与 outbox。一切正常则静默结束。")
    plan = [("jobwatch-cycle", "*/15 * * * 1-5", cycle),
            ("jobwatch-cycle-weekend", "0 * * * 0,6", cycle),
            ("jobwatch-digest", "0 9 * * *",
             f"定时唤醒：cd {ROOT} && python3 {SKILL_DIR}/scripts/daily_digest.py，"
             f"随后按 jobwatch SKILL.md 处理 outbox。空队列静默退出是正常的。")]
    added = []
    for name, expr, msg in plan:
        if name not in names:
            data["jobs"].append(job(name, expr, msg))
            added.append(f"{name} ({expr})")
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(json.dumps({"added": added, "tz": tz, "backup": str(bak),
                      "next_step": "openclaw gateway restart"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
