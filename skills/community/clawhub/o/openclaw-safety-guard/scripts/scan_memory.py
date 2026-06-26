#!/usr/bin/env python3
"""Memory health scanner: staleness, bloat, orphan references, sensitive info scan,
cross-workspace conflict detection, shared decision sync drift and decision propagation checks.
Metadata for hover panel: session counts, stale ratio, sensitive hits, retention policy.
"""
import re
from datetime import datetime, timedelta
from pathlib import Path
from utils import (
    get_openclaw_root, get_watchdog_config, auto_detect_agents,
    read_file_safe, WatchdogReport,
)

SENSITIVE_PATTERNS = [
    (re.compile(r'sk-[a-zA-Z0-9]{20,}'), "API Key (sk-...)"),
    (re.compile(r'Bearer\s+[a-zA-Z0-9._\-]{20,}'), "Bearer Token"),
    (re.compile(r'\bpassword\b\s*[=:]\s*\S{6,}', re.IGNORECASE), "Password assignment"),
    (re.compile(r'\bsecret\b\s*[=:]\s*\S{6,}', re.IGNORECASE), "Secret assignment"),
    (re.compile(r'[a-zA-Z0-9+/]{40,}={0,2}'), "Possible base64 secret (40+ chars)"),
]


def count_lines(text: str) -> int:
    return len(text.strip().splitlines()) if text.strip() else 0


def _looks_like_base64_secret(candidate: str) -> bool:
    if len(candidate) < 40:
        return False
    has_lower = any(ch.islower() for ch in candidate)
    has_upper = any(ch.isupper() for ch in candidate)
    has_digit = any(ch.isdigit() for ch in candidate)
    has_padding_or_symbol = any(ch in candidate for ch in ("=", "+"))

    # Reject slash-joined word lists such as SOUL/IDENTITY/... which are not secrets.
    if "/" in candidate:
        parts = [part for part in candidate.split("/") if part]
        if parts and all(part.replace("-", "").isalpha() for part in parts):
            return False

    # The fallback base64 rule should stay conservative; structured secrets usually
    # have mixed case and either digits or padding/symbol chars.
    return has_lower and has_upper and (has_digit or has_padding_or_symbol)


def _count_sensitive_matches(text: str) -> int:
    total_hits = 0
    for pattern, label in SENSITIVE_PATTERNS:
        if label == "Possible base64 secret (40+ chars)":
            for line in text.splitlines():
                stripped = line.strip()
                if not stripped:
                    continue
                # Skip obvious file paths / URLs that can accidentally look like base64 blobs.
                lowered = stripped.lower()
                if any(marker in stripped for marker in ("/Users/", "http://", "https://")):
                    continue
                if any(marker in lowered for marker in (".md", ".json", ".py", ".sh", "workspace-", "skills/")):
                    continue
                total_hits += sum(
                    1 for match in pattern.findall(stripped)
                    if _looks_like_base64_secret(match)
                )
            continue
        total_hits += len(pattern.findall(text))
    return total_hits


def check_memory_staleness(cfg, report, agents, root, stats):
    threshold = cfg.get("threshold_days", 14)
    cutoff = datetime.now() - timedelta(days=threshold)
    stale_files = []
    total_dated = 0

    for agent in agents:
        mem_dir = root / f"workspace-{agent}" / "memory"
        if not mem_dir.is_dir():
            continue
        for f in sorted(mem_dir.glob("202?-??-??.md")):
            total_dated += 1
            m = re.match(r"(\d{4}-\d{2}-\d{2})", f.name)
            if m:
                try:
                    fdate = datetime.strptime(m.group(1), "%Y-%m-%d")
                    if fdate < cutoff:
                        stale_files.append(str(f.relative_to(root)))
                except ValueError:
                    pass

    stats["total_dated_files"] = total_dated
    stats["stale_files"] = len(stale_files)
    stats["stale_ratio"] = f"{int(len(stale_files)/total_dated*100)}%" if total_dated > 0 else "0%"

    if stale_files:
        report.add_issue(
            "memory_staleness", "MEDIUM",
            f"存在 {len(stale_files)} 个超过 {threshold} 天未归档的 dated memory 文件",
            "运行 archive.py 清理或归档旧记忆",
            stale_files[:10],
            evidence=[f"共 {total_dated} 个 dated 文件，{len(stale_files)} 个超过 {threshold} 天"],
            fix_action="在飞书群告知 techops 执行 memory 归档"
        )


