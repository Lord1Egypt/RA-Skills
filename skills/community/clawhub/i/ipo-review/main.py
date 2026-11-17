from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _base_dir() -> Path:
    # 打包成 exe 后，以 exe 所在目录为基准查找 input/config/output；
    # 普通 python 运行时仍以当前目录为基准。
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(".")

from src.arithmetic_checker import check_arithmetic
from src.config_loader import load_config
from src.cutoff_consistency_checker import check_cutoff_date_consistency
from src.document_parser import parse_documents, write_unparsed_csv
from src.fact_extractor import extract_financial_facts
from src.financial_comparator import LAST_COMPARE_STATS, compare_financial_facts
from src.html_reporter import write_outputs
from src.inventory import build_inventory
from src.text_table_consistency_checker import check_text_table_consistency


def main() -> int:
    base = _base_dir()
    parser = argparse.ArgumentParser(description="本地IPO问询回复复核工具")
    parser.add_argument("--input", default=str(base / "input"), help="输入文件目录")
    parser.add_argument("--output", default=str(base / "output"), help="输出目录")
    parser.add_argument("--config", default=str(base / "config"), help="配置目录")
    args = parser.parse_args()

    log: list[str] = []
    config = load_config(args.config)
    log.append("配置加载完成。")

    docs = build_inventory(args.input, config["roles"])
    log.append(f"识别到 {len(docs)} 个输入文件。")

    evidence, unparsed = parse_documents(docs)
    log.append(f"生成 {len(evidence)} 条证据记录，解析失败/未解析项目 {len(unparsed)} 条。")

    facts = extract_financial_facts(evidence, config["metrics"])
    log.append(f"抽取 {len(facts)} 条财务事实。")

    issues = []
    comparison_exclusions = []
    arithmetic_skips = []
    financial_issues, financial_exclusions = compare_financial_facts(facts, config["tolerance"])
    issues.extend(financial_issues)
    comparison_exclusions.extend(financial_exclusions)
    arithmetic_issues, arithmetic_skip_rows = check_arithmetic(evidence, config["tolerance"])
    issues.extend(arithmetic_issues)
    arithmetic_skips.extend(arithmetic_skip_rows)
    issues.extend(check_cutoff_date_consistency(evidence, facts))
    issues.extend(check_text_table_consistency(evidence, facts))
    from src.typo_format_checker import check_format
    issues.extend(check_format(evidence))
    issues = _dedupe_and_number(issues)
    _assign_review_priority(issues)
    issues = _sort_and_number(issues)
    log.append(f"形成 {len(issues)} 条异常/提示事项。")
    log.extend(_quality_stats(facts, issues, comparison_exclusions, arithmetic_skips))

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    write_unparsed_csv(out / "unparsed_items.csv", unparsed)
    _write_csv(out / "parse_errors.csv", [{"file": r.get("file", ""), "position": r.get("page", ""), "error_type": "parse_failed", "reason": r.get("reason", "")} for r in unparsed])
    _write_csv(out / "comparison_exclusions.csv", comparison_exclusions)
    caliber_notes = _caliber_notes(comparison_exclusions)
    _write_csv(out / "caliber_notes.csv", caliber_notes)
    _write_csv(out / "arithmetic_skips.csv", arithmetic_skips)
    write_outputs(out, docs, evidence, facts, issues, log, {
        "parse_errors.csv": len(unparsed),
        "comparison_exclusions.csv": len(comparison_exclusions),
        "caliber_notes.csv": len(caliber_notes),
        "arithmetic_skips.csv": len(arithmetic_skips),
        "确认一致事项": LAST_COMPARE_STATS.get("CONFIRMED_CONSISTENT", 0),
        "正常舍入事项": LAST_COMPARE_STATS.get("NORMAL_ROUNDING", 0),
        "噪声参考": sum(1 for i in issues if i.review_priority == "noise"),
    })
    log.append("输出写入完成。")
    (out / "run_log.txt").write_text("\n".join(log), encoding="utf-8")
    report = out / "IPO问询回复复核分析报告.html"
    if getattr(sys, "frozen", False):
        key_count = sum(1 for i in issues if getattr(i, "review_priority", "") == "key")
        print("\n========================================")
        print(f"复核完成！共 {len(issues)} 条事项，其中待人工复核（重点）{key_count} 条。")
        print(f"报告位置：{report}")
        print("========================================\n")
        try:
            import os
            os.startfile(str(report))
        except Exception:
            pass
        input("已自动打开报告。按回车键关闭本窗口...")
    return 0


