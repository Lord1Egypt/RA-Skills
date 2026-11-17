#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""跨会议知识库 - 离线脚本（增强版 v3）。

聚合多场纪要素材，按类型(决策/行动项/风险/结论)抽取知识点建索引，
支持结构化行动项(负责人/DDL)、去重、统计，以及增强检索
(多关键词/容错/排序/高亮/JSON/类别过滤/跨会议冲突提示)。
每条条目带来源会议与章节，便于跨会议复用与追溯。

v3 改进（针对 TRACE 评测 R 维度）：
- 文件读取增加校验：二进制检测、空文件告警、编码异常统计，不再静默跳过。
- 构建结束时输出扫描摘要（总扫描 / 有效 / 跳过 / 告警）。
- 新增 --verbose 标志输出逐文件诊断详情。
- stats 输出含每文件贡献条目数，便于定位"哪个会议没被正确解析"。

纯标准库实现，零第三方依赖。支撑 meeting-kb-skill 的"可独立运行"。
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import date

# 分类顺序：特异性从高到低，用于"一行只归一个类别"的优先级判定，避免重复归类。
ORDER = ["决策", "行动项", "风险", "结论"]

CAT_KW = {
    "决策": ["决定", "拍板", "定下来", "决议", "定案", "定调"],
    "行动项": ["行动项", "待办", "跟进", "负责人", "DDL", "Deadline", "deadline", "截止", "@"],
    "风险": ["风险", "问题", "阻塞", "待决", "待确认", "延后", "延期", "卡点", "隐患"],
    "结论": ["结论", "要点", "共识", "总结", "明确为", "目标确定"],
}

# 章节标题 -> 类别（章节优先归类，比关键词更准）
SECTION_MAP = {
    "决策": "决策",
    "行动": "行动项",
    "待办": "行动项",
    "风险": "风险",
    "问题": "风险",
    "结论": "结论",
}

# 支持的文件扩展名
SUPPORTED_EXT = (".md", ".txt")

# 二进制检测阈值：前 8KB 中 null 字节占比超过此值视为二进制
BINARY_THRESHOLD = 0.05


def norm(s):
    """归一化：全角转半角、去标点与空白、小写。用于去重与检索容错。"""
    s = str(s)
    out = []
    for ch in s:
        code = ord(ch)
        if code == 0x3000:
            out.append(" ")
        elif 0xFF01 <= code <= 0xFF5E:
            out.append(chr(code - 0xFEE0))
        else:
            out.append(ch)
    s = "".join(out).lower()
    s = re.sub(r"[\s\-_/\\.,，。、：:；;!！?？()（）\[\]【】\"'\"'·\u2022\u2192]+", "", s)
    return s


def is_binary_file(filepath, sample_size=8192):
    """检测文件是否为二进制文件（基于 null 字节占比）。"""
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(sample_size)
        if not chunk:
            return False  # 空文件不算二进制
        null_count = chunk.count(b"\x00")
        return null_count / len(chunk) > BINARY_THRESHOLD
    except OSError:
        return False