def check_memory_bloat(cfg, report, agents, root, stats):
    max_memory_lines = cfg.get("memory_md_max_lines", 120)
    max_dated_lines = cfg.get("dated_total_max_lines", 600)

    for agent in agents:
        ws_path = root / f"workspace-{agent}"
        memory_md = ws_path / "MEMORY.md"
        content = read_file_safe(memory_md)
        lines = count_lines(content)
        if lines > max_memory_lines:
            report.add_issue(
                f"memory_bloat_{agent}", "MEDIUM",
                f"{agent}/MEMORY.md 膨胀，达 {lines} 行（上限 {max_memory_lines}）",
                "将带日期的动态事件迁移到 dated memory，MEMORY.md 只留静态事实",
                [str(memory_md.relative_to(root))],
                evidence=[f"当前 {lines} 行，上限 {max_memory_lines} 行"],
                fix_action="在飞书群告知负责人精简 MEMORY.md"
            )

        mem_dir = ws_path / "memory"
        if mem_dir.is_dir():
            total = 0
            for f in mem_dir.glob("202?-??-??.md"):
                total += count_lines(read_file_safe(f))
            if total > max_dated_lines:
                report.add_issue(
                    f"dated_bloat_{agent}", "MEDIUM",
                    f"{agent}/memory/ 目录记忆严重堆积，共 {total} 行（上限 {max_dated_lines}）",
                    "归档并删除较老的 dated memory",
                    [f"workspace-{agent}/memory"],
                    evidence=[f"dated memory 总计 {total} 行，上限 {max_dated_lines}"],
                    fix_action="在飞书群告知 techops 执行 memory 归档"
                )


def check_orphan_memory(cfg, report, agents, root):
    path_pattern = re.compile(r'skills/[\w-]+/[\w./-]+|memory/[\w./-]+')
    for agent in agents:
        ws_path = root / f"workspace-{agent}"
        memory_md = ws_path / "MEMORY.md"
        content = read_file_safe(memory_md)
        if not content:
            continue
        refs = path_pattern.findall(content)
        orphans = []
        for ref in refs:
            # Ignore template placeholders shown as usage examples.
            if "YYYY" in ref or "MM" in ref or "DD" in ref:
                continue
            full = ws_path / ref
            if not full.exists():
                orphans.append(ref)
        if orphans:
            report.add_issue(
                f"orphan_memory_{agent}", "LOW",
                f"{agent}/MEMORY.md 引用了 {len(orphans)} 个不存在的文件或目录",
                "清理 MEMORY.md 中的死链接",
                [f"workspace-{agent}/MEMORY.md"],
                evidence=[f"死链接: {', '.join(orphans[:5])}"],
                fix_action="在飞书群告知负责人清理 MEMORY.md 死链接"
            )


def check_sensitive_info(report, agents, root, stats):
    total_hits = 0
    for agent in agents:
        ws_path = root / f"workspace-{agent}"
        for md_file in ["MEMORY.md"]:
            content = read_file_safe(ws_path / md_file)
            if not content:
                continue
            total_hits += _count_sensitive_matches(content)

        mem_dir = ws_path / "memory"
        if mem_dir.is_dir():
            for f in mem_dir.glob("*.md"):
                content = read_file_safe(f)
                total_hits += _count_sensitive_matches(content)

    stats["sensitive_hits"] = total_hits
    if total_hits > 0:
        report.add_issue(
            "memory_sensitive_info", "HIGH",
            f"记忆文件中检测到 {total_hits} 处疑似敏感信息（API Key / Token / Password）",
            "检查并清理记忆文件中的敏感信息",
            [],
            evidence=[f"共 {total_hits} 处匹配（仅计数，不展示内容）"],
            fix_action="在飞书群告知 techops 排查并清理敏感信息"
        )


