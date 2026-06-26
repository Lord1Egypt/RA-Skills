#!/usr/bin/env python3
"""
lark-multi-agent-factory: 针对 @larksuite/openclaw-lark 插件的多 agent 批量配置工具
用法:
  python3 setup_agents.py --config '<JSON 字符串>'
  python3 setup_agents.py --config-file agents.json
  python3 setup_agents.py --list         # 查看已有 agents
  python3 setup_agents.py --remove <id>  # 删除 agent
  python3 setup_agents.py --set-channel  # 配置 channel 级别参数（threadSession / replyMode）

与 feishu-multi-agent-factory 的区别：
  - 专为 @larksuite/openclaw-lark (≥ 2026.4.0) 设计
  - 支持 threadSession、replyMode、blockStreaming 等官方插件专属字段
  - 创建前自动检查插件是否已安装并启用

输入 JSON 格式:
{
  "channel": {                          (可选) 覆盖 channel 级别配置
    "threadSession": true,
    "replyMode": "auto",
    "blockStreaming": false
  },
  "agents": [
    {
      "id": "coder",
      "name": "代码专家",
      "emoji": "💻",
      "description": "负责写代码",       (可选)
      "feishu_app_id": "cli_xxx",
      "feishu_app_secret": "xxxxxx",
      "feishu_domain": "feishu",         (可选, 默认 feishu)
      "reply_mode": "streaming"          (可选, 覆盖 channel 级别 replyMode)
    }
  ]
}
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

OPENCLAW_DIR = Path.home() / ".openclaw"
CONFIG_PATH  = OPENCLAW_DIR / "openclaw.json"

PLUGIN_NAME  = "@larksuite/openclaw-lark"
REPLY_MODES  = {"auto", "static", "streaming"}

# agent id 白名单：小写字母、数字、连字符，首字符必须为字母或数字，最长 32
_ID_PATTERN = re.compile(r'^[a-z0-9][a-z0-9\-]{0,31}$')


# ─── 校验 ─────────────────────────────────────────────────────────────────────

def validate_agent_id(agent_id: str) -> str:
    aid = agent_id.strip().lower()
    if not _ID_PATTERN.match(aid):
        raise ValueError(
            f"非法 agent id '{agent_id}'：只允许小写字母、数字、连字符，"
            f"首字符须为字母或数字，最长 32 位"
        )
    if ".." in aid or "/" in aid or "\\" in aid:
        raise ValueError(f"非法 agent id '{agent_id}'：包含路径穿越字符")
    return aid


def validate_reply_mode(mode: str) -> str:
    if mode not in REPLY_MODES:
        raise ValueError(f"reply_mode 必须是 {REPLY_MODES} 之一，收到: '{mode}'")
    return mode


def mask_secret(secret: str) -> str:
    if not secret:
        return "(未提供)"
    return secret[:4] + "****"


# ─── 插件检查 ─────────────────────────────────────────────────────────────────

def check_plugin_installed() -> bool:
    """检查 @larksuite/openclaw-lark 是否已安装"""
    try:
        result = subprocess.run(
            ["openclaw", "plugins", "list", "--json"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            plugins = json.loads(result.stdout)
            for p in (plugins if isinstance(plugins, list) else plugins.get("plugins", [])):
                name = p.get("name", "") if isinstance(p, dict) else str(p)
                if PLUGIN_NAME in name:
                    return True
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        pass

    # 备用：检查 node_modules
    node_paths = [
        Path("/opt/homebrew/lib/node_modules"),
        Path.home() / ".local/lib/node_modules",
        Path("/usr/local/lib/node_modules"),
    ]
    for base in node_paths:
        pkg = base / PLUGIN_NAME.lstrip("@").replace("/", "/")
        # @larksuite/openclaw-lark → larksuite/openclaw-lark
        pkg2 = base / "openclaw-lark"
        scope_pkg = base / "@larksuite" / "openclaw-lark"
        if scope_pkg.exists() or pkg.exists() or pkg2.exists():
            return True

    return False


# ─── 工具函数 ─────────────────────────────────────────────────────────────────

def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(cfg: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    print(f"  ✅ 配置已写入 {CONFIG_PATH}")


# ─── 列出现有 agents ──────────────────────────────────────────────────────────

def cmd_list():
    cfg = load_config()
    agents        = cfg.get("agents", {}).get("list", [])
    feishu_ch     = cfg.get("channels", {}).get("feishu", {})
    feishu_accts  = feishu_ch.get("accounts", {})
    thread_sess   = feishu_ch.get("threadSession", "—")
    reply_mode    = feishu_ch.get("replyMode", "—")

    print(f"\n  插件: {PLUGIN_NAME}")
    print(f"  channel.threadSession = {thread_sess}   replyMode = {reply_mode}")
    print(f"\n{'ID':<20} {'名称':<18} {'飞书 AppId':<30} {'replyMode':<12} {'状态'}")
    print("─" * 90)
    for a in agents:
        aid  = a["id"]
        name = a.get("name", "")
        emoji = a.get("identity", {}).get("emoji", "")
        feishu = feishu_accts.get(aid, {})
        app_id  = feishu.get("appId", "—")
        enabled = "✅" if feishu.get("enabled") else ("—" if not feishu else "❌")
        acct_rm = feishu.get("replyMode", "")
        rm_disp = acct_rm if acct_rm else "(继承)"
        print(f"{aid:<20} {emoji+' '+name:<18} {app_id:<30} {rm_disp:<12} {enabled}")
    print(f"\n共 {len(agents)} 个 agents")


# ─── 配置 channel 级别参数 ────────────────────────────────────────────────────

def cmd_set_channel(thread_session=None, reply_mode=None, block_streaming=None,
                    dry_run=False):
    cfg = load_config()
    feishu_cfg = cfg.setdefault("channels", {}).setdefault("feishu", {})
    changes = []

    if thread_session is not None:
        feishu_cfg["threadSession"] = thread_session
        changes.append(f"threadSession = {thread_session}")

    if reply_mode is not None:
        validate_reply_mode(reply_mode)
        feishu_cfg["replyMode"] = reply_mode
        changes.append(f"replyMode = '{reply_mode}'")

    if block_streaming is not None:
        feishu_cfg["blockStreaming"] = block_streaming
        changes.append(f"blockStreaming = {block_streaming}")

    if not changes:
        print("未指定任何参数，无更改。")
        print("可用参数: --thread-session, --reply-mode, --block-streaming")
        return

    if dry_run:
        print(f"[dry-run] 将设置: {', '.join(changes)}")
        return

    save_config(cfg)
    print(f"  channel 配置已更新: {', '.join(changes)}")


# ─── 删除 agent ───────────────────────────────────────────────────────────────

def cmd_remove(agent_id: str, dry_run: bool = False):
    if agent_id == "main":
        print("❌ 不允许删除 main agent")
        sys.exit(1)

    cfg = load_config()
    agent_list = cfg.get("agents", {}).get("list", [])
    existing = next((a for a in agent_list if a["id"] == agent_id), None)
    if not existing:
        print(f"❌ agent '{agent_id}' 不存在")
        sys.exit(1)

    if dry_run:
        print(f"[dry-run] 将删除 agent: {agent_id}")
        return

    cfg["agents"]["list"] = [a for a in agent_list if a["id"] != agent_id]

    feishu = cfg.get("channels", {}).get("feishu", {}).get("accounts", {})
    feishu.pop(agent_id, None)

    cfg["bindings"] = [b for b in cfg.get("bindings", [])
                       if b.get("agentId") != agent_id]

    allow = cfg.get("tools", {}).get("agentToAgent", {}).get("allow", [])
    if agent_id in allow:
        allow.remove(agent_id)

    save_config(cfg)
    print(f"✅ agent '{agent_id}' 已从配置中移除")
    print(f"   ⚠️  工作区目录未删除，请手动确认是否清除:")
    print(f"   rm -rf {OPENCLAW_DIR}/workspace-{agent_id}")
    print(f"   rm -rf {OPENCLAW_DIR}/agents/{agent_id}")


# ─── 创建单个 agent ───────────────────────────────────────────────────────────

def create_agent(cfg: dict, agent_cfg: dict,
                 channel_overrides: dict,
                 dry_run: bool = False) -> dict:
    """
    返回 {'status': 'created'|'skipped', 'id': ..., 'notes': [...]}
    """
    try:
        aid = validate_agent_id(agent_cfg["id"])
    except ValueError as e:
        return {"id": agent_cfg["id"], "status": "skipped", "notes": [str(e)]}

    name       = agent_cfg["name"]
    emoji      = agent_cfg.get("emoji", "🤖")
    desc       = agent_cfg.get("description", "")
    app_id     = agent_cfg.get("feishu_app_id", "")
    app_secret = agent_cfg.get("feishu_app_secret", "")
    domain     = agent_cfg.get("feishu_domain", "feishu")

    # Per-agent reply_mode override
    acct_reply_mode = agent_cfg.get("reply_mode", "")
    if acct_reply_mode:
        try:
            validate_reply_mode(acct_reply_mode)
        except ValueError as e:
            return {"id": aid, "status": "skipped", "notes": [str(e)]}

    result = {"id": aid, "status": "created", "notes": []}

    # ── 检查重复 ───────────────────────────────────────────────────────────────
    agent_list = cfg.get("agents", {}).get("list", [])
    if any(a["id"] == aid for a in agent_list):
        result["status"] = "skipped"
        result["notes"].append(f"agent id '{aid}' 已存在，跳过")
        return result

    workspace_path = OPENCLAW_DIR / f"workspace-{aid}"
    agent_dir      = OPENCLAW_DIR / "agents" / aid / "agent"

    if dry_run:
        result["notes"].append(f"[dry-run] 将创建 workspace: {workspace_path}")
        result["notes"].append(f"[dry-run] 将创建 agentDir:  {agent_dir}")
        if app_id:
            result["notes"].append(f"[dry-run] 飞书 account '{aid}' (AppId: {app_id})")
        if acct_reply_mode:
            result["notes"].append(f"[dry-run] per-agent replyMode: {acct_reply_mode}")
        return result

    # ── 1. 创建 workspace 目录 ─────────────────────────────────────────────────
    workspace_path.mkdir(parents=True, exist_ok=True)
    identity_md = workspace_path / "IDENTITY.md"
    if not identity_md.exists():
        identity_md.write_text(
            f"# IDENTITY.md\n\n"
            f"- **Name:** {name}\n"
            f"- **Emoji:** {emoji}\n"
            f"- **Description:** {desc or name}\n"
            f"- **Created:** {datetime.now().strftime('%Y-%m-%d')}\n",
            encoding="utf-8"
        )
        result["notes"].append(f"创建 IDENTITY.md → {identity_md}")

    for fname, content in [
        ("AGENTS.md",    "# AGENTS.md\n\n多 agent 协作说明。\n"),
        ("SOUL.md",      f"# SOUL.md\n\n{name} 的行为准则与人格设定。\n"),
        ("TOOLS.md",     "# TOOLS.md\n\n工具说明与注意事项。\n"),
        ("HEARTBEAT.md", "# HEARTBEAT.md\n\n"),
    ]:
        fp = workspace_path / fname
        if not fp.exists():
            fp.write_text(content, encoding="utf-8")

    # ── 2. 创建 agentDir ──────────────────────────────────────────────────────
    agent_dir.mkdir(parents=True, exist_ok=True)

    defaults_file = agent_dir / "defaults.json"
    if not defaults_file.exists():
        global_defaults = cfg.get("agents", {}).get("defaults", {})
        mini_defaults = {}
        if "model" in global_defaults:
            mini_defaults["model"] = global_defaults["model"]
        defaults_file.write_text(
            json.dumps(mini_defaults, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    result["notes"].append(f"请运行 `openclaw configure` 为 '{aid}' 配置 API key")

    # ── 3. 更新 agents.list ───────────────────────────────────────────────────
    new_agent_entry = {
        "id":        aid,
        "name":      name,
        "workspace": str(workspace_path),
        "agentDir":  str(agent_dir),
        "identity": {
            "name":  name,
            "emoji": emoji
        }
    }
    cfg.setdefault("agents", {}).setdefault("list", []).append(new_agent_entry)

    # ── 4. 添加飞书 account ───────────────────────────────────────────────────
    if app_id and app_secret:
        feishu_cfg = cfg.setdefault("channels", {}).setdefault("feishu", {})

        # 检查顶层默认机器人凭据
        if not feishu_cfg.get("appId") or not feishu_cfg.get("appSecret"):
            result["notes"].append(
                "⚠️  警告: channels.feishu 缺少顶层 appId/appSecret"
                "，请先通过 `openclaw channels add` 配置主账号"
            )

        # 应用 channel 级别的 @larksuite 专属字段
        if channel_overrides:
            if "threadSession" in channel_overrides:
                feishu_cfg.setdefault("threadSession", channel_overrides["threadSession"])
            if "replyMode" in channel_overrides:
                feishu_cfg.setdefault("replyMode", channel_overrides["replyMode"])
            if "blockStreaming" in channel_overrides:
                feishu_cfg.setdefault("blockStreaming", channel_overrides["blockStreaming"])
            if "blockStreamingCoalesce" in channel_overrides:
                feishu_cfg.setdefault("blockStreamingCoalesce",
                                      channel_overrides["blockStreamingCoalesce"])

        accounts = feishu_cfg.setdefault("accounts", {})
        if aid not in accounts:
            acct = {
                "appId":     app_id,
                "appSecret": app_secret,
                "name":      name,
                "domain":    domain,
                "enabled":   True
            }
            # 仅当 per-agent replyMode 与 channel 级别不同时才写入账号级别
            if acct_reply_mode:
                channel_rm = channel_overrides.get("replyMode", feishu_cfg.get("replyMode", ""))
                if acct_reply_mode != channel_rm:
                    acct["replyMode"] = acct_reply_mode
                    result["notes"].append(
                        f"per-agent replyMode = '{acct_reply_mode}' (覆盖 channel 级别)"
                    )
            accounts[aid] = acct
            result["notes"].append(
                f"飞书 account '{aid}' 已添加 (AppId: {app_id}, Secret: {mask_secret(app_secret)})"
            )
        else:
            result["notes"].append(f"飞书 account '{aid}' 已存在，跳过")
    else:
        result["notes"].append("未提供飞书凭据，跳过飞书 channel 配置")

    # ── 5. 添加 binding ───────────────────────────────────────────────────────
    if app_id and app_secret:
        bindings = cfg.setdefault("bindings", [])
        already_bound = any(
            b.get("agentId") == aid and
            b.get("match", {}).get("channel") == "feishu" and
            b.get("match", {}).get("accountId") == aid
            for b in bindings
        )
        if not already_bound:
            bindings.append({
                "agentId": aid,
                "match": {
                    "channel":   "feishu",
                    "accountId": aid
                }
            })

    # ── 6. 加入 agentToAgent.allow ────────────────────────────────────────────
    allow = (cfg.setdefault("tools", {})
                .setdefault("agentToAgent", {})
                .setdefault("allow", []))
    if aid not in allow:
        allow.append(aid)

    # ── 7. session.dmScope（多 agent 必须）───────────────────────────────────
    session = cfg.setdefault("session", {})
    if "dmScope" not in session:
        session["dmScope"] = "per-account-channel-peer"
        result["notes"].append("session.dmScope 已设置为 per-account-channel-peer")

    return result


# ─── 主入口 ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=f"OpenClaw 多 agent 批量配置工具（{PLUGIN_NAME}）"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--config",      help="内联 JSON 字符串")
    group.add_argument("--config-file", help="JSON 配置文件路径")
    group.add_argument("--list",        action="store_true", help="列出现有 agents")
    group.add_argument("--remove",      metavar="ID",   help="删除指定 agent")
    group.add_argument("--set-channel", action="store_true",
                       help="仅更新 channel 级别参数（无需 agents 列表）")

    parser.add_argument("--dry-run",    action="store_true", help="仅预览，不写入")
    parser.add_argument("--restart",    action="store_true", help="完成后重启 gateway")
    parser.add_argument("--skip-plugin-check", action="store_true",
                       help="跳过插件安装检查（调试用）")

    # --set-channel 专用参数
    parser.add_argument("--thread-session", type=lambda x: x.lower() == "true",
                        metavar="true|false", help="设置 threadSession")
    parser.add_argument("--reply-mode",  choices=list(REPLY_MODES),
                        help="设置 replyMode")
    parser.add_argument("--block-streaming", type=lambda x: x.lower() == "true",
                        metavar="true|false", help="设置 blockStreaming")

    args = parser.parse_args()

    # ── 插件检查 ──────────────────────────────────────────────────────────────
    if not args.skip_plugin_check:
        if not check_plugin_installed():
            print(f"❌ 未检测到 {PLUGIN_NAME} 插件")
            print(f"   请先安装: openclaw plugins install {PLUGIN_NAME}")
            print(f"   然后禁用内置插件（若已安装）: openclaw plugins disable feishu")
            print(f"   如需跳过此检查: --skip-plugin-check")
            sys.exit(1)

    if args.list:
        cmd_list()
        return

    if args.remove:
        cmd_remove(args.remove, dry_run=args.dry_run)
        if args.restart and not args.dry_run:
            print("\n🔄 重启 gateway...")
            subprocess.run(["openclaw", "gateway", "restart"], check=False)
        return

    if args.set_channel:
        cmd_set_channel(
            thread_session=args.thread_session,
            reply_mode=args.reply_mode,
            block_streaming=args.block_streaming,
            dry_run=args.dry_run,
        )
        if args.restart and not args.dry_run:
            print("\n🔄 重启 gateway...")
            subprocess.run(["openclaw", "gateway", "restart"], check=False)
        return

    # ── 解析 JSON 输入 ────────────────────────────────────────────────────────
    if args.config:
        try:
            payload = json.loads(args.config)
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析失败: {e}")
            sys.exit(1)
    else:
        with open(args.config_file, "r", encoding="utf-8") as f:
            payload = json.load(f)

    agents_to_create = payload.get("agents", [])
    if not agents_to_create:
        print("❌ 未找到 agents 列表")
        sys.exit(1)

    # channel 级别覆盖（来自 JSON 顶层 "channel" 字段）
    channel_overrides = payload.get("channel", {})

    # 校验 channel.replyMode
    if "replyMode" in channel_overrides:
        try:
            validate_reply_mode(channel_overrides["replyMode"])
        except ValueError as e:
            print(f"❌ channel.{e}")
            sys.exit(1)

    cfg = load_config()
    results = []

    print(f"\n{'─'*55}")
    print(f"  🏭 lark-agent-factory — 批量创建 {len(agents_to_create)} 个 agent")
    print(f"  插件: {PLUGIN_NAME}")
    if channel_overrides:
        overrides_display = {k: v for k, v in channel_overrides.items()}
        print(f"  channel 配置: {json.dumps(overrides_display, ensure_ascii=False)}")
    print(f"{'─'*55}")

    for a in agents_to_create:
        print(f"\n  ▶ {a.get('emoji','🤖')} {a['name']} (id: {a['id']})")
        r = create_agent(cfg, a, channel_overrides=channel_overrides, dry_run=args.dry_run)
        results.append(r)
        if r["status"] == "skipped":
            print(f"    ⚠️  跳过: {'; '.join(r['notes'])}")
        else:
            for note in r["notes"]:
                print(f"    • {note}")

    if not args.dry_run:
        save_config(cfg)

    created = [r for r in results if r["status"] == "created"]
    skipped = [r for r in results if r["status"] == "skipped"]
    print(f"\n{'─'*55}")
    print(f"  ✅ 创建: {len(created)} 个   ⚠️  跳过: {len(skipped)} 个")
    if created:
        print(f"  新 agents: {', '.join(r['id'] for r in created)}")

    if args.restart and created and not args.dry_run:
        print("\n🔄 重启 gateway...")
        subprocess.run(["openclaw", "gateway", "restart"], check=False)
    elif created and not args.dry_run:
        print("\n  ⚡ 请手动重启 gateway 使配置生效:")
        print("     openclaw gateway restart")

    print()


if __name__ == "__main__":
    main()
