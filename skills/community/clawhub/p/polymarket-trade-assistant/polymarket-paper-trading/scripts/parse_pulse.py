#!/usr/bin/env python3
"""
Parse a Polymarket market-pulse report and extract structured recommendations.

Usage:
    python parse_pulse.py <pulse_report.md>
    python parse_pulse.py ~/polymarket-reports/market-pulse-2026-02-24-040000.md

Output: JSON array of recommendations to stdout.
"""

import json
import re
import sys
from pathlib import Path


def parse_report(text: str) -> list[dict]:
    market_pattern = re.compile(
        r"^##\s+(\d+)\.\s+(.+?)$", re.MULTILINE
    )
    splits = list(market_pattern.finditer(text))
    if not splits:
        print("[WARN] No market sections found in report", file=sys.stderr)
        return []

    recommendations = []
    for i, match in enumerate(splits):
        start = match.start()
        end = splits[i + 1].start() if i + 1 < len(splits) else len(text)
        section = text[start:end]
        rank = int(match.group(1))
        question = match.group(2).strip()

        rec = parse_section(section, rank, question)
        if rec:
            recommendations.append(rec)

    return recommendations


def parse_section(section: str, rank: int, question: str) -> dict | None:
    rec: dict = {
        "rank": rank,
        "question": question,
        "url": "",
        "event_slug": "",
        "market_price": None,
        "spread": None,
        "direction": "",
        "recommended_price": None,
        "size_range": "",
        "max_executable": None,
        "edge": None,
        "edge_side": "",
        "confidence": "",
        "liquidity_tier": "",
        "order_strategy": "",
        "end_date": None,
    }

    link_m = re.search(r"\*\*链接[：:]\*\*\s*(https?://\S+)", section)
    if link_m:
        rec["url"] = link_m.group(1).strip()
        slug_m = re.search(r"polymarket\.com/event/([^\s/]+)", rec["url"])
        if slug_m:
            rec["event_slug"] = slug_m.group(1)

    prob_m = re.search(
        r"\*\*当前隐含概率[：:]\*\*\s*(\w+)\s*@\s*([\d.]+)%\s*\|\s*价差[：:]\s*([\d.]+)",
        section,
    )
    if prob_m:
        rec["market_price"] = float(prob_m.group(2)) / 100
        rec["spread"] = float(prob_m.group(3))

    conf_m = re.search(r"\*\*置信度[：:]\*\*\s*(.+?)$", section, re.MULTILINE)
    if conf_m:
        rec["confidence"] = conf_m.group(1).strip()

    edge_rows = re.findall(
        r"\|\|?\s*(\w+(?:\s*\([^)]*\))?)\s*\|\s*([\d.]+)%\s*\|\s*([\d.]+)%\s*\|\s*([+-]?[\d.]+%?\s*(?:edge\s+on\s+\w+)?)\s*\|",
        section,
    )
    best_edge = 0
    best_edge_side = ""
    for row in edge_rows:
        outcome_label = row[0].strip()
        edge_str = row[3].strip()
        edge_num_m = re.search(r"([+-]?[\d.]+)", edge_str)
        if edge_num_m:
            edge_val = float(edge_num_m.group(1))
            side_m = re.search(r"edge\s+on\s+(\w+)", edge_str)
            if side_m and edge_val > best_edge:
                best_edge = edge_val
                best_edge_side = side_m.group(1)
            elif edge_val > best_edge:
                best_edge = edge_val
                best_edge_side = outcome_label

    if best_edge > 0:
        rec["edge"] = best_edge / 100
        rec["edge_side"] = best_edge_side

    pos_section = re.search(
        r"###\s*仓位建议(.*?)(?=###|\Z)", section, re.DOTALL
    )
    if pos_section:
        pos_text = pos_section.group(1)

        dir_m = re.search(r"方向\s*\|\s*买入\s*(\w+)\s*@\s*(?:限价\s*)?[$]?([\d.]+)", pos_text)
        if dir_m:
            rec["direction"] = dir_m.group(1)
            rec["recommended_price"] = float(dir_m.group(2))

        size_m = re.search(r"规模\s*\|\s*(.+?)(?:\s*\||\s*$)", pos_text, re.MULTILINE)
        if size_m:
            raw = size_m.group(1).strip()
            tier_m = re.search(r"流动性等级[：:]\s*(\w+)", raw)
            if tier_m:
                rec["liquidity_tier"] = tier_m.group(1)
            range_m = re.match(r"([$\d,.\-<>]+)", raw)
            rec["size_range"] = range_m.group(1).strip() if range_m else raw

        max_m = re.search(r"最大可执行\s*\|\s*\$?([\d,]+)", pos_text)
        if max_m:
            rec["max_executable"] = float(max_m.group(1).replace(",", ""))

        strat_m = re.search(r"下单策略\s*\|\s*(.+?)(?:\s*\||\s*$)", pos_text, re.MULTILINE)
        if strat_m:
            rec["order_strategy"] = strat_m.group(1).strip()

    if not rec["direction"] and best_edge_side:
        rec["direction"] = best_edge_side

    return rec


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_pulse.py <pulse_report.md>", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1]).expanduser()
    if not path.exists():
        print(f"[ERROR] File not found: {path}", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding="utf-8")

    report_time = ""
    time_m = re.search(r"\*\*报告生成时间[：:]\*\*\s*(.+?)(?:\s*\(|$)", text, re.MULTILINE)
    if time_m:
        report_time = time_m.group(1).strip()

    recs = parse_report(text)

    output = {
        "source_file": str(path),
        "source_filename": path.name,
        "report_time": report_time,
        "recommendations": recs,
        "count": len(recs),
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"[INFO] Parsed {len(recs)} recommendations from {path.name}", file=sys.stderr)


if __name__ == "__main__":
    main()