def _dedupe_and_number(issues):
    seen = set()
    out = []
    for issue in issues:
        if issue.category == "数学勾稽错误":
            key = (issue.level, issue.category, issue.source_1, issue.source_2, issue.conclusion)
        else:
            key = (
                issue.level,
                issue.category,
                issue.item,
                tuple(issue.evidence_ids),
                issue.conclusion,
            )
        if key in seen:
            continue
        seen.add(key)
        issue.issue_id = f"ISS{len(out)+1:05d}"
        out.append(issue)
    return out


def _assign_review_priority(issues):
    """区分“重点待人工复核”、“一般”和“噪声/参考”，让人能快速聚焦真正要看的内容。

    key   = 经过严格口径/层级/量级校验后值得人工确认的实质线索；
    noise = 已被量级或敏感性护栏降级、或低价值的重复提示；
    normal= 其余需要留意但非首要的事项。
    """
    for issue in issues:
        issue.review_priority = _priority_of(issue)
        issue.count_in_exception_total = issue.status in {"HIGH_CONFIDENCE_CONFLICT", "LOW_CONFIDENCE_CONFLICT"}
        issue.display_default = issue.review_priority == "key"
        issue.noise_reason = ""
        if issue.category in {"表文数据不一致", "截止日口径不一致"}:
            issue.review_priority = "key"
            issue.count_in_exception_total = True
            issue.display_default = True
        if issue.review_priority == "noise":
            issue.count_in_exception_total = False
            issue.display_default = False
            issue.noise_reason = _noise_reason(issue)
        if issue.category in {"期间表述提示"}:
            issue.count_in_exception_total = False
            issue.display_default = False
        if issue.category == "候选跨文件差异":
            issue.count_in_exception_total = False


def _sort_and_number(issues):
    priority_order = {"key": 0, "normal": 1, "noise": 2}
    category_order = {
        "表文数据不一致": 0,
        "截止日口径不一致": 1,
        "跨文件财务数据差异": 2,
        "数学勾稽错误": 3,
        "候选跨文件差异": 4,
        "格式及文字问题": 5,
        "期间表述提示": 6,
    }
    ordered = sorted(
        issues,
        key=lambda i: (
            priority_order.get(getattr(i, "review_priority", "normal"), 1),
            category_order.get(i.category, 99),
            i.issue_id,
        ),
    )
    for idx, issue in enumerate(ordered, 1):
        issue.issue_id = f"ISS{idx:05d}"
    return ordered


def _priority_of(issue):
    cat = issue.category
    if cat in {"表文数据不一致", "截止日口径不一致"}:
        return "key"
    if cat == "口径不同提示":
        return "noise"
    if cat == "跨文件财务数据差异":
        # 严格比较通过（单位/期间/指标/层级/量级均一致），是重点。
        return "key"
    if cat == "候选跨文件差异":
        # 被量级或敏感性护栏降级的候选属于噪声；其余为接近同口径的真实差异，列为重点。
        if "降级原因" in (issue.suggestion or ""):
            return "noise"
        # 金额类指标的百分比是“占比”，其分母口径高度依赖上下文（占收入/占资产/占某客户），
        # 无法机械判定同口径，列为参考而非重点；“率”类指标（毛利率等）保留为重点。
        if issue.item.endswith("|percent") and not any(k in issue.item for k in ("率", "占比")):
            return "noise"
        return "key"
    if cat == "数学勾稽错误":
        # 小幅偏离更可能是真实漏记/端数差错，列为重点；中等偏离作为一般。
        ratio = issue.diff_ratio if issue.diff_ratio is not None else 1.0
        return "key" if ratio <= 0.05 else "normal"
    if cat == "期间表述提示":
        return "noise"
    return "normal"


