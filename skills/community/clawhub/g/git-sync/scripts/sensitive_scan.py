#!/usr/bin/env python3
"""
sensitive_scan.py - 敏感信息扫描与脱敏模块

扫描技能目录中的敏感信息（邮箱、token、IP、路径、用户名等），
并支持交互式确认脱敏策略。

用法:
  python sensitive_scan.py scan <skill_dir> [--config config.json]
  python sensitive_scan.py sanitize <file_path> <replacements_json>
  python sensitive_scan.py interactive <scan_result_json>
"""

import json
import os
import re
import sys
import argparse
from pathlib import Path

# ── 路径集中管理 ─────────────────────────────────────────
from _paths import (
    _data_dir_abs, DEFAULT_DATA_DIR_RAW, SKILL_DIR, SKILLS_ROOT as SKILLS_DIR,
    CONFIG_FILE,
)




def normalize_path(p):
    """将路径规范化为 Windows 绝对路径（处理 Git Bash /c/... 格式）"""
    p = os.path.expanduser(p)
    if p.startswith("/") and len(p) > 2 and p[1].isalpha() and p[2] == "/":
        p = p[1].upper() + ":" + p[2:].replace("/", "\\")
    return os.path.normpath(p)

# ── 敏感信息检测规则 ───────────────────────────────────────────────────

# 要扫描的文件扩展名
SCAN_EXTENSIONS = {".py", ".sh", ".md", ".json", ".yml", ".yaml", ".txt", ".cfg", ".ini"}

# 要排除的文件（相对技能目录）
EXCLUDE_FILES = {
    "SKILL.md",  # 文档通常不含真实敏感信息，但作者名需特殊处理
    "_meta.json",  # author 是署名，默认不脱敏
    "config.json",  # 本地配置文件，不含真实敏感信息（值为占位符或用户本地值）
}

# 敏感信息正则规则（按优先级排序）
SENSITIVE_PATTERNS = [
    # 1. 邮箱地址
    {
        "label": "邮箱地址",
        "regex": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "replace": "[email-redacted]",
        "severity": "high",
    },
    # 2. 私有 IP（内网）
    {
        "label": "内网IP（10.x）",
        "regex": r"10\.\d{1,3}\.\d{1,3}\.\d{1,3}",
        "replace": "[internal-ip-redacted]",
        "severity": "medium",
    },
    {
        "label": "内网IP（172.16-31.x）",
        "regex": r"172\.(1[6-9]|2[0-9]|3[01])\.\d{1,3}\.\d{1,3}",
        "replace": "[internal-ip-redacted]",
        "severity": "medium",
    },
    {
        "label": "内网IP（192.168.x）",
        "regex": r"192\.168\.\d{1,3}\.\d{1,3}",
        "replace": "[internal-ip-redacted]",
        "severity": "medium",
    },
    # 3. Token / API Key / Secret（常见模式）
    {
        "label": "Token/API密钥",
        "regex": r"""(?i)(token|api[_-]?key|apikey|secret|password|passwd|pwd)\s*[=:]\s*['"]?([a-zA-Z0-9_\-/\.]{16,})['"]?""",
        "replace": "[credential-redacted]",
        "severity": "critical",
        "group": 2,  # 只替换值部分
    },
    # 4. 私钥内容（PEM 格式）
    {
        "label": "私钥内容",
        "regex": r"-----BEGIN [A-Z]+ PRIVATE KEY-----.+-----END [A-Z]+ PRIVATE KEY-----",
        "replace": "[private-key-redacted]",
        "severity": "critical",
        "flags": re.DOTALL,
    },
    # 5. 本地绝对路径（Windows + Unix）
    {
        "label": "本地绝对路径",
        "regex": r"""(?i)[a-zA-Z]:\\[Users|home|root]\\[a-zA-Z0-9._-]+""",
        "replace": "[local-path-redacted]",
        "severity": "medium",
    },
    {
        "label": "Unix 家目录路径",
        "regex": r"/home/[a-zA-Z0-9._-]+/[a-zA-Z0-9._/ -]+",
        "replace": "[local-path-redacted]",
        "severity": "medium",
    },
]

