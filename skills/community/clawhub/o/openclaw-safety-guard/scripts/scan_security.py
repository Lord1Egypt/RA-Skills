#!/usr/bin/env python3
"""Security scanner: plist, git, exec-approvals, API key leaks, script path guards, knowledge freshness, openclaw doctor.
Metadata for hover panel: exec approvals status, wildcard rules, high-priv keys, leaked patterns, risk summary.
"""
import os
import json
import subprocess
import datetime
import re
from pathlib import Path
from utils import get_openclaw_root, get_workspace_root, get_watchdog_config, WatchdogReport


def expand(p: str) -> Path:
    if p == ".":
        return Path(get_workspace_root())
    if p.startswith("./") or p.startswith(".openclaw/"):
        return Path(get_workspace_root()) / p
    return Path(os.path.expanduser(p))


def project_openclaw_env() -> dict:
    workspace_root = Path(get_workspace_root())
    env = dict(os.environ)
    env["OPENCLAW_CONFIG_PATH"] = str(workspace_root / ".openclaw" / "config")
    env["OPENCLAW_STATE_DIR"] = str(workspace_root / ".openclaw" / "state")
    env["NO_COLOR"] = "1"
    return env


def check_plist_permissions(cfg, report):
    target = expand(cfg.get("target", "~/Library/LaunchAgents/ai.openclaw.gateway.plist"))
    if not target.exists():
        return
    mode = oct(target.stat().st_mode)[-3:]
    if mode != "600":
        report.add_issue(
            "plist_permissions", "MEDIUM",
            f"plist文件权限不安全：当前 {mode}，建议 600",
            f"chmod 600 {target}",
            [str(target)],
            evidence=[f"当前权限: {mode}，安全要求: 600"],
            fix_action="在终端执行 chmod 600 命令"
        )


def check_git_commit_lag(cfg, report):
    target = expand(cfg.get("target", "."))
    threshold = cfg.get("threshold_days", 7)
    if not (target / ".git").exists():
        return
    try:
        log_result = subprocess.run(
            ["git", "log", "-1", "--format=%ct"],
            cwd=target, capture_output=True, text=True, timeout=10
        )
        last_commit_ts = log_result.stdout.strip()
        if last_commit_ts:
            last_commit = datetime.datetime.fromtimestamp(int(last_commit_ts))
            days_ago = (datetime.datetime.now() - last_commit).days
            if days_ago > threshold:
                report.add_issue(
                    "git_commit_lag", "MEDIUM",
                    f"工作区已经 {days_ago} 天未提交代码（超过阈值 {threshold} 天）",
                    f"cd {target} && git add -A && git commit -m '定期安全备份'",
                    [str(target)],
                    evidence=[f"最后提交: {last_commit.strftime('%Y-%m-%d')}, 距今 {days_ago} 天"],
                    fix_action="在终端执行 git commit"
                )
    except Exception:
        pass


def check_exec_approvals(cfg, report, meta):
    target = expand(cfg.get("target", "~/.openclaw/exec-approvals.json"))
    if not target.exists():
        meta["exec_approvals_enabled"] = False
        report.add_issue(
            "exec_approvals_missing", "HIGH",
            "exec-approvals.json 不存在，所有 agent 可执行任意高危命令",
            "创建 exec-approvals.json 并配置白名单",
            [str(target)],
            evidence=["文件不存在: " + str(target)],
            fix_action="使用 openclaw approvals set 创建白名单"
        )
        return

    meta["exec_approvals_enabled"] = True
    try:
        with open(target, encoding="utf-8") as f:
            data = json.load(f)
        agents = data.get("agents", {})

        full_agents = [k for k, v in agents.items() if v.get("security") == "full"]
        meta["high_privilege_keys"] = len(full_agents)

        has_wildcard = False
        auto_allow_count = 0
        for agent_id, agent_cfg in agents.items():
            allowlist = agent_cfg.get("allowlist", [])
            for rule in allowlist:
                if isinstance(rule, str) and "*" in rule:
                    has_wildcard = True
                if isinstance(rule, dict) and rule.get("auto_approve"):
                    auto_allow_count += 1

        meta["wildcard_rules"] = has_wildcard
        meta["auto_allow_skills"] = auto_allow_count

        if full_agents:
            report.add_issue(
                "exec_approvals_full", "MEDIUM",
                f"以下 agent 处于 security=full 高危状态：{', '.join(full_agents)}",
                "将高危 agent 改为 security=allowlist",
                [str(target)],
                evidence=[f"security=full agents: {', '.join(full_agents)}"],
                fix_action="在飞书群告知 techops 收紧 exec-approvals"
            )
    except Exception:
        pass