def read_notes(input_dir, exclude=None, verbose=False):
    """读取目录中的纪要素材文件。

    返回 (notes, diagnostics)：
      notes: [(filename, content), ...]  \u2014 成功读取的有效文本
      diagnostics: dict \u2014 扫描诊断信息，含 warnings / skipped / errors 列表
    """
    diagnostics = {
        "total_scanned": 0,
        "valid_files": [],
        "skipped_ext": [],       # 不支持的扩展名
        "skipped_binary": [],    # 检测为二进制
        "skipped_empty": [],     # 空文件
        "warnings": [],          # 编码异常等警告
        "errors": [],             # 读取失败
    }

    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f"\u76ee\u5f55\u4e0d\u5b58\u5728\uff1a{input_dir}")

    try:
        entries = sorted(os.listdir(input_dir))
    except PermissionError as exc:
        raise PermissionError(f"\u65e0\u6cd5\u8bfb\u53d6\u76ee\u5f55\uff08\u6743\u9650\u4e0d\u8db3\uff09\uff1a{input_dir}") from exc

    notes = []
    for name in entries:
        if exclude and name == exclude:
            continue

        if name.startswith(".") or name.startswith("~"):
            continue

        p = os.path.join(input_dir, name)

        if os.path.isdir(p):
            continue

        diagnostics["total_scanned"] += 1

        ext_lower = os.path.splitext(name)[1].lower()
        if ext_lower not in SUPPORTED_EXT:
            diagnostics["skipped_ext"].append(name)
            if verbose:
                print(f"  [\u8df3\u8fc7] {name} \u2014 \u4e0d\u652f\u6301\u7684\u683c\u5f0f\uff08\u4ec5\u652f\u6301 .md/.txt\uff09", file=sys.stderr)
            continue

        if is_binary_file(p):
            diagnostics["skipped_binary"].append(name)
            print(
                f"  [\u8b66\u544a] {name} \u2014 \u68c0\u6d4b\u5230\u53ef\u80fd\u662f\u4e8c\u8fdb\u5236\u6587\u4ef6\uff0c\u5df2\u8df3\u8fc7\u3002"
                f"\u8bf7\u786e\u8ba4\u8be5\u6587\u4ef6\u662f\u5426\u4e3a\u7eaf\u6587\u672c\u4f1a\u8bae\u7eaa\u8981\u3002",
                file=sys.stderr,
            )
            continue

        try:
            with open(p, encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(p, encoding="gbk") as f:
                    content = f.read()
                diagnostics["warnings"].append(
                    f"{name} \u2014 \u975e UTF-8 \u7f16\u7801\uff08\u81ea\u52a8\u4ee5 GBK \u8bfb\u53d6\uff09\uff0c\u5efa\u8bae\u8f6c\u4e3a UTF-8 \u4ee5\u907f\u514d\u4e71\u7801"
                )
                if verbose:
                    print(f"  [\u8b66\u544a] {name} \u2014 \u7f16\u7801\u975e UTF-8\uff0c\u5df2\u7528 GBK \u517c\u5bb9\u8bfb\u53d6", file=sys.stderr)
            except Exception as exc:
                diagnostics["errors"].append(f"{name} \u2014 \u8bfb\u53d6\u5931\u8d25\uff1a{exc}")
                print(f"  [\u9519\u8bef] {name} \u2014 \u6587\u4ef6\u8bfb\u53d6\u5931\u8d25\uff1a{exc}", file=sys.stderr)
                continue
        except OSError as exc:
            diagnostics["errors"].append(f"{name} \u2014 \u8bfb\u53d6\u5931\u8d25\uff1a{exc}")
            print(f"  [\u9519\u8bef] {name} \u2014 \u6587\u4ef6\u8bfb\u53d6\u5931\u8d25\uff1a{exc}", file=sys.stderr)
            continue

        stripped = content.strip()
        if not stripped:
            diagnostics["skipped_empty"].append(name)
            if verbose:
                print(f"  [\u8df3\u8fc7] {name} \u2014 \u6587\u4ef6\u4e3a\u7a7a", file=sys.stderr)
            continue

        if len(stripped) < 10:
            diagnostics["warnings"].append(
                f"{name} \u2014 \u5185\u5bb9\u8fc7\u77ed\uff08{len(stripped)} \u5b57\u7266\uff09\uff0c\u53ef\u80fd\u4e0d\u662f\u5b8c\u6574\u4f1a\u8bae\u7eaa\u8981"
            )

        notes.append((name, content))
        diagnostics["valid_files"].append(name)

    return notes, diagnostics


def section_to_cat(section):
    if not section:
        return None
    for key, cat in SECTION_MAP.items():
        if key in section:
            return cat
    return None


def classify(line, section):
    """\u7ae0\u8282\u4f18\u5148\uff1b\u5426\u5219\u6309\u5173\u952e\u8bcd\u7279\u5f02\u6027\u4f18\u5148\u7ea7\uff0c\u4e00\u884c\u53ea\u5f52\u4e00\u4e2a\u7c7b\u522b\u3002"""
    sec_cat = section_to_cat(section)
    if sec_cat:
        return sec_cat
    for cat in ORDER:
        if any(k in line for k in CAT_KW[cat]):
            return cat
    return None


def extract_struct(text):
    """\u4ece\u884c\u52a8\u9879\u6587\u672c\u4e2d\u62bd\u53d6\u8d1f\u8d23\u4eba\u4e0e\u622a\u6b65\u65e5\u3002"""
    owner = None
    m = re.search(r"\u8d1f\u8d23\u4eba[：:]?\s*([\u4e00-\u9fa5A-Za-z]{1,6})", text)
    if m:
        owner = m.group(1)
    else:
        m = re.search(r"@\s*([\u4e00-\u9fa5A-Za-z]{1,6})", text)
        if m:
            owner = m.group(1)
    deadline = None
    m = re.search(r"(?:DDL|Deadline|deadline|\u622a\u6b62|\u6700\u665a)\s*[:：]?\s*([^\s\uff0c\u3002\u3001]+)", text)
    if m:
        deadline = m.group(1)
    else:
        m = re.search(r"(\u4e0b?\u5468[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u65e5\u5929])|(\d{1,2}\u6708\d{1,2}[\u65e5\u53f7]?)", text)
        if m:
            deadline = m.group(1) or m.group(2)
    return owner, deadline


def build(notes):
    kb = {c: [] for c in ORDER}
    seen = set()
    per_file_counts = Counter()

    for fname, text in notes:
        section = None
        file_count = 0
        for raw in text.splitlines():
            line = raw.strip()
            if not line:
                continue
            h = re.match(r"^#{1,6}\s*(.+?)\s*#*\s*$", line)
            if h:
                section = h.group(1).strip()
                continue
            cat = classify(line, section)
            if not cat:
                continue
            item = re.sub(r"^[-*]\s*", "", line)
            item = re.sub(r"^\d+[.、]\s*", "", item).strip()
            if not item:
                continue
            key = norm(item)
            if key in seen:
                continue
            seen.add(key)
            owner = deadline = None
            if cat == "\u884c\u52a8\u9879":
                owner, deadline = extract_struct(item)
            kb[cat].append({
                "src": fname,
                "section": section or "",
                "text": item,
                "owner": owner,
                "deadline": deadline,
            })
            file_count += 1
        per_file_counts[fname] = file_count

    return kb, per_file_counts


def render_kb(kb):
    lines = [f"# \u8de8\u4f1a\u8bae\u77e5\u8bc6\u5e93 \u00b7 {date.today()}",
             "",
             "> \u7531\u591a\u573a\u4f1a\u8bae\u7eaa\u8981\u591a\u6e90\u805a\u5408\uff0c\u6309\u7c7b\u578b\u6c89\u6dc0\uff0c\u4fbf\u4e8e\u8de8\u4f1a\u8bae\u68c0\u7d22\u4e0e\u590d\u7528\u3002\u6bcf\u6ce8\u660e\u6765\u6e90\u4f1a\u8bae\u4e0e\u7ae0\u8282\u3002",
             ""]
    for cat in ORDER:
        lines.append(f"## {cat}\uff08{len(kb[cat])}\uff09")
        for e in kb[cat]:
            extra = ""
            if cat == "\u884c\u52a8\u9879" and (e["owner"] or e["deadline"]):
                parts = []
                if e["owner"]:
                    parts.append(f"\u8d1f\u8d23\u4eba {e['owner']}")
                if e["deadline"]:
                    parts.append(f"DDL {e['deadline']}")
                extra = f"  _({' \u00b7 '.join(parts)})_"
            loc = e["section"] if e["section"] else ""
            src_line = f"\u3010{e['src']}\u3011" if not loc else f"\u3010{e['src']} \u00b7 {loc}\u3011"
            lines.append(f"- {src_line}{e['text']}{extra}")
        lines.append("")
    return "\n".join(lines)


def query(kb, kws, require_all=False, cat=None):
    cats = [cat] if cat else ORDER
    hits = []
    for c in cats:
        for e in kb[c]:
            hay = norm(e["text"] + " " + e["src"] + " " + (e["section"] or ""))
            matched = [k for k in kws if norm(k) in hay]
            ok = (len(matched) == len(kws)) if require_all else bool(matched)
            if ok:
                hits.append((len(matched), c, e, matched))
    hits.sort(key=lambda x: -x[0])
    return hits


def highlight(text, kws):
    for k in kws:
        if not k:
            continue
        text = re.sub(r"(" + re.escape(k) + r")", r"*\1*", text)
    return text


def print_stats(kb, per_file_counts=None):
    per_cat = {c: len(kb[c]) for c in ORDER}
    per_src = Counter(e["src"] for c in ORDER for e in kb[c])
    total = sum(per_cat.values())

    print(f"\n{'='*44}")
    print(f"  \u77e5\u8bc6\u5e93\u7edf\u8ba1\uff08\u5171 {total} \u6761\uff09")
    print(f"{'='*44}")
    header = f"  {'\u7c7b\u522b':<10}\u6570\u91cf"
    print(header)
    print(f"  {'-'*20}")
    for c in ORDER:
        print(f"  {c:<10}{per_cat[c]}")
    print()

    print(f"  {'\u6765\u6e90\u4f1a\u8bae':<22}\u8d21\u732e\u6761\u76ee")
    print(f"  {'-'*34}")
    for s, n in per_src.most_common():
        marker = ""
        if per_file_counts and per_file_counts.get(s, 0) == 0:
            marker = "  \u26a0\ufe0f \u8be5\u6587\u4ef6\u672a\u63d0\u53d6\u5230\u4efb\u4f55\u6761\u76ee"
        print(f"  {s:<22}{n}{marker}")

    if per_file_counts:
        zero_files = [f for f, cnt in per_file_counts.items() if cnt == 0]
        if zero_files:
            print()
            print(f"  \u26a0\ufe0f \u4ee5\u4e0b\u6587\u4ef6\u672a\u63d0\u53d6\u5230\u4efb\u4f55\u77e5\u8bc6\u70b9\uff1a")
            for zf in zero_files:
                print(f"    - {zf}\uff08\u53ef\u80fd\u7f3a\u5c11 ## \u51b3\u7b56 / ## \u884c\u52a8\u9879 \u7b49\u6807\u51c6\u7ae0\u8282\u6216\u5339\u914d\u5173\u952e\u8bcd\uff09")


def print_diagnostics(diagnostics):
    """\u6253\u5370\u626b\u63cf\u6458\u8981\uff08\u6784\u5efa\u7ed3\u675f\u65f6\u8c03\u7528\uff09\u3002"""
    d = diagnostics
    total = d["total_scanned"]
    valid = len(d["valid_files"])
    skipped = len(d["skipped_ext"]) + len(d["skipped_binary"]) + len(d["skipped_empty"])
    errs = len(d["errors"])
    warns = len(d["warnings"])

    print(f"\n{'\u2500'*46}")
    print(f"  \U0001f4ca \u626b\u63cf\u6458\u8981")
    print(f"{'\u2500'*46}")
    print(f"  \u603b\u626b\u63cf\u6587\u4ef6\uff1a{total}")
    print(f"  \u2705 \u6709\u6548\u7d20\u6750\uff1a{valid}")

    if skipped > 0:
        details = []
        if d["skipped_ext"]:
            details.append(f"\u683c\u5f0f\u4e0d\u652f\u6301 {len(d['skipped_ext'])} \u4e2a")
        if d["skipped_binary"]:
            details.append(f"\u4e8c\u8fdb\u5236 {len(d['skipped_binary'])} \u4e2a")
        if d["skipped_empty"]:
            details.append(f"\u7a7a\u6587\u4ef6 {len(d['skipped_empty'])} \u4e2a")
        print(f"  \u23ed\ufe0f \u5df2\u8df3\u8fc7\uff1a{skipped} \uff08{'; '.join(details)}\uff09")

    if errs > 0:
        print(f"  \u274c \u8bfb\u53d6\u5931\u8d25\uff1a{errs} \u4e2a")

    if warns > 0:
        print(f"  \u26a0\ufe0f \u544a\u8b66\uff1a{warns} \u6761")

    if total == 0:
        print()
        print(f"  \u2757 \u76ee\u5f55\u4e3a\u7a7a\uff0c\u8bf7\u68c0\u67e5 --input-dir \u8def\u5f84\u662f\u5426\u6b63\u786e\u3002")
    elif valid == 0 and total > 0:
        print()
        print(f"  \u2757 \u6709\u6587\u4ef6\u4f46\u65e0\u6709\u6548\u7d20\u6750\uff01\u8bf7\u68c0\u67e5\uff1a")
        print(f"     1. \u6587\u4ef6\u662f\u5426\u4e3a .md \u6216 .txt \u683c\u5f0f")
        print(f"     2. \u6587\u4ef6\u662f\u5426\u4e3a\u7a7a\u6216\u4e8c\u8fdb\u5236")
        print(f"     3. \u662f\u5426\u6709\u6743\u9650\u8bfb\u53d6\u8be5\u76ee\u5f55")

    print()


def main():
    ap = argparse.ArgumentParser(
        description="\u8de8\u4f1a\u8bae\u77e5\u8bc6\u5e93\uff08\u589e\u5f3a\u7248 v3\uff09",
        epilog=(
            "\u793a\u4f8b:\n"
            "  python kb_build.py --input-dir ./examples                     # \u6784\u5efa\u77e5\u8bc6\u5e93\n"
            "  python kb_build.py --input-dir ./examples --query \u652f\u4ed8       # OR \u68c0\u7d22\n"
            "  python kb_build.py --input-dir ./examples --query \u652f\u4ed8 --all   # AND \u68c0\u7d22\n"
            "  python kb_build.py --input-dir ./examples --stats              # \u7edf\u8ba1\n"
            "  python kb_build.py --input-dir ./examples --verbose            # \u8be6\u7ec6\u8bca\u65ad"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--input-dir", required=True, help="\u7eaa\u8981\u7d20\u6750\u76ee\u5f55(.md/.txt)")
    ap.add_argument("--output", default="\u77e5\u8bc6\u5e93.md", help="\u8f93\u51fa\u77e5\u8bc6\u5e93\u7d22\u5f15\u8def\u5f84(\u6784\u5efa\u6a21\u5f0f\uff0c\u9ed8\u8ba4 '\u77e5\u8bc6\u5e93.md')")
    ap.add_argument("--query", default=None, help="\u5173\u952e\u8bcd\uff0c\u7a7a\u683c\u5206\u9694\u591a\u4e2a(\u9ed8\u8ba4 OR)")
    ap.add_argument("--all", action="store_true", help="\u591a\u5173\u952e\u8bcd\u9700**u5168\u90e8\u547d\u4e2d**(AND)")
    ap.add_argument("--cat", default=None, choices=ORDER, help="\u9650\u5b9a\u68c0\u7d22\u7c7b\u522b")
    ap.add_argument("--json", action="store_true", help="\u4ee5 JSON \u8f93\u51fa\u68c0\u7d22\u7ed3\u679c")
    ap.add_argument("--stats", action="store_true", help="\u4ec5\u8f93\u51fa\u7edf\u8ba1")
    ap.add_argument("--verbose", action="store_true", help="\u8f93\u51fa\u9010\u6587\u4ef6\u8bca\u65ad\u8be6\u60c5\uff08\u8df3\u8fc7/\u544a\u8b66/\u7f16\u7801\uff09")
    args = ap.parse_args()

    # ---- 目录校验 ----
    if not os.path.isdir(args.input_dir):
        print(f"\u274c \u9519\u8bef\uff1a\u76ee\u5f55\u4e0d\u5b58\u5728 {args.input_dir}", file=sys.stderr)
        sys.exit(1)

    # ---- 读取素材（带诊断） ----
    try:
        notes, diag = read_notes(args.input_dir, exclude=os.path.basename(args.output), verbose=args.verbose)
    except (FileNotFoundError, PermissionError) as exc:
        print(f"\u274c \u9519\u8bef\uff1a{exc}", file=sys.stderr)
        sys.exit(1)

    if not notes:
        print_diagnostics(diag)
        sys.exit(1)

    # ---- 构建 ----
    kb, per_file_counts = build(notes)

    # ---- 输出模式 ----
    if args.stats:
        print_stats(kb, per_file_counts)
        print_diagnostics(diag)
        return

    if args.query:
        kws = [k.strip() for k in args.query.split() if k.strip()]
        if not kws:
            print("\u274c \u9519\u8bef\uff1a\u67e5\u8be2\u5173\u952e\u8bcd\u4e3a\u7a7a\uff0c\u8bf8\u63d0\u4f9b\u81f3\u5c11\u4e00\u4e2a\u5173\u952e\u8bcd\u3002", file=sys.stderr)
            sys.exit(1)

        hits = query(kb, kws, require_all=args.all, cat=args.cat)

        if not hits:
            mode_desc = "AND(\u5168\u90e8\u547d\u4e2d)" if args.all else "OR(\u547d\u4e2d\u4efb\u4e00)"
            cat_desc = f"\u3001\u9650\u5b9a\u7c7b\u522b=[{args.cat}]" if args.cat else ""
            print(f"\n\u67e5\u8be2\u300e{' '.join(kws)}\u300f({mode_desc}{cat_desc}) \u547d\u4e2d **0 \u6761**\u3002")
            print(f"\u5efa\u8bae\uff1a")
            print(f"  1. \u5c1d\u8bd5\u51cf\u5c11\u5173\u952e\u8bcd\u6570\u91cf\uff08OR \u6a21\u5f0f\u4e0b\u53ea\u9700\u547d\u4e2d\u4e00\u4e2a\u5373\u53ef\uff09")
            print(f"  2. \u68c0\u67e5\u62fc\u5199\u662f\u5426\u6b63\u786e\uff08\u5168/\u534a\u89d2\u3001\u5927\u5c0f\u5199\u5747\u5bb9\u9519\uff09")
            print(f"  3. \u4f7f\u7528 --stats \u786e\u8ba4\u77e5\u8bc6\u5e93\u662f\u5426\u542b\u6709\u8be5\u4e3b\u9898\u6761\u76ee")
            print(f"  4. \u53bb\u6389 --all \u53c2\u6570\u5207\u6362\u4e3a OR \u6a21\u5f0f\u91cd\u8bd5")
            sys.exit(0)

        if args.json:
            out = [{
                "cat": c, "src": e["src"], "section": e["section"],
                "text": e["text"], "owner": e["owner"], "deadline": e["deadline"],
                "matched": m,
            } for _, c, e, m in hits]
            print(json.dumps(out, ensure_ascii=False, indent=2))
        else:
            mode_str = " AND " if args.all else " "
            print(f"\n\u67e5\u8be2\u300e{' '.join(kws)}\u300f({mode_str.join(kws)}) \u547d\u4e2d **{len(hits)} \u6761**\uff1a")
            srcs = set(e["src"] for _, _, e, _ in hits)
            if len(srcs) > 1:
                print(f"\u26a0\ufe0f \u8be5\u4e3b\u9898\u6d89\u53ca **{len(srcs)}** \u4e2a\u4e0d\u540c\u4f1a\u8bae\uff0c\u7ed3\u8bba\u53ef\u80fd\u5b58\u5728\u5dee\u5f02\uff0c\u8bf7\u4eba\u5de5\u6838\u5bf9\u3002")
            print()
            for _, c, e, m in hits:
                extra = ""
                if e["owner"] or e["deadline"]:
                    parts = []
                    if e["owner"]:
                        parts.append(f"\u8d1f\u8d23\u4eba {e['owner']}")
                    if e["deadline"]:
                        parts.append(f"DDL {e['deadline']}")
                    extra = f"  _({' \u00b7 '.join(parts)})_"
                print(f"  [{c}]\u3010{e['src']}\u3011{highlight(e['text'], m)}{extra}")
    else:
        out = render_kb(kb)
        abs_output = os.path.abspath(args.output)
        with open(abs_output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"\u2705 \u5df2\u6784\u5efa\u77e5\u8bc6\u5e93\uff1a{abs_output}")
        print_stats(kb, per_file_counts)
        print_diagnostics(diag)


if __name__ == "__main__":
    main()