# ── 工具函数 ─────────────────────────────────────────────────────────────



def load_config(config_path=None):
    """读取 skills/.standardization/git-sync/data/config.json，返回配置字典"""
    if config_path is None:
        config_path = str(CONFIG_FILE)
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def scan_file(file_path, config=None):
    """
    扫描单个文件，返回检测到的敏感信息列表。
    每个条目：{"label", "severity", "line", "match", "replace"}
    """
    results = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except (UnicodeDecodeError, PermissionError):
        # 二进制文件跳过
        return results

    # 1. 正则规则扫描
    for rule in SENSITIVE_PATTERNS:
        flags = rule.get("flags", 0)
        for m in re.finditer(rule["regex"], content, flags):
            group_idx = rule.get("group", 0)
            matched_text = m.group(group_idx) if group_idx else m.group(0)
            # 跳过占位符（如 your-name-here）
            if matched_text.startswith("your-") or matched_text in (
                "[email-redacted]", "[internal-ip-redacted]",
                "[credential-redacted]", "[private-key-redacted]",
                "[local-path-redacted]",
            ):
                continue
            results.append({
                "label": rule["label"],
                "severity": rule["severity"],
                "line": content[:m.start()].count("\n") + 1,
                "match": matched_text,
                "replace": rule["replace"],
                "span": (m.start(), m.end()),
            })

    # 2. 用户名扫描（来自 config.json 的 user/author 值 — 裸扫描，全部暴露给 LLM 判断）
    if config:
        usernames = set()
        for key in ("author",):
            v = config.get(key, "")
            if v and not v.startswith("your-"):
                usernames.add(v)
        for platform in ("gitee", "github"):
            v = config.get(platform, {}).get("user", "")
            if v and not v.startswith("your-"):
                usernames.add(v)
        for username in usernames:
            if len(username) < 3:
                continue
            # 在文件内容中搜索用户名（单词边界）
            for m in re.finditer(rf"\b{re.escape(username)}\b", content):
                matched_text = m.group(0)
                # 跳过 _meta.json 里的 author 字段（署名不需要脱敏）
                if file_path.endswith("_meta.json") and "author" in content[max(0, m.start()-20):m.end()+10]:
                    continue
                results.append({
                    "label": "用户名（来自配置）",
                    "severity": "low",
                    "line": content[:m.start()].count("\n") + 1,
                    "match": matched_text,
                    "replace": "[username-redacted]",
                    "span": (m.start(), m.end()),
                })

    # 按位置排序、去重
    results.sort(key=lambda x: x["span"][0])
    seen = set()
    deduped = []
    for r in results:
        key = (r["label"], r["span"][0], r["span"][1])
        if key not in seen:
            seen.add(key)
            deduped.append(r)
    return deduped

def scan_skill(skill_dir, config=None):
    """
    扫描整个技能目录，返回按文件组织的检测结果。
    返回：[{"file": rel_path, "description": "...", "findings": [...]}]
    """
    skill_dir = os.path.normpath(skill_dir)
    skill_name = os.path.basename(skill_dir)
    results = []

    for root, dirs, files in os.walk(skill_dir):
        # 排除 __pycache__ 等
        dirs[:] = [d for d in dirs if d != "__pycache__" and not d.startswith(".")]
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in SCAN_EXTENSIONS:
                continue
            rel_path = os.path.relpath(os.path.join(root, fname), skill_dir)
            # 排除特定文件
            if rel_path.replace("\\", "/") in EXCLUDE_FILES:
                continue
            findings = scan_file(os.path.join(root, fname), config)
            if findings:
                desc = _file_description(fname, skill_name)
                results.append({
                    "file": rel_path.replace("\\", "/"),
                    "description": desc,
                    "findings": findings,
                    "severity": _max_severity(f["severity"] for f in findings),
                })
    return results

