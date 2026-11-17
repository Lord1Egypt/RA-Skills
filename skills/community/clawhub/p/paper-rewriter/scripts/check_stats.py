# -*- coding: utf-8 -*-
"""check_stats.py — 统计一致性检查器（v3.2.0 实质功能，竞品零有）。

学术文稿里最伤信用的不是文风，是数字打架：同一分组前后 n 不一致、
百分比清单加起来不是 100、p 值大小写风格混用。本工具对文档做三类
确定性内部一致性检查（不联网、不做统计推断、不判定结果真伪）：

  1. 百分比清单求和——同句内 ≥2 个百分数且句含划分用语（分别/依次/
     构成比/respectively 等），合计偏离 100 超过容差（默认 0.3）→ 报告；
     无划分用语的清单不核（合并症占比等合法地不凑整）；
  2. 分组样本量自洽——「label（n=X）」形态的同一 label 前后出现不同 n
     → 报告（label 归一化：去空白/统一全半角括号）；
  3. 检验统计量风格混用——p= 与 P= / p< 与 P< 两种风格并存
     → 建议统一（期刊口径各异，只提示不判定）。

退出码契约与 check_terms.py 同表：0 一致 / 1 发现问题 / 2 用法错误。
口径声明：内部一致性启发式，不是统计审查，更不代表结果真实可靠。
"""
import argparse
import json
import os
import re
import sys
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hxt_core

# 1) 百分比清单：同句内收集（句=。！？；换行 边界；避免跨句误并）
_PCT_RX = re.compile(r"(\d{1,3}(?:[.,]\d+)?)\s*[%％]")


def _pct_to_float(raw):
    """「12,5%」→12.5（欧式小数）；「1,000%」→1000（千分位）。规则：逗号后
    恰三位数字=千分位去逗号，其余逗号作小数点。"""
    if "," in raw:
        head, _, tail = raw.rpartition(",")
        if len(tail) == 3 and head and head.replace(",", "").isdigit():
            return float(raw.replace(",", ""))
        return float(raw.replace(",", "."))
    return float(raw)
_SENT_SPLIT_RX = re.compile(r"[。！？;\n；]|(?<!\d)\.(?!\d)")
# 2) 分组 n：「label（n=42）」「label(n = 42)」「label n=42」
_GROUP_RX = re.compile(
    r"([\u4e00-\u9fffA-Za-z][\u4e00-\u9fffA-Za-z0-9_\-/]{0,24}?)\s*[（(]\s*n\s*[=＝]\s*(\d+)\s*[)）]"
    r"|([\u4e00-\u9fffA-Za-z][\u4e00-\u9fffA-Za-z0-9_\-/]{0,24}?)\s+n\s*[=＝]\s*(\d+)", re.I)
# 裸式分支的量词头停用词：「样本数 n=350」是总数不是分组——并入会制造假冲突
_BARE_LABEL_STOP = {"样本数", "例数", "人数", "总数", "总例数", "合计", "total", "overall"}
# 3) p 风格：独立词边界，P./p./P</p<（含统计学惯例的斜体差异不区分）
_P_STYLE_RX = re.compile(r"(?<![A-Za-z])([pP])\s*([<=≤＜＞]|＝|=)\s*0?\.\d+")


# label 前导修饰词：只剥汇总口径前缀（共计/全部/其中/总计类）。时点前缀
# （最终/随访末/入组时等）**不剥**——「干预组 n=45 随机化」vs「最终干预组
# n=42 完成试验」是合法的不同时点样本量（失访），并组会把每篇有脱落的
# RCT 都误报成数字打架（v3.2.0 评审实锤后收敛）。尾部修饰保留（「干预组
# 完成试验者」是另一分组）。
_LABEL_PREFIX_RX = re.compile(r"^(共计|全部|其中|总计)+")


def _norm_label(s):
    s = re.sub(r"\s+", "", s or "").replace("（", "(").replace("）", ")")
    return _LABEL_PREFIX_RX.sub("", s)


# 穷举清单线索词：出现即按「应合计 100%」口径核对（分别/依次/共/其余/构成比…）
_PARTITION_CUE_RX = re.compile(
    r"分别|依次|共计|共占|其余|构成比|占比为|比例分别|remainder|respectively|"
    r"account(?:ed)?\s+for|the\s+rest(?!\s+of\s+the\s+(?:world|country|region))")


