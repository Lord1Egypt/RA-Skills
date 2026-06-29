#!/usr/bin/env python3
"""
Pipeline Schema & Validation
=============================

集中定义管道各阶段的 paper 字段合同，提供入口/出口校验 + 问题报告。
校验失败不阻断管道（不 exit），写入 pipeline_issues.json 供 AI 决策。

用法：
    from pipeline_schema import validate, report, stamp, PIPELINE_VERSION

    # 出口校验
    ok, issues = validate(papers, stage="merged")
    if issues:
        report(issues, stage="merged")
        print(f"[validate] {len(ok)}/{len(papers)} OK, {len(issues)} issues → pipeline_issues.json")

    # 输出前盖版本章
    stamp(output_dict, stage="merged")

版本策略：
    _pipeline_version 升版规则 — 字段增删/改名/类型变更 → +1。
    旧脚本读到高版本 → 报 version_mismatch，不静默运行。
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

PIPELINE_VERSION = 1

# ═══════════════════════════════════════════════════════════════════════════
# 阶段字段合同
# ═══════════════════════════════════════════════════════════════════════════

REQUIRED_FIELDS: dict[str, list[str]] = {
    # --- 搜索阶段（提取器产出） ---
    "search": [
        "title",
        "link",
    ],

    # --- 合并阶段（merge_results.py 产出） ---
    "merged": [
        "title",
        "_source_db",
    ],

    # --- 摘要补全阶段（enrich_abstracts.py 产出） ---
    "enriched": [
        "title",
        "_source_db",
        "_abstract_file",      # 可能为空字符串表示无摘要，但字段必须存在
    ],

    # --- 评分阶段（paper_ranker.py 产出） ---
    "ranked": [
        "title",
        "_scores",             # {relevance, impact, recency, accessibility}
    ],

    # --- AI 重排阶段（ai_rerank.py 产出） ---
    "ai_ranked": [
        "title",
        "_ai_scores",          # {relevance, quality, novelty, reason}
    ],

    # --- AI 综述阶段（ai_summarize.py 产出） ---
    "summarized": [
        "title",
        "_cn_summary",         # 200-300 字中文简述
    ],

    # --- 主题聚类阶段（theme_cluster.py 产出） ---
    "themed": [
        "title",
        "_theme",              # 主题分类标签
    ],
}

# 各阶段的「应该有但缺失不致命」的字段 → severity=warning
NICE_TO_HAVE: dict[str, list[str]] = {
    "search":   ["doi", "authors", "year"],
    "merged":   ["doi", "link", "year", "authors"],
    "enriched": ["doi", "year", "authors", "venue"],
    "ranked":   ["doi", "_abstract_file"],
    "ai_ranked":["doi", "_abstract_file", "_cn_summary"],
    "summarized":["doi", "_ai_scores"],
    "themed":  ["doi", "_cn_summary", "_ai_scores"],
}

# ═══════════════════════════════════════════════════════════════════════════
# 校验
# ═══════════════════════════════════════════════════════════════════════════

def validate(papers: list[dict], stage: str) -> tuple[list[dict], list[dict]]:
    """
    校验一批论文是否满足指定阶段的要求。

    参数：
        papers:  论文 dict 列表
        stage:   阶段名（"search" / "merged" / ... / "themed"）

    返回：
        (ok_papers, issues)
        - ok_papers: 合规的论文列表（带 _schema_error 标记的已被移到这里）
        - issues: 问题描述列表，每条含 paper_index / severity / problem / detail / suggestion
    """
    if stage not in REQUIRED_FIELDS:
        return papers, [{
            "stage": stage,
            "severity": "error",
            "problem": "unknown_stage",
            "detail": f"Stage '{stage}' not defined in REQUIRED_FIELDS. "
                       f"Valid stages: {', '.join(sorted(REQUIRED_FIELDS))}",
            "suggestion": "Check pipeline_schema.py REQUIRED_FIELDS",
        }]

    required = REQUIRED_FIELDS[stage]
    nice = NICE_TO_HAVE.get(stage, [])
    ok_papers = []
    issues = []

    for i, paper in enumerate(papers):
        paper_ok = True

        # 检查必填字段
        for field in required:
            value = paper.get(field)
            # None / 空字符串 / 不存在 → 缺
            if value is None or (isinstance(value, str) and value.strip() == ""):
                paper_ok = False
                issues.append({
                    "paper_index": i,
                    "paper_title": _short_title(paper),
                    "severity": "error",
                    "problem": "missing_required_field",
                    "detail": f"Field '{field}' is missing or empty",
                    "suggestion": f"Check upstream script that should produce '{field}' for stage '{stage}'",
                })

        # 检查建议字段
        for field in nice:
            value = paper.get(field)
            if value is None or (isinstance(value, str) and value.strip() == ""):
                issues.append({
                    "paper_index": i,
                    "paper_title": _short_title(paper),
                    "severity": "warning",
                    "problem": "missing_nice_to_have",
                    "detail": f"Field '{field}' is missing (non-critical)",
                    "suggestion": f"Consider enriching from another source if needed later",
                })

        if paper_ok:
            ok_papers.append(paper)
        else:
            # 标记但保留，让 AI 决定如何处理
            paper["_schema_error"] = True
            ok_papers.append(paper)  # 仍然放进 ok，不丢弃

    return ok_papers, issues


# ═══════════════════════════════════════════════════════════════════════════
# 问题报告
# ═══════════════════════════════════════════════════════════════════════════

REPORT_PATH = "memory/pipeline_issues.json"


def report(issues: list[dict], stage: str, output_path: str | None = None):
    """
    将校验问题追加写入 pipeline_issues.json。

    如果文件已存在，追加到 issues 列表；否则新建。
    每条问题自动附加时间戳和阶段标记。
    """
    if not issues:
        return

    path = output_path or REPORT_PATH
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    # 加载已有报告
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                report_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            report_data = {"_pipeline_version": PIPELINE_VERSION, "issues": []}
    else:
        report_data = {"_pipeline_version": PIPELINE_VERSION, "issues": []}

    # 更新版本号
    report_data["_pipeline_version"] = PIPELINE_VERSION

    # 附加时间戳和阶段标记
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    existing = report_data.setdefault("issues", [])

    for issue in issues:
        issue["timestamp"] = timestamp
        issue["stage"] = stage
        existing.append(issue)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    # 打印一句话摘要
    errors = sum(1 for i in issues if i.get("severity") == "error")
    warnings = sum(1 for i in issues if i.get("severity") == "warning")
    parts = []
    if errors:
        parts.append(f"{errors} error(s)")
    if warnings:
        parts.append(f"{warnings} warning(s)")
    print(f"[validate:{stage}] {', '.join(parts)} → {path}", file=sys.stderr)


# ═══════════════════════════════════════════════════════════════════════════
# 版本章
# ═══════════════════════════════════════════════════════════════════════════

def stamp(data: dict, stage: str) -> dict:
    """
    给输出 JSON 的顶层添加版本标记和阶段标记。
    原地修改并返回。
    """
    data["_pipeline_version"] = PIPELINE_VERSION
    data["_pipeline_stage"] = stage
    return data


def check_version(data: dict, stage: str) -> list[dict]:
    """
    检查输入 JSON 的版本是否兼容。
    返回 issues 列表（空 = 兼容）。
    """
    issues = []
    version = data.get("_pipeline_version")
    if version is not None and version > PIPELINE_VERSION:
        issues.append({
            "severity": "error",
            "problem": "version_mismatch",
            "detail": (f"Input has _pipeline_version={version}, "
                       f"but this script expects ≤{PIPELINE_VERSION}. "
                       f"Results may be invalid."),
            "suggestion": "Re-run the pipeline from the stage that produced this file, "
                          "or update pipeline_schema.py PIPELINE_VERSION.",
        })
    return issues


# ═══════════════════════════════════════════════════════════════════════════
# 辅助
# ═══════════════════════════════════════════════════════════════════════════

def _short_title(paper: dict, max_len: int = 80) -> str:
    """论文标题截断，用于问题报告的可读性。"""
    title = paper.get("title", "") or "(no title)"
    if len(title) > max_len:
        return title[:max_len - 3] + "..."
    return title


# ═══════════════════════════════════════════════════════════════════════════
# CLI（方便单独检查某个中间文件）
# ═══════════════════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Validate a pipeline intermediate JSON against its stage schema"
    )
    parser.add_argument("file", help="JSON file to validate")
    parser.add_argument("--stage", "-s", required=True,
                        choices=list(REQUIRED_FIELDS.keys()),
                        help="Pipeline stage to validate against")
    parser.add_argument("--output", "-o", default=None,
                        help="Custom issues output path (default: memory/pipeline_issues.json)")
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 解包
    if isinstance(data, dict) and "papers" in data:
        papers = data["papers"]
    elif isinstance(data, list):
        papers = data
    else:
        print(f"Error: unrecognized format — expected dict with 'papers' or list", file=sys.stderr)
        sys.exit(1)

    # 版本检查
    version_issues = check_version(data if isinstance(data, dict) else {}, args.stage)

    # 字段校验
    ok, field_issues = validate(papers, args.stage)

    all_issues = version_issues + field_issues

    if all_issues:
        report(all_issues, args.stage, args.output)
        errors = sum(1 for i in all_issues if i.get("severity") == "error")
        warnings = sum(1 for i in all_issues if i.get("severity") == "warning")
        print(f"{args.file}: {len(ok)}/{len(papers)} papers OK "
              f"({errors} errors, {warnings} warnings)")
    else:
        print(f"{args.file}: {len(ok)}/{len(papers)} papers OK — no issues")


if __name__ == "__main__":
    main()