def _has_genuine_value_conflict(matches: dict, authority: str, root: "Path") -> bool:
    """
    Returns True only if there is clear evidence of a numeric value conflict:
    a non-authority file defines values (e.g. age ranges 35-55, percentages 5%)
    that DIFFER from the authority's canonical values.

    Returns False when:
    - All files reference the same canonical values (consistent)
    - No numeric values appear in any of the matched lines (pure text references)
    - We cannot locate the authority content (conservative: don't flag)

    This prevents false positives where multiple workspaces REFERENCE the same
    rules without actually contradicting them.
    """
    # Strip full calendar dates (YYYY-MM-DD) BEFORE extracting numeric ranges,
    # so that "2026-03-04" does not produce spurious range hits like "03-04".
    date_pat = re.compile(r'\d{4}-\d{2}-\d{2}')
    # Match numeric ranges like 55-70 or 35-55 (age ranges, day ranges, etc.)
    # Use 1-3 digit groups only to avoid matching year fragments.
    range_pat = re.compile(r'(?<!\d)\d{1,3}[-–]\d{1,3}(?!\d)')
    pct_pat = re.compile(r'\d+%')

    def extract_values(lines):
        vals = set()
        for line in lines:
            cleaned = date_pat.sub('', line)  # remove calendar dates first
            vals.update(range_pat.findall(cleaned))
            vals.update(pct_pat.findall(cleaned))
        return vals

    # Locate authority lines.  Three strategies in priority order:
    # 1. Any file in matches whose path ends with the authority path
    # 2. Any file in matches that belongs to the authority workspace
    # 3. Read the authority file directly from disk (handles shared/ authorities)
    auth_ws_prefix = authority.split("/")[0]  # e.g. "shared" or "workspace-insight"
    authority_rel = next((f for f in matches if f.endswith(authority) or authority in f), None)
    if not authority_rel:
        authority_rel = next((f for f in matches if f.startswith(auth_ws_prefix)), None)

    if authority_rel:
        authority_lines = matches[authority_rel]
    else:
        # e.g. authority = "shared/DECISIONS.md" — not scanned but exists on disk
        auth_path = root / authority
        auth_text = read_file_safe(auth_path)
        if not auth_text:
            # Cannot find authority at all — conservatively do NOT flag
            return False
        authority_lines = auth_text.splitlines()

    # Extract values that the authority EXPLICITLY BANS (values near prohibition language).
    # Only these constitute a real conflict when a non-authority file uses them.
    ban_markers = ["禁止", "禁", "红线", "不得", "废弃", "已废弃", "错误", "旧值"]

    def extract_banned_values(lines):
        """Values that appear in lines containing explicit prohibition language."""
        vals = set()
        for line in lines:
            if any(bm in line for bm in ban_markers):
                cleaned = date_pat.sub('', line)
                vals.update(range_pat.findall(cleaned))
                vals.update(pct_pat.findall(cleaned))
        return vals

    banned_values = extract_banned_values(authority_lines)

    if not banned_values:
        # Authority has no explicitly banned numeric values → no numeric conflict possible.
        return False

    # A real conflict: a non-authority file uses a banned value in an AFFIRMATIVE (non-banning) context.
    # If the line also contains a ban marker, it's just copying the rule correctly — not a conflict.
    for fpath, flines in matches.items():
        if fpath.startswith(auth_ws_prefix) or (authority_rel and fpath == authority_rel):
            continue
        for fline in flines:
            # Skip lines that are themselves prohibiting the value (consistent with authority)
            if any(bm in fline for bm in ban_markers):
                continue
            cleaned = date_pat.sub('', fline)
            line_values = set(range_pat.findall(cleaned)) | set(pct_pat.findall(cleaned))
            if line_values & banned_values:  # affirmative use of a banned value = real conflict
                return True

    return False  # No genuine conflict detected


