#!/usr/bin/env python3
"""Communication health scanner: bindings, spawn references, multi-agent routing.
Metadata for hover panel: channels active, channel list, tokens expiring, outbound policy.
"""
import json
import re
import os
from pathlib import Path
from utils import (
    get_openclaw_root, get_watchdog_config, auto_detect_agents,
    read_file_safe, WatchdogReport,
)


def scan_comm(config, report, root, agents):
    gateway_config = root / "config"

    if len(agents) <= 1:
        report.mark_not_applicable("单 agent 场景，通信路由检查不适用")
        report.set_metadata("channels_active", 0)
        report.set_metadata("channel_list", [])
        return

    channels_active = 0
    channel_list = []
    tokens_expiring = 0

    if gateway_config.exists():
        try:
            gw_data = json.loads(read_file_safe(gateway_config))

            # Detect active channels
            channels_cfg = gw_data.get("channels", {})
            for ch_name, ch_cfg in channels_cfg.items():
                if isinstance(ch_cfg, dict):
                    accounts = ch_cfg.get("accounts", {})
                    if accounts:
                        channels_active += 1
                        tools = ch_cfg.get("tools", {})
                        tool_names = [k for k, v in tools.items() if v] if tools else []
                        desc = f"{ch_name}"
                        if tool_names:
                            desc += f" ({', '.join(tool_names[:3])})"
                        channel_list.append(desc)

            # Check env var completeness for credential health
            env_keys_needed = set()
            for ch_name, ch_cfg in channels_cfg.items():
                if isinstance(ch_cfg, dict):
                    for acc_name, acc_cfg in ch_cfg.get("accounts", {}).items():
                        for key in ("appId", "appSecret"):
                            val = acc_cfg.get(key, "")
                            if isinstance(val, str) and val.startswith("$"):
                                env_keys_needed.add(val[1:])

            missing_env = [k for k in env_keys_needed if not os.environ.get(k)]
            if missing_env:
                tokens_expiring = len(missing_env)
                report.add_issue(
                    "comm_missing_env_keys", "HIGH",
                    f"通道凭证环境变量缺失：{', '.join(missing_env[:3])}{'...' if len(missing_env) > 3 else ''}",
                    "在 .env 或 plist EnvironmentVariables 中补齐",
                    [str(gateway_config)],
                    evidence=[f"缺失: {', '.join(missing_env)}"],
                    fix_action="在飞书群告知 techops 补齐环境变量"
                )

            # Check bindings
            bindings = gw_data.get("bindings", [])
            channel_binds = {}
            for b in bindings:
                if b.get("channel") == "feishu":
                    cid = b.get("channelId")
                    acc = b.get("accountId", "default")
                    if cid not in channel_binds:
                        channel_binds[cid] = set()
                    channel_binds[cid].add(acc)

            for cid, accs in channel_binds.items():
                if "default" not in accs or "main" not in accs:
                    report.add_issue(
                        f"feishu_binding_missing_{cid}", "HIGH",
                        f"飞书群 {cid[:12]}... 缺少 default 或 main 的绑定兜底",
                        "在 .openclaw/config 的 bindings 中补齐两个 accountId 的绑定",
                        [str(gateway_config)],
                        evidence=[f"当前绑定: {', '.join(accs)}，缺少 {'default' if 'default' not in accs else 'main'}"],
                        fix_action="在飞书群告知 techops 补齐 binding"
                    )

        except (json.JSONDecodeError, KeyError):
            pass

    # Check spawn targets
    spawn_pattern = re.compile(r'spawn\s+`?([a-zA-Z0-9_-]+)`?')
    for agent in agents:
        agent_dir = root / f"workspace-{agent}"
        for md_file in ["SOUL.md", "AGENTS.md", "HEARTBEAT.md"]:
            content = read_file_safe(agent_dir / md_file)
            if not content:
                continue
            matches = spawn_pattern.findall(content)
            for m in matches:
                if m not in agents and m != "main":
                    report.add_issue(
                        f"invalid_spawn_{agent}_{md_file}_{m}", "HIGH",
                        f"{agent}/{md_file} 试图 spawn 不存在的 agent: {m}",
                        f"修正 spawn 目标为已存在的 agent: {', '.join(agents)}",
                        [f"workspace-{agent}/{md_file}"],
                        evidence=[f"spawn {m} 不在已知 agent 列表中"],
                        fix_action="在飞书群告知负责人修正 spawn 目标"
                    )

    report.set_metadata("channels_active", channels_active)
    report.set_metadata("channel_list", channel_list)
    report.set_metadata("tokens_expiring_soon", tokens_expiring)
    report.set_metadata("outbound_policy", "Hongsong allowlist" if channels_active > 0 else "未配置")


def main():
    config = get_watchdog_config()
    report = WatchdogReport("comm")
    root = Path(get_openclaw_root())
    agents = auto_detect_agents(config)

    scan_comm(config, report, root, agents)
    report.save()


if __name__ == "__main__":
    main()
