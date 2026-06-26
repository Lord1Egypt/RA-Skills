#!/usr/bin/env python3
"""Discord Thread 批量操作工具 - 供 project skill 调用"""

import argparse
import json
import sys
import urllib.request
import urllib.error


def api(method, path, token, data=None):
    """Discord API 调用"""
    url = f"https://discord.com/api/v10{path}"
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
        "User-Agent": "DiscordBot (https://openclaw.ai, 1.0)",
    }
    body = json.dumps(data, ensure_ascii=False).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            if not raw:
                return {}
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"API Error {e.code} {path}: {err}", file=sys.stderr)
        return None


def create_thread(token, channel_id, name, message, auto_archive=10080):
    """在指定 Channel 创建 Thread 并发送初始消息"""
    import time
    # 先发一条消息到频道
    msg = api("POST", f"/channels/{channel_id}/messages", token, {
        "content": f"📋 **新项目线程**: {name}"
    })
    if not msg or "id" not in msg:
        print(f"  ❌ 发送消息失败: channel {channel_id}", file=sys.stderr)
        return None
    time.sleep(0.3)
    # 基于该消息创建 Thread
    thread = api("POST", f"/channels/{channel_id}/messages/{msg['id']}/threads", token, {
        "name": name,
        "auto_archive_duration": auto_archive,
    })
    if not thread or "id" not in thread:
        print(f"  ❌ 创建 Thread 失败: {name}", file=sys.stderr)
        return None
    time.sleep(0.3)
    # 在 Thread 里发送初始任务
    api("POST", f"/channels/{thread['id']}/messages", token, {
        "content": message,
    })
    time.sleep(0.3)
    return thread


def create_threads_batch(token, project_name, assignments):
    """批量创建项目 Thread

    assignments: [{"agent_id": "laojun", "channel_id": "xxx", "role": "架构设计", "task": "..."}]
    """
    results = {}
    for a in assignments:
        thread_name = f"[{project_name}] {a['role']}"
        members = ", ".join(x["agent_id"] for x in assignments if x["agent_id"] != a["agent_id"])
        message = (
            f"📋 **项目**: {project_name}\n\n"
            f"**你的职责**: {a['role']}\n\n"
            f"**任务**: {a['task']}\n\n"
            f"**协作成员**: {members}\n\n"
            f"请开始工作，有问题随时沟通。"
        )
        thread = create_thread(token, a["channel_id"], thread_name, message)
        if thread and "id" in thread:
            results[a["agent_id"]] = {
                "thread_id": thread["id"],
                "thread_name": thread_name,
            }
            print(f"  ✅ {a['agent_id']} → {thread_name} (thread: {thread['id']})")
        else:
            print(f"  ❌ {a['agent_id']} → {thread_name} (创建失败)")
    return results


def get_latest_messages(token, thread_ids):
    """获取多个 Thread 的最新消息"""
    results = {}
    for agent_id, thread_id in thread_ids.items():
        msgs = api("GET", f"/channels/{thread_id}/messages?limit=1", token)
        if msgs:
            results[agent_id] = {
                "content": msgs[0].get("content", "")[:100],
                "timestamp": msgs[0].get("timestamp", ""),
                "author": msgs[0].get("author", {}).get("username", ""),
            }
        else:
            results[agent_id] = None
    return results


def load_openclaw_discord_config():
    """从 openclaw.json 提取 Discord 配置"""
    import os
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    with open(config_path) as f:
        config = json.load(f)

    discord = config.get("channels", {}).get("discord", {})
    accounts = discord.get("accounts", {})
    default_account = accounts.get("default", {})
    token = default_account.get("token", "")

    # 从 bindings 提取 agent -> channel 映射
    channel_map = {}
    for binding in config.get("bindings", []):
        agent_id = binding.get("agentId")
        match = binding.get("match", {})
        peer = match.get("peer", {})
        if peer.get("kind") == "channel" and agent_id:
            channel_map[agent_id] = peer["id"]

    guild_id = ""
    for gid in default_account.get("guilds", {}):
        guild_id = gid
        break

    return {
        "token": token,
        "guild_id": guild_id,
        "channel_map": channel_map,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Discord Thread 批量操作")
    sub = parser.add_subparsers(dest="command")

    # create: 从 JSON stdin 批量创建
    p_create = sub.add_parser("create", help="批量创建项目 Thread")
    p_create.add_argument("project_name", help="项目名")
    p_create.add_argument("--input", help="JSON 文件路径 (或 stdin)")

    # status: 查询 Thread 最新消息
    p_status = sub.add_parser("status", help="查询项目 Thread 状态")
    p_status.add_argument("--input", help="JSON 文件路径 (或 stdin)")

    # config: 输出当前 Discord 配置
    p_config = sub.add_parser("config", help="输出 OpenClaw Discord 配置")

    args = parser.parse_args()

    if args.command == "config":
        cfg = load_openclaw_discord_config()
        print(json.dumps(cfg, indent=2, ensure_ascii=False))

    elif args.command == "create":
        cfg = load_openclaw_discord_config()
        if args.input:
            with open(args.input) as f:
                assignments = json.load(f)
        else:
            assignments = json.load(sys.stdin)

        # 补充 channel_id
        for a in assignments:
            if "channel_id" not in a:
                a["channel_id"] = cfg["channel_map"].get(a["agent_id"], "")

        print(f"🚀 创建项目「{args.project_name}」Thread...")
        results = create_threads_batch(cfg["token"], args.project_name, assignments)
        print(json.dumps(results, indent=2, ensure_ascii=False))

    elif args.command == "status":
        cfg = load_openclaw_discord_config()
        if args.input:
            with open(args.input) as f:
                thread_ids = json.load(f)
        else:
            thread_ids = json.load(sys.stdin)
        results = get_latest_messages(cfg["token"], thread_ids)
        print(json.dumps(results, indent=2, ensure_ascii=False))

    else:
        parser.print_help()