def check_cross_workspace_conflict(cfg, report, agents, root):
    tracked = cfg.get("tracked_concepts", [])
    if not tracked:
        return

    for concept in tracked:
        name = concept.get("name", "未命名概念")
        keywords = concept.get("keywords", [])
        authority = concept.get("authority", "shared/DECISIONS.md")
        if not keywords:
            continue

        matches = {}
        for agent in agents:
            ws_path = root / f"workspace-{agent}"
            for fname in ("MEMORY.md", "SOUL.md"):
                fpath = ws_path / fname
                content = read_file_safe(fpath)
                if not content:
                    continue
                lines = [ln.strip() for ln in content.splitlines() if any(kw in ln for kw in keywords)]
                if lines:
                    rel = str(fpath.relative_to(root))
                    matches[rel] = lines[:3]

        if len(matches) > 1:
            # Only report as a conflict when non-authority files contain values
            # that genuinely differ from the authority (e.g., wrong age range).
            # Consistent references to the same rules are NOT conflicts.
            if not _has_genuine_value_conflict(matches, authority, root):
                continue

            evidence = []
            for fpath, lines in matches.items():
                evidence.append(f"{fpath}:")
                for ln in lines:
                    evidence.append(f"  - {ln[:120]}")

            report.add_issue(
                f"cross_workspace_conflict_{name}", "HIGH",
                f"概念「{name}」在多个 workspace 定义，存在冲突风险",
                f"统一到权威来源 {authority}，其余文件改为引用",
                list(matches.keys())[:10],
                evidence=evidence[:8],
                fix_action=f"在飞书群同步 {name} 的唯一权威定义（{authority}）"
            )


def check_shared_sync_drift(cfg, report, agents, root):
    decisions_path = root / "shared" / "DECISIONS.md"
    decisions_content = read_file_safe(decisions_path)
    if not decisions_content:
        report.add_issue(
            "shared_decisions_missing", "HIGH",
            "shared/DECISIONS.md 缺失或为空，跨 agent 决策无法统一",
            "创建 shared/DECISIONS.md 并写入关键决策",
            [str(decisions_path)],
            evidence=["shared/DECISIONS.md 不存在或内容为空"],
            fix_action="在飞书群通知 techops 初始化 shared/DECISIONS.md"
        )
        return

    critical_ids = cfg.get("critical_decisions", [])
    for did in critical_ids:
        if did not in decisions_content:
            report.add_issue(
                f"critical_decision_missing_{did}", "HIGH",
                f"关键决策 {did} 未出现在 shared/DECISIONS.md",
                f"将 {did} 补充到 shared/DECISIONS.md",
                [str(decisions_path)],
                evidence=[f"未命中关键决策 ID: {did}"],
                fix_action=f"在飞书群通知负责人补录 {did}"
            )
            continue

        section_lines = []
        in_section = False
        for line in decisions_content.splitlines():
            if did in line:
                in_section = True
            if in_section:
                if line.startswith("### ") and did not in line:
                    break
                section_lines.append(line)
        section = "\n".join(section_lines)

        affected_agents = []
        if "fansgrowth" in section or "小音" in section:
            affected_agents.append("fansgrowth")
        if "private" in section or "小私" in section:
            affected_agents.append("private")
        if "所有 agent" in section or "全体 agent" in section:
            affected_agents = list(agents)

        key_phrases = []
        if did == "D-010":
            key_phrases = ["高危操作", "禁止自动执行", "人工确认"]
        elif did == "D-003":
            key_phrases = ["Day 1-21", "禁推扩课", "禁止推扩课"]
        elif did == "D-004":
            key_phrases = ["删v率", "5%", "红线"]

        for agent in affected_agents:
            soul_path = root / f"workspace-{agent}" / "SOUL.md"
            soul_content = read_file_safe(soul_path)
            if not soul_content:
                continue
            has_equivalent = did in soul_content or any(p in soul_content for p in key_phrases)
            if not has_equivalent:
                report.add_issue(
                    f"shared_sync_drift_{did}_{agent}", "HIGH",
                    f"{did} 影响 workspace-{agent}，但其 SOUL.md 未体现约束",
                    f"在 workspace-{agent}/SOUL.md 中补充 {did} 对应规则",
                    [str(soul_path)],
                    evidence=[f"未命中 {did} 及关键短语: {', '.join(key_phrases) or 'N/A'}"],
                    fix_action=f"在飞书群通知 workspace-{agent} 负责人同步 {did}"
                )