def check_api_key_in_git(cfg, report, meta):
    target = expand(cfg.get("target", "."))
    patterns = cfg.get("patterns", ["sk-", "Bearer "])
    if not (target / ".git").exists():
        return

    regex_rules = []
    if "sk-" in patterns:
        regex_rules.append(("sk-", re.compile(r"sk-[A-Za-z0-9]{20,}")))
    if "Bearer " in patterns:
        regex_rules.append(("Bearer ", re.compile(r"Bearer\s+[A-Za-z0-9._-]{20,}")))

    hits = []
    evidence = []
    for label, regex in regex_rules:
        try:
            res = subprocess.run(
                ["git", "log", "-p", "--all", "--pickaxe-regex", f"-G{regex.pattern}", "--oneline", "--diff-filter=A"],
                cwd=target, capture_output=True, text=True, timeout=30
            )
        except Exception:
            continue

        if not res.stdout.strip():
            continue

        added_lines = [
            line[1:].strip()
            for line in res.stdout.splitlines()
            if line.startswith("+") and not line.startswith("+++")
        ]
        matched_lines = [line for line in added_lines if regex.search(line)]
        if matched_lines:
            hits.append(label)
            evidence.append(f"{label} 命中示例: {matched_lines[0][:160]}")

    meta["leaked_patterns"] = len(hits)
    if hits:
        report.add_issue(
            "api_key_in_git", "HIGH",
            f"Git 历史记录中可能泄露了 API Key（命中关键词：{', '.join(hits)}）",
            "用 git-filter-repo 或 BFG Repo Cleaner 清理敏感数据",
            [str(target)],
            evidence=evidence or [f"命中关键词: {', '.join(hits)}"],
            fix_action="使用 BFG Repo Cleaner 清理 Git 历史"
        )


def check_skill_scripts_path(cfg, report):
    """Checks whether key scripts have path allowlist guards."""
    targets = cfg.get("targets", [])
    missing_protection = []
    for t in targets:
        p = expand(t)
        if not p.exists():
            continue
        content = p.read_text(encoding="utf-8", errors="ignore")
        if "assert_safe_path" not in content and "SAFE_DIRS" not in content:
            missing_protection.append(str(p))

    if missing_protection:
        report.add_issue(
            "skill_scripts_path", "MEDIUM",
            f"发现 {len(missing_protection)} 个关键脚本缺少路径白名单保护",
            "为关键脚本添加 assert_safe_path 或 SAFE_DIRS 校验",
            missing_protection[:10],
            evidence=[f"未检测到 assert_safe_path/SAFE_DIRS: {Path(p).name}" for p in missing_protection[:5]],
            fix_action="在飞书群告知 techops 给关键脚本补路径白名单"
        )


