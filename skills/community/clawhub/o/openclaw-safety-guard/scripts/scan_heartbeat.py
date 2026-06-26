#!/usr/bin/env python3
"""Heartbeat health scanner: checks HEARTBEAT.md files and heartbeat config.
Metadata for hover panel: active count, avg interval, daily calls, model, cost, lightContext, active hours.
"""
import json
import math
import re
from pathlib import Path
from utils import get_openclaw_root, get_watchdog_config, auto_detect_agents, read_file_safe, WatchdogReport

BOOTSTRAP_MAX_CHARS = 20000
TRUNCATION_WARN_CHARS = 16000
COST_WARN_TOKENS = 1000
LIGHT_CONTEXT_HINT_PATTERNS = [
    "读 `",
    "读取 `",
    "用 exec",
    "```bash",
    "python3 ",
    "sessions_spawn",
    "spawn ",
    "message 工具",
    "`message` 工具",
]
MESSAGE_HINT_PATTERNS = [
    "message 工具",
    "`message` 工具",
    "用 message",
]
READ_HINT_PATTERNS = [
    "读 `",
    "读取 `",
    "检查 `",
]
TIME_LOGIC_PATTERNS = [
    r"每周[一二三四五六日天].{0,8}第一次",
    r"每天.{0,8}前两次",
    r"每\s*\d+\s*天.{0,8}一次",
    r"超过\s*\d+\s*天.{0,12}(未发|未确认|未跟进|无进展)",
    r"距上次.{0,12}\d+\s*天",
]
UNAVAILABLE_RUNTIME_PATTERNS = [
    "CallMcpTool",
    "Cursor MCP",
    "user-xhs-mcp",
    "browser-use",
    "xhs_auth_status",
]

MODEL_COST_MAP = {
    "deepseek/deepseek-chat": "Low",
    "minimax/minimax-m2.5": "Low",
    "hongsong/minimax-m2.5": "Low",
    "hongsong/claude-sonnet-4-6": "High",
    "anthropic/claude-sonnet-4-6": "High",
    "openai/gpt-4o": "Medium",
    "openai/gpt-4o-mini": "Low",
    "qwen/qwen3.5-plus": "Low",
}

COST_HINTS = {
    "Low": "当前使用轻量模型，成本可控。",
    "Medium": "中等成本模型，建议评估是否可降级为 deepseek/minimax。",
    "High": "高成本模型（Claude/Opus 级别），强烈建议心跳改用轻量模型，仅在 Cron 任务中使用高端模型。",
}


def _is_claude_like_model(model: str) -> bool:
    normalized = (model or "").lower()
    return "claude" in normalized or normalized.startswith("anthropic/")


def _normalize_model(model: str) -> str:
    return (model or "").strip().lower()


def _is_intentional_skip(content: str) -> bool:
    normalized = (content or "").lower()
    intentional_phrases = ["skip heartbeat", "keep this file empty", "to skip heartbeat"]
    return any(p in normalized for p in intentional_phrases)


def _extract_external_refs(content: str) -> list[str]:
    refs = []
    for ref in re.findall(r"`([^`]+)`", content or ""):
        ref = ref.strip()
        if not ref or ref == "HEARTBEAT_OK":
            continue
        if (
            "/" in ref
            or ref.endswith((".md", ".json", ".csv", ".py"))
            or ref.startswith("memory/")
            or ref.startswith("skills/")
        ):
            refs.append(ref)
    return sorted(set(refs))


def _has_light_context_bootstrap(content: str) -> bool:
    return any(pattern in (content or "") for pattern in LIGHT_CONTEXT_HINT_PATTERNS)


def _contains_any(content: str, patterns: list[str]) -> bool:
    lowered = (content or "").lower()
    return any(pattern.lower() in lowered for pattern in patterns)


def _detect_time_logic(content: str) -> list[str]:
    hits = []
    for pattern in TIME_LOGIC_PATTERNS:
        match = re.search(pattern, content or "")
        if match:
            hits.append(match.group(0))
    return hits


def _detect_unavailable_runtime(content: str) -> list[str]:
    hits = []
    for pattern in UNAVAILABLE_RUNTIME_PATTERNS:
        if pattern.lower() in (content or "").lower():
            hits.append(pattern)
    return hits