def check_percent_sums(text, tolerance=0.3):
    """同句内 ≥2 个百分数的求和核对（v3.2.0 防误报双通道）。

    百分比清单未必互斥穷尽（合并症/多选题占比合法地不等于 100，近失凑整
    窗口也区分不了两者）——**只在句含划分用语时核对**：分别/依次/共计/
    其余/构成比/respectively 等。无划分用语的清单（如合并症占比
    58.2%+40.5%=98.7%）一律不报——宁可少报，不误报合法清单。"""
    results = []
    for sent in _SENT_SPLIT_RX.split(text):
        pcts = [_pct_to_float(m.group(1)) for m in _PCT_RX.finditer(sent)]
        if len(pcts) < 2:
            continue
        if not _PARTITION_CUE_RX.search(sent):
            continue
        total = sum(pcts)
        if abs(total - 100.0) <= tolerance:
            continue
        results.append({
            "kind": "percent_sum",
            "detail": "百分比清单合计 %.1f%%（句含划分用语，应为 100%%±%.1f）" % (
                total, tolerance),
            "parts": pcts, "tolerance": tolerance,
            "context": sent.strip()[:120],
        })
    return results


def check_group_ns(text, source=""):
    """同一分组 label 前后出现不同 n → 报告。

    source 非空时（--batch 跨文件模式）每处命中带来源，冲突可标注
    「跨文件」——摘要/方法/结果分章写作时同一分组 n 前后打架是审稿
    现场最常见的硬伤，单文件模式看不见。"""
    seen = {}
    order = []
    for m in _GROUP_RX.finditer(text):
        raw_label = m.group(1) if m.group(1) else m.group(3)
        if raw_label and raw_label.lower() in _BARE_LABEL_STOP:
            continue
        label = _norm_label(raw_label)
        n = int(m.group(2) if m.group(2) else m.group(4))
        if len(label) < 2:
            continue  # 单字标签误配率高（如「共 n=」），宁少报
        if label not in seen:
            seen[label] = []
            order.append(label)
        seen[label].append((n, source) if source else n)
    results = []
    for label in order:
        vals = seen[label]
        plain = [v[0] if isinstance(v, tuple) else v for v in vals]
        uniq = sorted(set(plain))
        if len(uniq) < 2:
            continue
        cross = any(isinstance(v, tuple) for v in vals)
        if cross:
            span = sorted({s2 for v in vals if isinstance(v, tuple) for s2 in v[1:]})
            detail = "分组「%s」跨文件样本量不一致：%s（出现在 %s）" % (
                label, " vs ".join("n=%d" % x for x in uniq[:6]),
                "、".join(span[:5]))
        else:
            detail = "分组「%s」出现多个样本量：%s" % (
                label, " vs ".join("n=%d" % x for x in plain[:6]))
        results.append({
            "kind": "group_n_conflict",
            "detail": detail,
            "label": label, "values": plain[:8],
            "cross_file": cross,
        })
    return results


def check_p_style(text):
    """p=/P= 两种风格并存 → 建议统一（不判定谁对——期刊口径各异）。"""
    lower = upper = lt_lower = lt_upper = 0
    for m in _P_STYLE_RX.finditer(text):
        style, op = m.group(1), m.group(2)
        if op in ("=", "＝"):  # =/＝ 计等式风格；</<=/≤/＜/＞ 计小于风格
            if style == "p":
                lower += 1
            else:
                upper += 1
        else:
            if style == "p":
                lt_lower += 1
            else:
                lt_upper += 1
    eq_mix = min(lower, upper) > 0
    lt_mix = min(lt_lower, lt_upper) > 0
    if not (eq_mix or lt_mix):
        return None
    forms = []
    if lower:
        forms.append("p=%d 处" % lower)
    if upper:
        forms.append("P=%d 处" % upper)
    if lt_lower:
        forms.append("p<%d 处" % lt_lower)
    if lt_upper:
        forms.append("P<%d 处" % lt_upper)
    return {
        "kind": "p_style_mix",
        "detail": "检验统计量大小写风格混用（%s）——同刊应统一（斜体规范以目标期刊稿约为准）"
                  % "、".join(forms),
        "counts": {"p_eq": lower, "P_eq": upper, "p_lt": lt_lower, "P_lt": lt_upper},
    }