def _file_description(fname, skill_name):
    """返回文件用途说明（中文）"""
    base = fname.lower()
    if base.endswith(".py"):
        return "Python 脚本，包含核心逻辑"
    if base.endswith(".sh"):
        return "Bash 脚本，包含执行逻辑"
    if base == "skill.md":
        return "技能说明文档"
    if base.endswith(".json") and "config" not in base:
        return "JSON 配置文件"
    if base.endswith(".json"):
        return "JSON 配置文件"
    if base.endswith(".md"):
        return "Markdown 文档"
    return "技能文件"

def _max_severity(severities):
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    return min(severities, key=lambda s: order.get(s, 99))

def build_replacements(findings_list):
    """
    根据检测结果构建替换字典 {match: replace}。
    对同一 match 文本，优先保留更具体的替换值。
    """
    replacements = {}
    for f in findings_list:
        replacements[f["match"]] = f["replace"]
    return replacements

def sanitize_content(content, replacements):
    """对内容执行脱敏替换（按 match 长度降序，避免子串优先替换）"""
    # 按 match 字符串长度降序排列，避免短串先替换导致长串匹配失败
    items = sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True)
    result = content
    for match_text, replace_with in items:
        if match_text in result:
            result = result.replace(match_text, replace_with)
    return result

def sanitize_file(file_path, replacements, backup=True):
    """对单个文件执行脱敏，可选备份原文件"""
    if backup:
        backup_path = file_path + ".bak"
        import shutil

        shutil.copy2(file_path, backup_path)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = sanitize_content(content, replacements)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return backup_path if backup else None

# ── 交互式确认（命令行菜单） ──────────────────────────────────────────────

SEVERITY_ICON = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
SEVERITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}

def format_findings_report(results):
    """格式化检测结果，供用户审阅"""
    if not results:
        return "  ✅ 未发现敏感信息。"
    lines = []
    lines.append(f"\n  发现 {len(results)} 个文件包含敏感信息：\n")
    for i, entry in enumerate(results, 1):
        icon = SEVERITY_ICON.get(entry["severity"], "⚪")
        lines.append(f"  {i}. [{icon}] {entry['file']}")
        lines.append(f"       └─ {entry['description']}")
        for f in entry["findings"]:
            ficon = SEVERITY_ICON.get(f["severity"], "⚪")
            lines.append(f"       ├─ {ficon} {f['label']}：「{_truncate(f['match'], 40)}」（第 {f['line']} 行）")
        lines.append("")
    return "\n".join(lines)

