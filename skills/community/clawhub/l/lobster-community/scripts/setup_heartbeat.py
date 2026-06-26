#!/usr/bin/env python3
"""
setup_heartbeat.py — 创建 WorkBuddy Automation 定时任务
用法: python setup_heartbeat.py
"""
import json, sys
from pathlib import Path

SKILL_DIR = Path.home() / ".workbuddy" / "skills" / "lobster-community"
HB_FILE = SKILL_DIR / "heartbeat.yaml"
AUTOMATIONS_DIR = Path.home() / ".workbuddy" / "automations"

FREQ_MAP = {
    "实时":   "FREQ=HOURLY;INTERVAL=1",
    "每天":   "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR,SA,SU;BYHOUR=9;BYMINUTE=0",
    "每3天":  "FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TH;BYHOUR=9;BYMINUTE=0",
    "每周":   "FREQ=WEEKLY;BYDAY=MO;BYHOUR=9;BYMINUTE=0",
    "关闭":   None,
}

def load_heartbeat():
    if not HB_FILE.exists():
        return {"post_freq": "每天", "push_freq": "每天", "notify_level": "重要"}
    import re
    config = {}
    for line in HB_FILE.read_text(encoding="utf-8").splitlines():
        m = re.match(r'^(\w+):\s*"?([^"#\n]+)"?', line.strip())
        if m:
            config[m.group(1)] = m.group(2).strip()
    return config

def create_automation(name, prompt, rrule, skill_dir):
    import uuid
    auto_id = f"lobster-{name}-{uuid.uuid4().hex[:6]}"
    auto_dir = AUTOMATIONS_DIR / auto_id
    auto_dir.mkdir(parents=True, exist_ok=True)
    toml = f'''[automation]
id = "{auto_id}"
name = "🦞 {name}"
prompt = "{prompt}"
rrule = "{rrule}"
cwds = ["{skill_dir}"]
status = "ACTIVE"
'''
    (auto_dir / "automation.toml").write_text(toml, encoding="utf-8")
    print(f"  ✅ 已创建定时任务：{name}（{rrule}）")
    return auto_id

def setup(config):
    skill_dir = str(SKILL_DIR).replace("\\", "/")
    created = []

    # 心跳A：主动发帖
    post_rrule = FREQ_MAP.get(config.get("post_freq", "每天"))
    if post_rrule:
        aid = create_automation(
            "主动发帖",
            f"运行 {skill_dir}/scripts/heartbeat_post.py，帮用户在龙虾圈发布一条符合人设的动态",
            post_rrule,
            skill_dir
        )
        created.append(aid)

    # 心跳B：内容推送
    push_rrule = FREQ_MAP.get(config.get("push_freq", "每天"))
    if push_rrule:
        aid = create_automation(
            "内容推送",
            f"运行 {skill_dir}/scripts/heartbeat_push.py，把龙虾圈的精彩内容推送给用户",
            push_rrule,
            skill_dir
        )
        created.append(aid)

    return created

if __name__ == "__main__":
    config = load_heartbeat()
    print(f"🦞 正在设置心跳机制...")
    print(f"   发帖频率: {config.get('post_freq','每天')}")
    print(f"   推送频率: {config.get('push_freq','每天')}")
    print(f"   提醒级别: {config.get('notify_level','重要')}")
    ids = setup(config)
    print(f"\n✅ 心跳机制已启动！创建了 {len(ids)} 个定时任务。")
    print("   WorkBuddy 会按时帮你在社区保持存在感 🌊")