# 跨文件模式的加宽前缀表：时点修饰（入组/最终等）在分章写作里常造成
# 同组不同写法；单文件保持保守不剥（防失访误报），跨文件放宽+显式免责
_LABEL_PREFIX_WIDE_RX = re.compile(
    r"^(共计|全部|其中|总计|最终|结束时|随访末|末次|入组时|入组|基线时|治疗后|"
    r"纳入|入选|招募|共纳入|共入组|本研究)+")
_CROSS_CAVEAT = "（跨文件聚合会把不同时点的样本量也并组比对——若为随机化 vs 完成随访等时点差异请忽略）"


def run_batch(paths, tolerance=0.3):
    """跨文件批量（v3.3.0）：逐文件三类检查 + 跨文件 group_n 聚合。

    跨文件聚合的意义：分章写作（摘要/方法/结果各一稿）时，同一分组
    「摘要 n=120、结果 n=118」的打架单文件检查看不见——合并聚合才抓得住。"""
    per_file = {}
    texts = []
    for p in paths:
        text = load_text(p)
        name = os.path.basename(p)
        groups, issues = run_checks(text, tolerance=tolerance)
        per_file[name] = {"issues": issues, "groups": groups}
        texts.append((name, text))
    agg = {}
    order = []
    merged = set()  # 剥离过时点/汇总前缀的 label（v3.3.0 评审：并组是候选而非定罪）
    for name, text in texts:
        for m in _GROUP_RX.finditer(text):
            raw_label = m.group(1) if m.group(1) else m.group(3)
            if raw_label and raw_label.lower() in _BARE_LABEL_STOP:
                continue
            normed = _norm_label(raw_label)
            label = _LABEL_PREFIX_WIDE_RX.sub("", normed)
            n = int(m.group(2) if m.group(2) else m.group(4))
            if len(label) < 2:
                continue
            if label != normed:
                merged.add(label)
            if label not in agg:
                agg[label] = []
                order.append(label)
            agg[label].append((n, name))
    cross = []
    for label in order:
        vals = agg[label]
        plain = [v[0] for v in vals]
        uniq = sorted(set(plain))
        if len(uniq) < 2:
            continue
        span = sorted({s2 for _, s2 in vals})
        tp = label in merged
        if tp:
            detail = ("分组「%s」跨文件样本量不同，可能为时点口径差异（随机化 vs 完成随访等）"
                      "——如确属同组同口径请核对原始数据（出现在 %s）" % (
                          label, "、".join(span[:5])))
        else:
            detail = "分组「%s」跨文件样本量不一致：%s（出现在 %s）" % (
                label, " vs ".join("n=%d" % x for x in uniq[:6]),
                "、".join(span[:5]))
        cross.append({
            "kind": "group_n_conflict", "cross_file": True,
            "timepoint_merged": tp,
            "detail": detail,
            "label": label, "values": plain[:8],
        })
    return per_file, cross


def run_checks(text, tolerance=0.3):
    out = {
        "percent_sum": check_percent_sums(text, tolerance=tolerance),
        "group_n_conflict": check_group_ns(text),
        "p_style_mix": [x for x in [check_p_style(text)] if x],
    }
    issues = out["percent_sum"] + out["group_n_conflict"] + out["p_style_mix"]
    return out, issues


def load_text(path):
    try:
        return hxt_core.read_text(path)
    except (OSError, ValueError) as e:
        print("错误: %s" % e, file=sys.stderr)
        sys.exit(2)