def _truncate(s, max_len):
    if len(s) <= max_len:
        return s
    return s[:max_len//2] + "..." + s[-(max_len//2 - 3):]

def interactive_review(results, batch_mode=False):
    """
    交互式确认每个文件的处理方式。
    返回：{"file_rel_path": "sanitize"|"keep"|"detailed", ...}
    batch_mode=True 时直接返回所有文件的处理方式（由外部处理）。
    """
    if not results:
        return {}

    print(format_findings_report(results))
    print("请选择处理方式：")
    print("  1) 全部脱敏（推荐，公开上架用）")
    print("  2) 全部保留（私有仓库用）")
    print("  3) 逐个文件选择")
    print("  4) 针对某个文件提更细的要求（如只脱敏特定条目）")
    print("  5) 中止同步/打包")
    print("")

    if batch_mode:
        # 非交互模式：返回 (results, needs_decision=True)
        return {"__needs_decision__": True, "__results__": results}

    while True:
        try:
            choice = input("  请输入选项 [1-5]: ").strip()
        except EOFError:
            # 无交互环境（如 cron），默认全部脱敏
            print("  ⚠️  无交互环境，默认全部脱敏")
            choice = "1"

        if choice == "1":
            return {e["file"]: "sanitize" for e in results}
        if choice == "2":
            return {e["file"]: "keep" for e in results}
        if choice == "3":
            return _per_file_choice(results)
        if choice == "4":
            return _detailed_choice(results)
        if choice == "5":
            print("  ❌ 已中止")
            sys.exit(1)

def _per_file_choice(results):
    """逐个文件选择"""
    decisions = {}
    for i, entry in enumerate(results, 1):
        icon = SEVERITY_ICON.get(entry["severity"], "⚪")
        print(f"\n  文件 {i}/{len(results)}：[{icon}] {entry['file']}")
        print(f"    说明：{entry['description']}")
        for f in entry["findings"][:3]:
            ficon = SEVERITY_ICON.get(f["severity"], "⚪")
            print(f"    · {ficon} {f['label']}：「{_truncate(f['match'], 30)}」")
        if len(entry["findings"]) > 3:
            print(f"    · ... 还有 {len(entry['findings']) - 3} 项")

        while True:
            r = input("  处理？（s=脱敏 / k=保留 / d=详细设置）：").strip().lower()
            if r in ("s", "sanitize"):
                decisions[entry["file"]] = "sanitize"
                break
            if r in ("k", "keep"):
                decisions[entry["file"]] = "keep"
                break
            if r in ("d", "detailed"):
                decisions[entry["file"]] = _detailed_for_file(entry)
                break
    return decisions

def _detailed_choice(results):
    """针对某个文件提更细要求"""
    decisions = {}
    while True:
        print("\n  输入文件编号查看详情，或输入 'done' 完成：")
        for i, entry in enumerate(results, 1):
            icon = SEVERITY_ICON.get(entry["severity"], "⚪")
            print(f"    {i}) [{icon}] {entry['file']}（{len(entry['findings'])} 项）")
        inp = input("  文件编号（或 done）: ").strip()
        if inp.lower() == "done":
            # 未选择的文件默认脱敏
            for entry in results:
                if entry["file"] not in decisions:
                    decisions[entry["file"]] = "sanitize"
            break
        if not inp.isdigit() or int(inp) < 1 or int(inp) > len(results):
            print("  ❌ 无效编号")
            continue
        idx = int(inp) - 1
        entry = results[idx]
        decisions[entry["file"]] = _detailed_for_file(entry)
    return decisions

def _detailed_for_file(entry):
    """对单个文件的每个敏感条目单独选择"""
    print(f"\n  文件：{entry['file']}")
    keep_set = set()
    for i, f in enumerate(entry["findings"], 1):
        icon = SEVERITY_ICON.get(f["severity"], "⚪")
        r = input(f"    {i}/{len(entry['findings'])} [{icon}] {f['label']}：「{_truncate(f['match'], 40)}」 脱敏？（y=脱敏 / n=保留）[Y/n]: ").strip().lower()
        if r in ("n", "no"):
            keep_set.add(f["match"])
    # 构建该文件的替换表（只替换用户同意的）
    replacements = {}
    for f in entry["findings"]:
        if f["match"] not in keep_set:
            replacements[f["match"]] = f["replace"]
    return {"mode": "custom", "replacements": replacements}

# ── CLI 入口 ─────────────────────────────────────────────────────────────

def cmd_scan(args):
    config = load_config(args.config)
    skill_dir = normalize_path(args.skill_dir)
    results = scan_skill(skill_dir, config)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"  ✅ 扫描结果已写入 {args.output}")
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    # 不要用 sys.exit，让调用方通过文件是否为空判断
    return

def cmd_sanitize(args):
    config = load_config(args.config)
    # args.file 是要脱敏的文件，args.replacements 是 JSON 文件或直接 JSON 字符串
    target_file = normalize_path(args.file)
    if os.path.exists(args.replacements):
        with open(args.replacements, "r", encoding="utf-8") as f:
            replacements = json.load(f)
    else:
        replacements = json.loads(args.replacements)
    backup = sanitize_file(target_file, replacements, backup=not args.no_backup)
    print(f"  ✅ 已脱敏：{args.file}" + (f"（备份：{backup}）" if backup else ""))

