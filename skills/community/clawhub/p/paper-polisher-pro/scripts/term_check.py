#!/usr/bin/env python3
"""
Term Normalization Checker — paper-polisher-pro (package version: see SKILL.md frontmatter)
Check non-standard medical terminology against authority databases.

Usage:
    python3 term_check.py <input_file>
    python3 term_check.py <input_file> --output report.json
    python3 term_check.py <input_file> --auto-fix
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

LOCAL_JSON = Path(__file__).parent.parent / "data" / "terminology.json"

@dataclass
class TermIssue:
    original: str
    standard: str
    source: str
    position: int  # char offset
    context: str   # surrounding text snippet
    en_name: str = ""

@dataclass
class TermReport:
    file: str = ""
    total_issues: int = 0
    standardization_rate: float = 0.0  # percentage of terms that ARE standard
    issues: list = field(default_factory=list)
    summary: str = ""


def load_custom_bank(path):
    """v7.1.0: 加载自定义术语库（--bank）——格式与内置 terminology.json 相同
    （数组，每条 {cn, en?, aliases?, source?}），逐条校验带行号（坏条目不静默吞）。"""
    items, warns = [], []
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as e:
        return [], [f"自定义词表解析失败: {e}"]
    if not isinstance(data, list):
        return [], ["自定义词表必须是数组（[{cn, en?, aliases?, source?}, …]）"]
    for i, item in enumerate(data, 1):
        if not isinstance(item, dict) or not item.get("cn"):
            warns.append(f"第 {i} 条缺 cn 字段，已跳过")
            continue
        items.append(item)
    return items, warns


def load_terminology(custom_path=None) -> dict:
    """Load terms from local terminology.json (portable, no external dependencies).

    v7.1.0: custom_path（--bank）非空时加载自定义词表并与内置合并——
    同 cn 覆盖内置条目（项目自有缩写/机构名的统一走项目词表）。"""
    terms = {}
    
    if not LOCAL_JSON.exists():
        print(f"Error: terminology data not found at {LOCAL_JSON}", file=sys.stderr)
        return terms
    
    try:
        with open(LOCAL_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            cn_name = item["cn"]
            entry = {"standard": cn_name, "en": item.get("en", ""), "source": item.get("source", "")}
            terms[cn_name.lower()] = entry
            for alias in item.get("aliases", []):
                alias = alias.strip()
                if alias and len(alias) >= 2 and alias.lower() != cn_name.lower():
                    # 跳过歧义极大的极短纯ASCII别名(AT/AR/AD等会被子串误匹配到普通英文)
                    if re.fullmatch(r"[a-zA-Z]{1,3}", alias):
                        continue
                    terms[alias.lower()] = entry
        if custom_path:
            citems, cwarns = load_custom_bank(custom_path)
            for w in cwarns:
                print(f"Warning: {w}", file=sys.stderr)
            for item in citems:
                cn_name = str(item["cn"]).strip()
                entry = {"standard": cn_name, "en": item.get("en", ""),
                         "source": item.get("source", "") or "项目自定义词表"}
                terms[cn_name.lower()] = entry
                for alias in item.get("aliases", []):
                    alias = str(alias).strip()
                    if alias and len(alias) >= 2 and alias.lower() != cn_name.lower():
                        if re.fullmatch(r"[a-zA-Z]{1,3}", alias):
                            continue
                        terms[alias.lower()] = entry
            print(f"自定义词表: +{len(citems)} 条（合并后共 "
                  f"{len(set(e['standard'] for e in terms.values()))} 个概念）", file=sys.stderr)
        print(f"Loaded {len(set(e['standard'] for e in terms.values()))} terms from local JSON", file=sys.stderr)
    except Exception as e:
        print(f"Error: Failed to load terminology: {e}", file=sys.stderr)
    
    return terms


def check_terms(text: str, terms_db: dict) -> TermReport:
    """Check text against terminology database by searching for all known terms."""
    
    if not terms_db:
        return TermReport(summary="术语库为空，无法检查。")
    
    # Get unique standard terms
    standard_terms = {}
    for key, entry in terms_db.items():
        std = entry["standard"]
        if std not in standard_terms:
            standard_terms[std] = entry
    
    issues = []
    standard_count = 0
    checked_positions = set()  # Avoid overlapping matches

    # v5.8.1 匹配机制修复：单遍收集全部候选（标准词+别名），按长度降序全局裁决。
    # 旧两遍扫描（先标准后别名）会被短标准词占位挡掉更长别名（"母源抗体"被"抗体"占位漏报）。
    candidates = []  # (pos, end, std_name, entry, is_alias)
    sorted_terms = sorted(standard_terms.items(), key=lambda x: len(x[0]), reverse=True)
    for std_name, entry in sorted_terms:
        for m in re.finditer(re.escape(std_name), text):
            candidates.append((m.start(), m.start() + len(std_name), std_name, entry, False))
    for alias_lower, entry in terms_db.items():
        std_name = entry["standard"]
        if alias_lower == std_name.lower():
            continue  # Skip standard names (already counted)
        # 词边界保护(v3修复): 英文别名必须前后是词边界, 避免把 "baricitinib" 里的 "ar" 当成 AR
        alias_pat = alias_lower
        if re.fullmatch(r"[a-zA-Z]+", alias_pat):
            pattern = r"(?<![a-zA-Z])" + re.escape(alias_pat) + r"(?![a-zA-Z])"
        else:
            pattern = re.escape(alias_pat)
        for m in re.finditer(pattern, text, re.IGNORECASE):
            candidates.append((m.start(), m.start() + len(alias_lower), std_name, entry, True))

    # 全局裁决：长者优先认领区间；同长同位时标准词优先于别名
    candidates.sort(key=lambda c: (-(c[1] - c[0]), c[0], c[4]))
    for pos, end, std_name, entry, is_alias in candidates:
        if any(s <= pos < e or s < end <= e for s, e in checked_positions):
            continue
        if not is_alias:
            checked_positions.add((pos, end))
            standard_count += 1
            continue

        # 派生词后缀排除(中文): 避免"风湿病"误报"风湿病学家/风湿病学/风湿病学会"
        # 等合法派生词。被排除的候选不认领区间，让更短的合法匹配有机会落位。
        rest = text[end:end + 4]
        SINGLE_SUFFIXES = ("家", "刊", "报", "类", "系", "学")
        DERIVATION_SUFFIXES = ("学家", "学会", "学分", "学科", "科学",
                               "分会", "中心", "专科", "科室", "研究",
                               "学院", "医院", "医师", "杂志", "手册",
                               "主任", "教授", "学系", "理论")
        if rest and (any(rest.startswith(s) for s in DERIVATION_SUFFIXES)
                     or rest[:1] in SINGLE_SUFFIXES):
            continue  # 合法派生词(如"风湿病学家"), 不算非标准用法
        # 专名机构后缀排除: "美国风湿病学会""中华风湿病学会"等为官方中文名, 保留原名
        PRECEDING_NAME_CHARS = ("国", "华", "洲", "际", "盟")
        if rest.startswith("会") and pos > 0 and text[pos - 1] in PRECEDING_NAME_CHARS:
            continue  # 官方机构名, 保留原名
        checked_positions.add((pos, end))

        context_start = max(0, pos - 15)
        context_end = min(len(text), end + 15)
        issues.append(TermIssue(
            original=text[pos:end],
            standard=std_name,
            source=entry["source"],
            position=pos,
            context=text[context_start:context_end],
            en_name=entry.get("en", "")
        ))

    total_known = standard_count + len(issues)
    rate = (standard_count / total_known * 100) if total_known > 0 else 0
    
    # Build summary
    if not issues:
        summary = f"✅ 术语检查通过。检测到 {standard_count} 个标准术语，无非标准用法。"
    else:
        lines = [f"发现 {len(issues)} 处非标准术语（标准率 {rate:.1f}%）："]
        for i, issue in enumerate(issues, 1):
            lines.append(f"  {i}. \"{issue.original}\" → 标准名: \"{issue.standard}\"（{issue.source}）")
            if issue.en_name:
                lines.append(f"     英文: {issue.en_name}")
        summary = "\n".join(lines)

    # ── 全称规范检查 (full-name normalization) ──────────────────────
    # 主匹配阶段会因短标准名(如"干扰素")占位而漏掉"该用全称却用了简称"的情况。
    # 这里独立扫一遍: 凡是裸称出现且前面不是规范型号前缀的, 提示补全为全称。
    # 规则可扩展: (裸称正则, 应有前缀集合, 全称, 说明)
    FULL_NAME_RULES = [
        # 裸称"干扰素病"前若不是 Ⅰ型/II型/III型/二型/三型 等, 应补为"Ⅰ型干扰素病"
        (re.compile(r"(?<![ⅠIIⅢ二三四1-3])(?<![型iI一])干扰素病"),
         "Ⅰ型干扰素病",
         "全程全称规范(2026-06): 干扰素病首次/正式出现须写全称 Ⅰ型干扰素病"),
    ]
    covered = set()
    for (s, e) in checked_positions:
        for p in range(s, e):
            covered.add(p)
    for pat, full_name, note in FULL_NAME_RULES:
        for m in pat.finditer(text):
            pos = m.start()
            end = m.end()
            # 全称规范独立判定: 不受短标准名(如"干扰素")占位影响。
            # 正则的负向后顾已确保只抓"前面无型号前缀"的裸称,
            # 因此即使与"干扰素"位置重叠, 该裸称仍是需要补全的独立问题点。
            # (不检查 covered, 避免漏报)
            context_start = max(0, pos - 15)
            context_end = min(len(text), end + 15)
            issues.append(TermIssue(
                original=text[pos:end],
                standard=full_name,
                source=note,
                position=pos,
                context=text[context_start:context_end],
                en_name=""
            ))
    # 重算标准率与摘要(全称规范问题也算 issue)
    total_known = standard_count + len(issues)
    rate = (standard_count / total_known * 100) if total_known > 0 else 0
    if not issues:
        summary = f"✅ 术语检查通过。检测到 {standard_count} 个标准术语，无非标准用法。"
    else:
        lines = [f"发现 {len(issues)} 处非标准术语（标准率 {rate:.1f}%）："]
        for i, issue in enumerate(issues, 1):
            lines.append(f"  {i}. \"{issue.original}\" → 标准名: \"{issue.standard}\"（{issue.source}）")
            if issue.en_name:
                lines.append(f"     英文: {issue.en_name}")
        summary = "\n".join(lines)

    return TermReport(
        total_issues=len(issues),
        standardization_rate=round(rate, 1),
        issues=[asdict(i) for i in issues],
        summary=summary
    )


def auto_fix(text: str, issues: list) -> str:
    """Auto-replace non-standard terms with standard ones.
    
    Uses position-based replacement to avoid substring collisions:
    1. Sort issues by length (longest first)
    2. Find all match positions
    3. Replace from end to start to preserve indices
    4. Skip any matches that overlap with already-replaced regions
    """
    if not issues:
        return text
    
    # Sort by original length descending (longest match first)
    sorted_issues = sorted(issues, key=lambda x: len(x["original"]), reverse=True)
    
    # Collect all replacement regions: (start, end, standard)
    regions = []
    for issue in sorted_issues:
        original = issue["original"]
        standard = issue["standard"]
        start = 0
        while True:
            pos = text.find(original, start)
            if pos == -1:
                break
            # Check no overlap with existing regions
            end = pos + len(original)
            overlaps = any(not (end <= r[0] or pos >= r[1]) for r in regions)
            if not overlaps:
                regions.append((pos, end, standard))
            start = pos + 1
    
    # Sort regions by position descending (replace from end to preserve indices)
    regions.sort(key=lambda r: r[0], reverse=True)
    
    # Apply replacements
    result = text
    for start, end, standard in regions:
        result = result[:start] + standard + result[end:]
    
    return result


NOTICE = "ℹ️ 供学术写作自查与质量改进使用；不用于规避机构 AIGC 检测，请遵循所在机构的 AI 使用与披露政策。"


# ── v5.9.0: 词典外新造词探测（opt-in，建议性，未校准） ─────────────────────
# 背景（实战对照表 2026-10-16 需求 2）：词典匹配对词典外自创词不可见——15 个自创词
# 扩展前漏检 14 个。本启发式把「文本里高频出现、却不在术语库」的字串提示给
# 人工复核。诚实边界：无校准语料、误报不可控，因此 ①默认关闭（--neologism
# 显式开启）②只提示不判定对错 ③永不计分、永不汇入门禁复合分。
_NEOLexer_STOP = frozenset("""
我们 他们 自己 这个 那个 这些 那些 研究 结果 显示 表明 提示 患者 治疗 细胞
数据 分析 临床 不同 出现 进行 检测 检查 诊断 观察 比较 方法 材料 实验 模型
系统 功能 相关 以及 同时 此外 因此 但是 而且 或者 可以 可能 导致 引起 发生
存在 具有 包括 根据 通过 对于 关于 由于 除了 需要 应该 建议 注意 重要 主要
部分 一些 以下 上述 综合 总结 结论 讨论 目的 背景 意义 价值 影响 作用 效果
变化 增加 减少 升高 降低 水平 指标 情况 状态 过程 阶段 时期 时间 年龄 性别
病例 报告 文献 参考 标准 规范 检验 血清 免疫 蛋白 基因 突变 阳性 阴性 急性
慢性 重度 轻度 中度 目前 目前 异常 正常 范围 区间 评估 判断 判读 结合 分布
表达 活性 反应 因子 受体 综合 其中 以上 之间 由于 各种 某些 该患 本例 全文
""".split())


def find_neologisms(text: str, terms_db: dict, top_n: int = 10):
    """词典外高频字串提示（启发式，未校准；只作人工核对线索）。

    规则：CJK 连续段内取 2-4 字窗口；3-4 字串出现 ≥2 次或 2 字串出现 ≥4 次
    入候选；排除术语库已知词（含别名）、库内任何词的子串、停用词。
    返回 [{term, count}]，按 (次数降序, 长度降序) 截 top_n。
    """
    import re as _re
    from collections import Counter
    known = set(terms_db.keys())
    known |= {e["standard"].lower() for e in terms_db.values()}
    known_blob = "|".join(sorted((k for k in known if len(k) >= 2), key=len, reverse=True))
    runs = _re.findall(r"[\u4e00-\u9fff]{2,}", text)
    counter = Counter()
    for run in runs:
        for n in (2, 3, 4):
            for i in range(len(run) - n + 1):
                counter[run[i:i + n]] += 1
    out = []
    for w, c in counter.items():
        if w in _NEOLexer_STOP or w in known:
            continue
        if known_blob and w in known_blob:
            continue  # 库内更长词的组成片段（如「特异」⊂「年龄特异性」）不提示
        need = 4 if len(w) == 2 else 2
        if c >= need:
            out.append({"term": w, "count": c})
    out.sort(key=lambda x: (-x["count"], -len(x["term"])))
    # 去掉被更长保留项包含的短候选
    kept = []
    for x in out:
        if not any(x["term"] in k["term"] for k in kept):
            kept.append(x)
    return kept[:top_n]


def main():
    parser = argparse.ArgumentParser(description="Term Normalization Checker")
    parser.add_argument("input", help="Input text file")
    parser.add_argument("--output", help="Output JSON report file")
    parser.add_argument("--auto-fix", action="store_true", help="Auto-fix and output corrected text")
    parser.add_argument("--neologism", action="store_true",
                        help="附加词典外高频字串提示（启发式、未校准、不计分；人工核对线索）")
    parser.add_argument("--bank", metavar="PATH",
                        help="v7.1.0: 项目自定义术语库（JSON 数组，格式同内置库：cn/en/aliases/source）；"
                             "与内置合并、同 cn 覆盖——学位论文自有缩写/机构名的统一走项目词表")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(2)  # 退出码契约 v5.8.0: 输入错误=2
    with open(args.input, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    terms_db = load_terminology(args.bank if getattr(args, "bank", None) else None)
    report = check_terms(text, terms_db)
    report.file = args.input

    if args.auto_fix and report.issues:
        fixed = auto_fix(text, report.issues)
        # Fixed text always goes to *_fixed.txt
        base = Path(args.input)
        fix_path = str(base.with_stem(base.stem + "_fixed"))
        with open(fix_path, "w", encoding="utf-8") as f:
            f.write(fixed)
        print(f"Auto-fixed {len(report.issues)} terms → {fix_path}")
    
    output_dict = asdict(report)

    neologisms = find_neologisms(text, terms_db) if args.neologism else []
    if args.neologism:
        output_dict["neologism_hints"] = neologisms
        output_dict["neologism_note"] = ("未校准启发式提示（不计分、不判定对错）——词典外高频字串，"
                                         "可能为新造词/生僻表述，请人工核对")

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_dict, f, ensure_ascii=False, indent=2)
        print(f"Report saved to {args.output}", file=sys.stderr)
    else:
        print(report.summary)
        if args.neologism:
            print("─" * 40)
            print("⚠️ 未校准启发式提示（不计分、不判定对错）——词典外高频字串，请人工核对：")
            if neologisms:
                for x in neologisms:
                    print(f"  · {x['term']}（出现 {x['count']} 次）")
            else:
                print("  （无）")
        print(NOTICE)


if __name__ == "__main__":
    import sys as _sys
    try:  # v3.5: 中文 Windows 默认 GBK 控制台会因 emoji/警示符崩溃 stdout——统一 UTF-8
        _sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        _sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    main()
