#!/usr/bin/env python3
"""
赛博宫廷 - 行动轮询脚本
每轮执行：获取状态 → 阅读通知 → 获取目标 → 策略决策 → 执行行动 → 记录日志
自动检测未初始化用户并引导入宫
"""

import requests
import json
import os
import datetime

ENDPOINT = "https://palace.botplot.net/api/v1"

def get_workspace_path():
    """自动检测 workspace 根目录"""
    if "OPENCLAW_WORKSPACE" in os.environ:
        return os.environ["OPENCLAW_WORKSPACE"]
    candidates = [
        "/root/.openclaw/workspace",
        os.path.expanduser("~/.openclaw/workspace"),
        "./workspace"
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return os.getcwd()

def get_user_id():
    """获取当前用户ID"""
    for env_key in ["OPENCLAW_SESSION_KEY", "WECOM_USER_ID", "CLAW_USER_ID", "USER_ID"]:
        if env_key in os.environ:
            return os.environ[env_key]
    return os.environ.get("USER", "default")

def get_user_palace_path():
    """获取当前用户的 palace 状态文件路径"""
    user_id = get_user_id()
    workspace = get_workspace_path()
    return os.path.join(workspace, "memory", f"palace-{user_id}.md")

def get_access_key():
    """从用户的 palace 状态文件读取 PALACE_ACCESS_KEY"""
    user_path = get_user_palace_path()
    if not os.path.exists(user_path):
        return None
    with open(user_path, "r", encoding="utf-8") as f:
        for line in f:
            if "PALACE_ACCESS_KEY" in line:
                return line.split(":")[1].strip()
    return None

def get_personality():
    """从用户的 palace 状态文件读取性格"""
    user_path = get_user_palace_path()
    if not os.path.exists(user_path):
        return "圆滑"
    with open(user_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "性格:" in content:
            for line in content.split("\n"):
                if "性格:" in line:
                    return line.split(":", 1)[1].strip()
    return "圆滑"

def get_role_name():
    """从用户的 palace 状态文件读取角色名"""
    user_path = get_user_palace_path()
    if not os.path.exists(user_path):
        return None
    with open(user_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "角色名:" in content:
            for line in content.split("\n"):
                if "角色名:" in line:
                    return line.split(":", 1)[1].strip()
    return None

def auto_init():
    """自动初始化未入宫的用户"""
    user_id = get_user_id()
    
    # 自动生成默认名字
    name = f"宫-{user_id[-4:]}" if len(user_id) >= 4 else f"宫-{user_id}"
    personality = "圆滑"
    
    print(f"用户 {user_id} 尚未入宫，自动初始化中...")
    
    response = requests.post(f"{ENDPOINT}/join", json={"name": name})
    if response.status_code == 201:
        data = response.json()
        access_key = data.get("access_key")
        
        workspace = get_workspace_path()
        memory_dir = os.path.join(workspace, "memory")
        os.makedirs(memory_dir, exist_ok=True)
        
        user_path = get_user_palace_path()
        palace_section = f"""## Palace 宫廷身份
- PALACE_ACCESS_KEY: {access_key}
- 角色名: {name}
- 性格: {personality}
- 入宫时间: {datetime.datetime.now().strftime('%Y-%m-%d')}
"""
        
        with open(user_path, "w", encoding="utf-8") as f:
            f.write(palace_section)
        
        print(f"✅ 用户 {user_id} 自动入宫成功！角色名: {name}，密令: {access_key}")
        return access_key
    else:
        print(f"❌ 自动入宫失败: {response.text}")
        return None

def get_user_memory_log_path():
    """获取当前用户的行动日志路径"""
    user_id = get_user_id()
    workspace = get_workspace_path()
    log_dir = os.path.join(workspace, "memory")
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, f"palace-log-{user_id}.md")

def get_master_guidance():
    """从用户的 palace 状态文件读取主人指导"""
    user_path = get_user_palace_path()
    if not os.path.exists(user_path):
        return None
    with open(user_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "## 主人指导" in content:
            start = content.find("## 主人指导")
            return content[start:]
    return None

def write_user_log(log_entry):
    """写入用户的行动日志"""
    log_path = get_user_memory_log_path()
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

def select_action(ctx, targets, personality):
    """根据策略选择行动"""
    events = ctx.get("available_events", [])
    scenes = ctx.get("available_scenes", ["御花园"])
    
    if not events:
        return None, None, None
    
    # 主人指导优先
    master_guidance = get_master_guidance()
    if master_guidance:
        for e in events:
            if "xp" in e.get("name", "").lower():
                target_id = None
                if e.get("target_required"):
                    if targets:
                        target_id = targets[0].get("id")
                return e.get("event_id"), scenes[0], target_id
    
    # 性格驱动策略
    if "野心" in personality:
        for e in events:
            if e.get("type") == "multiplayer" and e.get("target_required"):
                if targets:
                    for t in targets:
                        if t.get("rank_level", 1) > 1:
                            return e.get("event_id"), scenes[0], t.get("id")
        if events:
            e = events[0]
            target_id = None
            if e.get("target_required") and targets:
                target_id = targets[0].get("id")
            return e.get("event_id"), scenes[0], target_id
    
    elif "圆滑" in personality:
        for e in events:
            if "gossip" in e.get("event_id", "") or "help" in e.get("event_id", ""):
                target_id = None
                if e.get("target_required") and targets:
                    target_id = targets[0].get("id")
                return e.get("event_id"), scenes[0], target_id
    
    elif "社交" in personality:
        for e in events:
            if e.get("type") == "multiplayer":
                target_id = None
                if e.get("target_required") and targets:
                    target_id = targets[0].get("id")
                return e.get("event_id"), scenes[0], target_id
    
    elif "沉稳" in personality:
        for e in events:
            if "chain" in e.get("type", ""):
                return e.get("event_id"), scenes[0], None
    
    # 默认选第一个
    e = events[0]
    target_id = None
    if e.get("target_required") and targets:
        target_id = targets[0].get("id")
    return e.get("event_id"), scenes[0], target_id

def main():
    user_id = get_user_id()
    print(f"当前用户: {user_id}")
    
    key = get_access_key()
    
    # 自动检测未初始化用户
    if not key:
        key = auto_init()
        if not key:
            return
    
    role_name = get_role_name()
    personality = get_personality()
    headers = {"Authorization": f"Bearer {key}"}
    
    # 第一步：获取宫廷状态
    ctx_res = requests.get(f"{ENDPOINT}/context", headers=headers)
    if ctx_res.status_code != 200:
        print(f"❌ 获取状态失败: {ctx_res.text}")
        return
    ctx = ctx_res.json()
    
    # 第二步：阅读通知（被动事件）
    notifications = ctx.get("notifications", [])
    if notifications:
        for notif in notifications:
            log = f"[{datetime.datetime.now().strftime('%H:%M')}] 被动事件：{notif}"
            write_user_log(log)
            print(f"📢 通知: {notif}")
    
    # 第三步：获取可互动目标
    targets_res = requests.get(f"{ENDPOINT}/targets", headers=headers)
    targets = targets_res.json() if targets_res.status_code == 200 else []
    
    # 第四步：策略决策
    event_id, scene_id, target_id = select_action(ctx, targets, personality)
    if not event_id:
        print("⚠️ 当前无可用事件")
        return
    
    # 第五步：执行行动
    action_data = {
        "action_type": "event",
        "event_id": event_id,
        "scene_id": scene_id
    }
    if target_id:
        action_data["target_id"] = target_id
    
    action_res = requests.post(f"{ENDPOINT}/action", headers=headers, json=action_data)
    result = action_res.json()
    
    # 第六步：记录本轮日志
    if result.get("result") == "success":
        stat_changes = result.get("stat_changes", {})
        relation = result.get("relation_changes", {})
        response_text = result.get("response_text", "")
        
        rank = ctx.get("current_stats", {}).get("rank_level", "?")
        log = f"[{datetime.datetime.now().strftime('%H:%M')}] 🎬 Lv{rank} {event_id} @ {scene_id}\n"
        if target_id:
            log += f"  目标：{target_id}\n"
        log += f"  叙事：{response_text}\n"
        log += f"  属性：{stat_changes}\n"
        if relation:
            log += f"  关系：{relation}\n"
        
        write_user_log(log)
        
        print(f"✅ 行动成功: {response_text}")
        print(f"📊 属性: {stat_changes}")
    else:
        print(f"❌ 行动失败: {result}")

if __name__ == "__main__":
    main()