def check_knowledge_freshness(cfg, report):
    """Checks security knowledge base freshness (weekly update expected)."""
    threshold = cfg.get("threshold_days", 7)
    target = expand(cfg.get("target", ".openclaw/workspace-techops/skills/security-scanner/knowledge"))
    if not target.exists():
        report.add_issue(
            "knowledge_freshness_missing", "LOW",
            "安全知识库目录不存在，无法评估规则更新时效",
            "创建 knowledge 目录并执行一次知识更新",
            [str(target)],
            evidence=["目录不存在"],
            fix_action="在飞书群告知 techops 执行 security-scanner weekly knowledge"
        )
        return

    findings = sorted(target.glob("????-W??-findings.md"), reverse=True)
    if not findings:
        report.add_issue(
            "knowledge_freshness_empty", "LOW",
            "安全知识库还没有 weekly findings，规则可能长期未迭代",
            "执行 weekly knowledge 更新脚本并沉淀到 knowledge/",
            [str(target)],
            evidence=["未找到 YYYY-WW-findings.md 文件"],
            fix_action="在飞书群告知 techops 执行 weekly knowledge update"
        )
        return

    latest = findings[0]
    mtime = datetime.datetime.fromtimestamp(latest.stat().st_mtime)
    days_ago = (datetime.datetime.now() - mtime).days
    if days_ago > threshold:
        report.add_issue(
            "knowledge_freshness_stale", "LOW",
            f"安全知识库最后更新于 {days_ago} 天前（阈值 {threshold} 天）",
            "执行 weekly knowledge 更新，补充最新攻防实践",
            [str(latest)],
            evidence=[f"最后文件: {latest.name}, 最后更新时间: {mtime.strftime('%Y-%m-%d')}"],
            fix_action="在飞书群告知 techops 更新 security knowledge"
        )


def check_doctor_health(cfg, report):
    try:
        result = subprocess.run(
            ["openclaw", "doctor", "--non-interactive"],
            capture_output=True, text=True, timeout=30,
            env=project_openclaw_env()
        )
        output = (result.stdout + result.stderr).strip()
        actionable_markers = [
            "allowFrom: set to [\"*\"]",
            "permissions are too open",
            "group/world readable",
            "gateway.mode is unset",
            "Gateway auth is off or missing a token",
            "Session store dir missing",
        ]
        actionable_lines = [
            line.strip()
            for line in output.splitlines()
            if any(marker in line for marker in actionable_markers)
        ]
        if actionable_lines:
            report.add_issue(
                "doctor_health", "HIGH",
                f"openclaw doctor 发现 {len(actionable_lines)} 个系统健康警告",
                "运行 openclaw doctor --fix 尝试修复",
                [],
                evidence=actionable_lines[:5],
                fix_action="在终端执行 openclaw doctor --fix"
            )
    except Exception:
        pass


def main():
    config = get_watchdog_config()
    report = WatchdogReport("security")
    sec_cfg = config.get("security", {}).get("checks", [])

    if not sec_cfg:
        report.mark_not_applicable("config.json 中未配置 security.checks")
        report.save()
        return

    meta = {
        "exec_approvals_enabled": False,
        "wildcard_rules": False,
        "auto_allow_skills": 0,
        "high_privilege_keys": 0,
        "leaked_patterns": 0,
    }

    checkers = {
        "plist_permissions": lambda cfg, r: check_plist_permissions(cfg, r),
        "git_commit_lag": lambda cfg, r: check_git_commit_lag(cfg, r),
        "exec_approvals": lambda cfg, r: check_exec_approvals(cfg, r, meta),
        "api_key_in_git": lambda cfg, r: check_api_key_in_git(cfg, r, meta),
        "skill_scripts_path": lambda cfg, r: check_skill_scripts_path(cfg, r),
        "knowledge_freshness": lambda cfg, r: check_knowledge_freshness(cfg, r),
        "doctor_health": lambda cfg, r: check_doctor_health(cfg, r),
    }

    for chk in sec_cfg:
        if chk.get("enabled", True):
            fn = checkers.get(chk["id"])
            if fn:
                fn(chk, report)

    # Build risk summary from top issues
    risk_summary = [iss["title"] for iss in report.issues[:3]]

    report.set_metadata("exec_approvals_enabled", meta["exec_approvals_enabled"])
    report.set_metadata("wildcard_rules", meta["wildcard_rules"])
    report.set_metadata("auto_allow_skills", meta["auto_allow_skills"])
    report.set_metadata("high_privilege_keys", meta["high_privilege_keys"])
    report.set_metadata("leaked_patterns", meta["leaked_patterns"])
    report.set_metadata("risk_summary", risk_summary)

    report.save()


if __name__ == "__main__":
    main()