def build_report(groups, issues, source=""):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = ["# 统计一致性检查：%s" % (source or "未命名文稿"), "",
             "> 自动生成（%s）。内部一致性启发式口径——不是统计审查，" % now,
             "> 不判定结果真伪；改动数字前以原始数据为准。", ""]
    if not issues:
        lines.append("未发现统计一致性问题。")
        return "\n".join(lines)
    lines.append("发现 %d 项统计一致性问题：" % len(issues))
    lines.append("")
    lines.append("| 类别 | 详情 |")
    lines.append("| --- | --- |")
    for x in issues:
        lines.append("| %s | %s |" % (x["kind"], x["detail"].replace("|", "\\|")))
    lines.append("")
    if groups["percent_sum"]:
        lines.append("百分比明细：")
        lines.append("")
        for x in groups["percent_sum"]:
            lines.append("- %s → 各项 %s，合计 %.1f" % (
                x["context"], " + ".join(str(p) for p in x["parts"]),
                sum(x["parts"])))
        lines.append("")
    lines.append("> 审稿人对数字打架的容忍度远低于文风问题：修一致性，先于修文风"
                 "（以原始数据为准）。")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="统计一致性检查器（内部一致性启发式）")
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + hxt_core.__version__)
    ap.add_argument("file", nargs="?", help="待检文档（.txt/.md/.docx）")
    ap.add_argument("--batch", help="批量模式：检查目录下全部 .txt/.md/.docx，"
                                     "并做跨文件分组 n 聚合（摘要/方法/结果分稿的数字打架）")
    ap.add_argument("--tolerance", type=float, default=0.3,
                    help="百分比合计容差（默认 0.3 个百分点）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--report", help="生成 markdown 一致性报告")
    args = ap.parse_args()

    if args.batch:
        import glob as _glob
        paths = sorted(
            fp for fp in _glob.glob(os.path.join(args.batch, "*"))
            if fp.lower().endswith((".txt", ".md", ".docx")))
        if not paths:
            ap.error("目录下无可检文件（.txt/.md/.docx）：%s" % args.batch)
        per_file, cross = run_batch(paths, tolerance=args.tolerance)
        hard = [x for x in cross if not x.get("timepoint_merged")]
        cand = [x for x in cross if x.get("timepoint_merged")]
        n_issues = sum(len(v["issues"]) for v in per_file.values()) + len(hard)
        if args.report:
            print("[提示] --batch 暂不支持 --report（单文件模式可用）", file=sys.stderr)
        if args.json:
            print(json.dumps({"files": per_file, "cross_file": cross,
                              "total": n_issues,
                              "disclaimer": "内部一致性启发式，非统计审查，不代表结果真伪"},
                             ensure_ascii=False, indent=2))
            sys.exit(0)
        print("批量检查 %d 个文件：" % len(paths))
        for name, v in per_file.items():
            print("  %s：%d 项" % (name, len(v["issues"])))
            for x in v["issues"]:
                print("    [%s] %s" % (x["kind"], x["detail"]))
        if hard:
            print("跨文件聚合：%d 项" % len(hard))
            for x in hard:
                print("  [%s] %s" % (x["kind"], x["detail"]))
        if cand:
            print("跨文件时点候选（不计入退出码——时点差异属合法，请人工判断）：")
            for x in cand:
                print("  [%s] %s" % (x["kind"], x["detail"]))
        print("（内部一致性提示，非统计审查——先核对原始数据是笔误还是口径差异，再改表述）")
        sys.exit(1 if n_issues else 0)

    if not args.file:
        ap.error("缺少待检文档")

    text = load_text(args.file)
    groups, issues = run_checks(text, tolerance=args.tolerance)

    if args.json:
        print(json.dumps({"issues": issues, "total": len(issues),
                          "groups": groups,
                          "disclaimer": "内部一致性启发式，非统计审查，不代表结果真伪"},
                         ensure_ascii=False, indent=2))
        sys.exit(0)

    if args.report:
        md = build_report(groups, issues, source=args.file)
        try:
            with open(args.report, "w", encoding="utf-8") as rf:
                rf.write(md + "\n")
            print("报告已写入 %s" % args.report, file=sys.stderr)
        except OSError as e:
            print("错误: 无法写入报告（%s）" % e, file=sys.stderr)

    if not issues:
        print("未发现统计一致性问题。")
        sys.exit(0)

    print("发现 %d 项统计一致性问题：" % len(issues))
    for x in issues:
        print("  [%s] %s" % (x["kind"], x["detail"]))
    print("（内部一致性提示，非统计审查——先核对原始数据是笔误还是口径差异，再改表述）")
    sys.exit(1)


if __name__ == "__main__":
    hxt_core.cli_entry(main)