def cmd_interactive(args):
    if not os.path.exists(args.scan_result):
        print(f"  ❌ 扫描结果文件不存在：{args.scan_result}")
        sys.exit(1)
    with open(args.scan_result, "r", encoding="utf-8") as f:
        results = json.load(f)
    decisions = interactive_review(results, batch_mode=args.batch)
    if args.batch:
        # batch 模式：decisions 包含 __needs_decision__ 标记
        # 由外部（git-sync.sh）处理，这里只输出 JSON
        pass
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(decisions, f, ensure_ascii=False, indent=2)
        print(f"  ✅ 决策结果已写入 {args.output}")
    else:
        print(json.dumps(decisions, ensure_ascii=False, indent=2))

def cmd_apply(args):
    """根据决策 JSON，对技能目录中的文件执行脱敏/保留"""
    with open(args.decisions, "r", encoding="utf-8") as f:
        decisions = json.load(f)
    with open(args.scan_result, "r", encoding="utf-8") as f:
        results = json.load(f)
    skill_dir = normalize_path(args.skill_dir)
    # 构建 file → findings 映射
    file_findings = {e["file"]: e["findings"] for e in results}
    for file_rel, decision in decisions.items():
        if file_rel.startswith("__"):
            continue
        fpath = os.path.join(skill_dir, file_rel)
        if not os.path.exists(fpath):
            print(f"  ⚠️  文件不存在，跳过: {file_rel}")
            continue
        if decision == "keep":
            print(f"  ⏭️  保留（不脱敏）: {file_rel}")
            continue
        if decision == "sanitize":
            findings = file_findings.get(file_rel, [])
            replacements = build_replacements(findings)
            new_content = sanitize_content(open(fpath, "r", encoding="utf-8").read(), replacements)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"  ✅ 已脱敏: {file_rel}")
        elif isinstance(decision, dict) and decision.get("mode") == "custom":
            # 用户逐项选择的结果
            replacements = decision.get("replacements", {})
            new_content = sanitize_content(open(fpath, "r", encoding="utf-8").read(), replacements)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"  ✅ 已脱敏（部分）: {file_rel}")
    print(f"\n  ✅ 处理完成，技能目录: {skill_dir}")

def main():
    parser = argparse.ArgumentParser(description="敏感信息扫描与脱敏")
    sub = parser.add_subparsers(dest="command")

    # scan 子命令
    p_scan = sub.add_parser("scan", help="扫描技能目录")
    p_scan.add_argument("skill_dir", help="技能目录路径")
    p_scan.add_argument("--config", help="config.json 路径")
    p_scan.add_argument("--output", "-o", help="输出扫描结果到 JSON 文件")

    # sanitize 子命令
    p_san = sub.add_parser("sanitize", help="对文件执行脱敏替换")
    p_san.add_argument("file", help="要脱敏的文件路径")
    p_san.add_argument("replacements", help="替换表（JSON 文件或 JSON 字符串）")
    p_san.add_argument("--config", help="config.json 路径")
    p_san.add_argument("--no-backup", action="store_true", help="不备份原文件")

    # interactive 子命令
    p_int = sub.add_parser("interactive", help="交互式确认处理方式")
    p_int.add_argument("scan_result", help="扫描结果 JSON 文件")
    p_int.add_argument("--output", "-o", help="输出决策结果到 JSON 文件")
    p_int.add_argument("--batch", action="store_true", help="批量模式（不交互，只输出结果）")

    # apply 子命令（根据决策执行脱敏）
    p_app = sub.add_parser("apply", help="根据决策执行脱敏")
    p_app.add_argument("skill_dir", help="技能目录路径（脱敏目标）")
    p_app.add_argument("--decisions", required=True, help="决策 JSON 文件")
    p_app.add_argument("--scan-result", required=True, help="扫描结果 JSON 文件")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)
    dispatch = {
        "scan": cmd_scan,
        "sanitize": cmd_sanitize,
        "interactive": cmd_interactive,
        "apply": cmd_apply,
    }
    dispatch[args.command](args)

if __name__ == "__main__":
    main()