def _noise_reason(issue):
    text = " ".join([issue.suggestion or "", issue.caliber_analysis or "", issue.source_1_text or "", issue.source_2_text or ""])
    for kw, reason in [
        ("市盈率", "valuation_multiple"),
        ("融资规模", "financing_amount"),
        ("募集资金", "financing_amount"),
        ("销售额", "sales_amount_not_margin"),
        ("对毛利率的影响", "gross_margin_impact"),
        ("毛利率差异率", "gross_margin_impact"),
        ("敏感性", "sensitivity_or_assumption"),
        ("测算", "sensitivity_or_assumption"),
        ("差异比率", "suspect_caliber_or_scale"),
    ]:
        if kw in text:
            return reason
    return "low_value_reference"


def _quality_stats(facts, issues, comparison_exclusions, arithmetic_skips):
    from collections import Counter
    unit_stats = Counter((f.raw_unit, f.unit_source) for f in facts)
    scope_stats = Counter(f.scope for f in facts)
    status_stats = Counter(i.status for i in issues)
    strict_count = sum(1 for f in facts if f.is_strictly_comparable)
    official = sum(1 for i in issues if getattr(i, "count_in_exception_total", True))
    candidates = sum(1 for i in issues if i.status in {"CALIBER_DIFFERENCE", "MANUAL_REVIEW_CANDIDATE", "PERIOD_VAGUE"})
    financial = sum(1 for i in issues if i.category in {"跨文件财务数据差异", "候选跨文件差异"})
    key_count = sum(1 for i in issues if i.review_priority == "key")
    noise_count = sum(1 for i in issues if i.review_priority == "noise")
    lines = [
        f"单位识别统计：{dict(unit_stats.most_common(20))}",
        f"scope统计：{dict(scope_stats.most_common(20))}",
        f"is_strictly_comparable=True数量：{strict_count}",
        f"问题状态统计：{dict(status_stats)}",
        f"跨文件财务差异数量：{financial}",
        f"正式异常数量：{official}",
        f"候选事项数量：{candidates}",
        f"待人工复核（重点）数量：{key_count}",
        f"噪声/参考数量：{noise_count}",
        f"comparison_exclusions数量：{len(comparison_exclusions)}",
        f"arithmetic_skips数量：{len(arithmetic_skips)}",
        f"确认一致事项数量：{LAST_COMPARE_STATS.get('CONFIRMED_CONSISTENT', 0)}",
        f"正常舍入事项数量：{LAST_COMPARE_STATS.get('NORMAL_ROUNDING', 0)}",
    ]
    return lines


def _caliber_notes(comparison_exclusions):
    business_reasons = {
        "metric_caliber_modifier_mismatch": ("调整/剔除影响口径不同，不应与普通实际指标直接比较", "核对披露是否已说明调整口径；如需对比，应明确列示调整项。"),
        "forecast_or_assumption_metric": ("假定增长、预测、测算或敏感性口径，不代表实际历史财务数据", "避免与实际数混用；如披露预测口径，应单独说明假设基础。"),
        "special_caliber_lower_higher": ("孰低/孰高等特殊计算口径，与单一原始指标不同", "补充说明计算口径，避免读者误认为实际净利润。"),
        "derived_metric_context": ("衍生指标或测算口径，不适合作为原始财务指标比较", "保留为测算说明，不纳入一致性差异判断。"),
    }
    rows = []
    for row in comparison_exclusions:
        reason = row.get("exclusion_reason", "")
        if reason not in business_reasons:
            continue
        explanation, suggestion = business_reasons[reason]
        rows.append({
            "file": row.get("file", ""),
            "position": row.get("position", ""),
            "metric": row.get("metric", ""),
            "period": row.get("period", ""),
            "value": row.get("value", ""),
            "exclusion_reason": reason,
            "business_explanation": explanation,
            "suggestion": suggestion,
        })
    return rows


def _write_csv(path: Path, rows: list[dict]) -> None:
    import csv
    keys = sorted({k for row in rows for k in row}) if rows else ["empty"]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    try:
        _code = main()
    except Exception:  # noqa: BLE001
        if getattr(sys, "frozen", False):
            import traceback
            traceback.print_exc()
            print("\n运行出错。请确认 input 文件夹中放入了待复核文件，且 config 文件夹存在。")
            input("按回车键关闭本窗口...")
            _code = 1
        else:
            raise
    raise SystemExit(_code)