def check_decision_propagation(cfg, report, agents, root):
    party_memory = root / "workspace-party" / "MEMORY.md"
    shared_decisions = root / "shared" / "DECISIONS.md"

    party_content = read_file_safe(party_memory)
    shared_content = read_file_safe(shared_decisions)
    if not party_content or not shared_content:
        return

    in_decisions = False
    party_decisions = []
    for line in party_content.splitlines():
        if "重要长期决策" in line or "重要决策" in line:
            in_decisions = True
            continue
        if in_decisions:
            if line.startswith("---") or (line.startswith("#") and "重要" not in line):
                break
            if "|" in line and line.count("|") >= 3:
                cells = [c.strip() for c in line.split("|")]
                cells = [c for c in cells if c and c != "---"]
                if len(cells) >= 2 and cells[0] not in ("决策", "---", ""):
                    party_decisions.append(cells[0])

    for decision_name in party_decisions:
        if decision_name not in shared_content:
            report.add_issue(
                f"decision_propagation_{decision_name}", "HIGH",
                f"party MEMORY 决策「{decision_name}」未同步到 shared/DECISIONS.md",
                "将该决策写入 shared/DECISIONS.md，确保所有 agent 可读",
                [str(party_memory), str(shared_decisions)],
                evidence=[f"shared/DECISIONS.md 未命中决策: {decision_name}"],
                fix_action=f"在飞书群通知操盘手把「{decision_name}」同步到 shared 层"
            )


def main():
    config = get_watchdog_config()
    report = WatchdogReport("memory")
    mem_cfg = config.get("memory", {}).get("checks", [])
    agents = auto_detect_agents(config)
    root = Path(get_openclaw_root())

    has_memory = any(
        (root / f"workspace-{a}" / "MEMORY.md").exists() or
        (root / f"workspace-{a}" / "memory").is_dir()
        for a in agents
    )
    if not has_memory:
        report.mark_not_applicable("没有任何 workspace 包含 MEMORY.md 或 memory/ 目录")
        report.save()
        return

    stats = {}
    session_count = sum(
        1 for a in agents
        if (root / f"workspace-{a}" / "MEMORY.md").exists()
    )
    stats["sessions"] = session_count

    checkers = {
        "cross_workspace_conflict": check_cross_workspace_conflict,
        "memory_staleness": lambda cfg, r, a, rt: check_memory_staleness(cfg, r, a, rt, stats),
        "memory_bloat": lambda cfg, r, a, rt: check_memory_bloat(cfg, r, a, rt, stats),
        "shared_sync_drift": check_shared_sync_drift,
        "decision_propagation": check_decision_propagation,
        "orphan_memory": check_orphan_memory,
    }

    for chk in mem_cfg:
        if chk.get("enabled", True):
            fn = checkers.get(chk["id"])
            if fn:
                fn(chk, report, agents, root)

    check_sensitive_info(report, agents, root, stats)

    report.set_metadata("sessions", stats.get("sessions", 0))
    report.set_metadata("stale_sessions", stats.get("stale_ratio", "0%"))
    report.set_metadata("sensitive_hits", stats.get("sensitive_hits", 0))
    report.set_metadata("retention_policy", "14 天后建议归档（手动触发 archive.py）")
    report.set_metadata("total_dated_files", stats.get("total_dated_files", 0))

    report.save()


if __name__ == "__main__":
    main()