def scan_heartbeat(config, report, root, agents):
    has_any_heartbeat = False
    active_count = 0
    intervals = []
    models_used = set()
    light_context_agents = []
    non_light_agents = []
    active_hours_info = {}
    hb_md_tokens_est = {}
    inactive_templates = []
    execution_audit = {}

    gw_config_path = root / "config"
    gw_agent_map = {}
    if gw_config_path.exists():
        try:
            gw_data = json.loads(read_file_safe(gw_config_path))
            for agent_cfg in gw_data.get("agents", {}).get("list", []):
                aid = agent_cfg.get("id", "")
                hb_cfg = agent_cfg.get("heartbeat", {})
                if hb_cfg:
                    gw_agent_map[aid] = hb_cfg
        except (json.JSONDecodeError, KeyError):
            pass

    for agent in agents:
        agent_dir = root / f"workspace-{agent}"
        if not agent_dir.exists():
            continue

        hb_md = agent_dir / "HEARTBEAT.md"
        hb_content = read_file_safe(hb_md)
        hb_cfg = gw_agent_map.get(agent, {})
        has_substantive_content = any(
            l.strip() and not l.strip().startswith("#")
            for l in (hb_content or "").splitlines()
        )
        intentional_skip = _is_intentional_skip(hb_content)

        if not hb_cfg:
            if hb_content and intentional_skip:
                inactive_templates.append(agent)
            continue

        has_any_heartbeat = True
        active_count += 1
        heartbeat_model = hb_cfg.get("model", "")
        external_refs = _extract_external_refs(hb_content)
        step_count = len(re.findall(r"^## Step\b", hb_content or "", flags=re.MULTILINE))
        clear_silence_rule = "HEARTBEAT_OK" in (hb_content or "") or "沉默条件" in (hb_content or "")
        light_context_enabled = bool(hb_cfg.get("lightContext"))
        message_explicit = _contains_any(hb_content, MESSAGE_HINT_PATTERNS)
        read_explicit = _contains_any(hb_content, READ_HINT_PATTERNS)
        exec_explicit = "```bash" in (hb_content or "") or "python3 " in (hb_content or "") or "用 exec" in (hb_content or "")
        spawn_explicit = "sessions_spawn" in (hb_content or "") or "spawn " in (hb_content or "")
        time_logic_hits = _detect_time_logic(hb_content)
        unavailable_runtime_hits = _detect_unavailable_runtime(hb_content)

        execution_audit[agent] = {
            "lightContext": light_context_enabled,
            "model": heartbeat_model or "未指定",
            "substantive": has_substantive_content,
            "step_count": step_count,
            "external_refs": external_refs,
            "clear_silence_rule": clear_silence_rule,
            "lightContext_bootstrap_explicit": _has_light_context_bootstrap(hb_content),
            "read_explicit": read_explicit,
            "exec_explicit": exec_explicit,
            "message_explicit": message_explicit,
            "spawn_explicit": spawn_explicit,
            "time_logic_detected": time_logic_hits,
            "unavailable_runtime_refs": unavailable_runtime_hits,
        }

        # First priority: execution completeness. Only flag when file is near the documented
        # bootstrap truncation ceiling, not merely because it is "long".
        if hb_content:
            char_len = len(hb_content)
            est_tokens = int(len(hb_content) * 0.7)
            hb_md_tokens_est[agent] = est_tokens
            if char_len >= TRUNCATION_WARN_CHARS:
                report.add_issue(
                    f"heartbeat_md_near_truncation_{agent}", "MEDIUM",
                    f"{agent}/HEARTBEAT.md 长度 {char_len} chars，接近注入截断上限 {BOOTSTRAP_MAX_CHARS}",
                    "优先精简 HEARTBEAT.md，确保心跳注入不被截断",
                    [str(hb_md)],
                    evidence=[
                        f"文件长度 {char_len} chars，预估 {est_tokens} tokens",
                        f"知识库记录的单文件自动注入上限为 {BOOTSTRAP_MAX_CHARS} chars",
                    ],
                    fix_action="在飞书群告知 techops 精简该 HEARTBEAT.md"
                )

            if _is_claude_like_model(heartbeat_model) and est_tokens > COST_WARN_TOKENS:
                report.add_issue(
                    f"heartbeat_md_large_claude_{agent}", "LOW",
                    f"{agent}/HEARTBEAT.md 预估 {est_tokens} tokens，Claude 类心跳成本偏高",
                    "保持执行逻辑不变，仅压缩文案冗余或改用轻量心跳模型",
                    [str(hb_md)],
                    evidence=[
                        f"文件长度 {char_len} chars，预估 {est_tokens} tokens",
                        f"heartbeat.model={heartbeat_model}",
                    ],
                    fix_action="在飞书群告知 techops 评估是否继续保留 Claude 类心跳"
                )

        lines = [l for l in (hb_content or "").splitlines() if l.strip()]
        if lines and all(l.strip().startswith("#") for l in lines[:3]):
            non_comment = [l for l in lines if not l.strip().startswith("#")]
            if not non_comment:
                if not intentional_skip:
                    report.add_issue(
                        f"heartbeat_only_comments_{agent}", "MEDIUM",
                        f"{agent}/HEARTBEAT.md 仅含注释，会被框架跳过（#7 易错点）",
                        "在最顶部加入非注释的实质说明",
                        [str(hb_md)],
                        evidence=["文件前 3 行全部以 # 开头，无实质内容"],
                        fix_action="在飞书群告知负责人修复"
                    )

        if has_substantive_content and step_count == 0 and not clear_silence_rule:
            report.add_issue(
                f"heartbeat_logic_unclear_{agent}", "LOW",
                f"{agent}/HEARTBEAT.md 缺少清晰的步骤或 HEARTBEAT_OK 沉默条件，执行边界不清晰",
                "补充 Step 结构或明确写出何时回复 HEARTBEAT_OK",
                [str(hb_md)],
                evidence=["未检测到 `## Step` 结构，且未检测到 `HEARTBEAT_OK` / `沉默条件`"],
                fix_action="在飞书群告知负责人补清心跳执行边界"
            )

        if light_context_enabled and external_refs and not _has_light_context_bootstrap(hb_content):
            report.add_issue(
                f"heartbeat_lightcontext_business_risk_{agent}", "MEDIUM",
                f"{agent} 启用 lightContext，但 HEARTBEAT.md 没明确写出补充读取/执行步骤，可能缺少业务上下文",
                "把必须读取的业务文件、exec 命令、消息动作直接写进 HEARTBEAT.md",
                [str(hb_md)],
                evidence=[
                    f"检测到外部依赖 {len(external_refs)} 个：{', '.join(external_refs[:6])}",
                    "lightContext=true 时只自动注入 HEARTBEAT.md",
                ],
                fix_action="在飞书群告知 techops 补齐 lightContext 自举步骤"
            )

        if time_logic_hits:
            report.add_issue(
                f"heartbeat_time_logic_mixed_{agent}", "MEDIUM",
                f"{agent}/HEARTBEAT.md 混入时间/频率判断，职责应交给 Cron 或外部状态",
                "把“每天前几次/每周一/每 3 天”之类逻辑迁出 HEARTBEAT.md",
                [str(hb_md)],
                evidence=[f"命中时间逻辑：{', '.join(time_logic_hits[:4])}"],
                fix_action="在飞书群告知负责人把时间调度从 heartbeat 中拆出"
            )

        if hb_cfg.get("target") == "none" and not message_explicit:
            report.add_issue(
                f"heartbeat_message_implicit_{agent}", "LOW",
                f"{agent} heartbeat target=\"none\"，但 HEARTBEAT.md 未显式说明使用 message 工具",
                "把发群动作明确写成 `message` 工具，避免模型只输出文本不发消息",
                [str(hb_md)],
                evidence=["target=none 时框架不会自动投递外部消息"],
                fix_action="在飞书群告知负责人补全 message 工具说明"
            )

        if light_context_enabled and not read_explicit:
            report.add_issue(
                f"heartbeat_lightcontext_read_implicit_{agent}", "LOW",
                f"{agent} 启用 lightContext，但 HEARTBEAT.md 没明确写出读取业务文件的动作",
                "显式写出要读哪些文件，而不是假设模型会自己知道",
                [str(hb_md)],
                evidence=["lightContext=true 时其他 bootstrap 文件不会自动注入"],
                fix_action="在飞书群告知负责人补全读取步骤"
            )

        if unavailable_runtime_hits:
            report.add_issue(
                f"heartbeat_runtime_tool_mismatch_{agent}", "MEDIUM",
                f"{agent}/HEARTBEAT.md 引用了 OpenClaw 运行时不可用的能力",
                "改成 OpenClaw 可调用的 read/exec/message/sessions_spawn 等能力",
                [str(hb_md)],
                evidence=[f"命中不可用引用：{', '.join(unavailable_runtime_hits)}"],
                fix_action="在飞书群告知负责人替换为运行时可用能力"
            )

        if hb_cfg:
            every_str = hb_cfg.get("every", "30m")
            try:
                minutes = int(every_str.replace("m", ""))
                intervals.append(minutes)
            except ValueError:
                pass

            model = hb_cfg.get("model", "")
            if model:
                models_used.add(model)

            if hb_cfg.get("lightContext"):
                light_context_agents.append(agent)
            else:
                non_light_agents.append(agent)

            ah = hb_cfg.get("activeHours", {})
            if ah:
                active_hours_info[agent] = f"{ah.get('start','?')}-{ah.get('end','?')}"
                if not all(ah.get(k) for k in ("start", "end", "timezone")):
                    report.add_issue(
                        f"heartbeat_activehours_incomplete_{agent}", "LOW",
                        f"{agent} heartbeat.activeHours 不完整，建议显式写全 start/end/timezone",
                        "补齐 activeHours.start、end、timezone",
                        [str(gw_config_path)],
                        evidence=[json.dumps(ah, ensure_ascii=False)],
                        fix_action="在飞书群告知 techops 补齐 activeHours"
                    )
                elif ah.get("start") == ah.get("end"):
                    report.add_issue(
                        f"heartbeat_activehours_zero_width_{agent}", "MEDIUM",
                        f"{agent} heartbeat.activeHours 的 start 与 end 相同，可能导致始终跳过",
                        "修改 activeHours，避免零宽时间窗",
                        [str(gw_config_path)],
                        evidence=[json.dumps(ah, ensure_ascii=False)],
                        fix_action="在飞书群告知 techops 修复 activeHours"
                    )
            else:
                report.add_issue(
                    f"heartbeat_activehours_missing_{agent}", "LOW",
                    f"{agent} heartbeat 未显式配置 activeHours，建议写出业务时段",
                    "根据业务补充 activeHours，避免 24x7 心跳噪音",
                    [str(gw_config_path)],
                    evidence=["官方允许省略，但本项目建议显式声明业务时段"],
                    fix_action="在飞书群告知 techops 评估 activeHours"
                )

            if "directPolicy" not in hb_cfg:
                report.add_issue(
                    f"heartbeat_directpolicy_implicit_{agent}", "LOW",
                    f"{agent} heartbeat 未显式声明 directPolicy，存在默认值漂移风险",
                    "显式写出 directPolicy: \"allow\" 或 \"block\"",
                    [str(gw_config_path)],
                    evidence=["v2026.2.25+ 已用 directPolicy 替代 allowDirect"],
                    fix_action="在飞书群告知 techops 补齐 directPolicy"
                )

            if "allowDirect" in hb_cfg:
                report.add_issue(
                    f"heartbeat_deprecated_allowDirect_{agent}", "MEDIUM",
                    f"{agent} heartbeat 使用已废弃的 allowDirect，应改为 directPolicy",
                    "将 allowDirect 替换为 directPolicy: \"allow\" 或 \"block\"",
                    [str(gw_config_path)],
                    evidence=["v2026.2.25 Breaking Change: allowDirect 已废弃"],
                    fix_action="在飞书群告知 techops 修改 config"
                )

            if hb_cfg.get("target") == "feishu":
                report.add_issue(
                    f"heartbeat_target_feishu_{agent}", "MEDIUM",
                    f"{agent} heartbeat target=\"feishu\" 会导致整段回复进群（#6 易错点）",
                    "改为 target: \"none\" + 用 message 工具发群",
                    [str(gw_config_path)],
                    evidence=["target=feishu 时 Gateway 投递整段助手回复"],
                    fix_action="在飞书群告知 techops 修改 config"
                )

    if not has_any_heartbeat:
        report.mark_not_applicable("没有任何 workspace 配置了 HEARTBEAT.md 或 heartbeat")
        return

    # Build metadata
    avg_interval = int(sum(intervals) / len(intervals)) if intervals else 0
    if avg_interval > 0:
        active_minutes_per_day = 16 * 60  # assume 16h active
        daily_calls = int(active_minutes_per_day / avg_interval) * active_count
    else:
        daily_calls = 0

    default_model = list(models_used)[0] if len(models_used) == 1 else (", ".join(models_used) if models_used else "未指定")
    cost_level = "Low"
    for m in models_used:
        cl = MODEL_COST_MAP.get(_normalize_model(m), "Medium")
        if cl == "High":
            cost_level = "High"
            break
        if cl == "Medium":
            cost_level = "Medium"

    report.set_metadata("active_heartbeats", active_count)
    report.set_metadata("avg_interval_min", avg_interval)
    report.set_metadata("daily_calls_est", daily_calls)
    report.set_metadata("default_model", default_model)
    report.set_metadata("model_cost_level", cost_level)
    report.set_metadata("cost_hint", COST_HINTS.get(cost_level, ""))
    report.set_metadata("light_context", {
        "on": light_context_agents,
        "off": non_light_agents,
    })
    report.set_metadata("inactive_templates", inactive_templates)
    report.set_metadata("execution_audit", execution_audit)
    report.set_metadata("heartbeat_md_tokens", hb_md_tokens_est)
    report.set_metadata("active_hours", active_hours_info if active_hours_info else "未配置（24x7）")
    report.set_metadata("quiet_hours", "None")


def main():
    config = get_watchdog_config()
    report = WatchdogReport("heartbeat")
    root = Path(get_openclaw_root())
    agents = auto_detect_agents(config)

    scan_heartbeat(config, report, root, agents)
    report.save()


if __name__ == "__main__":
    main()
