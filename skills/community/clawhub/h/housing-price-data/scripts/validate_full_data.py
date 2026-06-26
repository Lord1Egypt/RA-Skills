#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_full_data.py - 拉取并校验国家统计局70城住宅价格指数全量数据

功能：
1. 拉取 RSS 中全部期次数据
2. 独立解析每期 70 城新房/二手房表格
3. 校验数据格式、完整性与当前按城市查询解析器的一致性
4. 可选导出全量数据与校验报告
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from bs4 import BeautifulSoup

import fetch_data
from config import INDICATORS, SUPPORTED_CITIES, VALID_METRICS
from exceptions import NetworkError, RSSFeedError

PERIOD_PATTERN = re.compile(r"^\d{4}-\d{2}$")
TARGET_INDICATORS = (INDICATORS["new"], INDICATORS["used"])


def split_row_segments(header: List[str], row: List[str]) -> List[Tuple[List[str], List[str]]]:
    """将可能包含多城市的单行拆成若干城市片段。"""
    if not header or not row:
        return []

    city_columns = [index for index, name in enumerate(header) if "城市" in fetch_data.normalize(name)]
    if len(city_columns) > 1:
        segments = []
        for index, start in enumerate(city_columns):
            end = city_columns[index + 1] if index + 1 < len(city_columns) else len(header)
            segment_row = row[start:min(end, len(row))]
            if segment_row:
                segments.append((header[start:end], segment_row))
        if segments:
            return segments

    header_length = len(header)
    if header_length > 0 and len(row) % header_length == 0 and len(row) > header_length:
        return [(header, row[index:index + header_length]) for index in range(0, len(row), header_length)]

    return [(header, row)]


def extract_segment_record(
    seg_header: List[str],
    seg_row: List[str],
    indicator: str,
    period_label: str,
    source_url: str,
) -> Optional[Dict[str, object]]:
    """将一个城市片段解析为结构化记录。"""
    size = min(len(seg_header), len(seg_row))
    city = ""
    metrics: Dict[str, Optional[float]] = {}

    for index in range(size):
        key = fetch_data.normalize(seg_header[index])
        value = fetch_data.normalize(seg_row[index])
        if not key or not value:
            continue

        if any(label in key for label in ("城市", "地区", "城市名称")):
            city = fetch_data.normalize_city_name(value)
            continue

        if "分类" in key:
            continue

        for metric in VALID_METRICS:
            if metric in key:
                metrics[metric] = fetch_data.parse_number(value)

    if not city or city not in SUPPORTED_CITIES:
        return None
    if not any(value is not None for value in metrics.values()):
        return None

    return {
        "period": period_label,
        "city": city,
        "indicator": indicator,
        "metrics": metrics,
        "source_url": source_url,
    }


def parse_full_page(content: bytes, period_label: str, source_url: str) -> List[Dict[str, object]]:
    """独立解析单期页面中的全量 70 城数据。"""
    soup = BeautifulSoup(content, "html.parser")

    tables = soup.select(".detail-text-content .txt-content .trs_editor_view table")
    if not tables:
        tables = soup.select(".trs_editor_view table")
    if not tables:
        tables = soup.find_all("table")

    page_records: Dict[Tuple[str, str], Dict[str, object]] = {}

    for table in tables:
        preceding = []
        node = table
        for _ in range(4):
            count = 0
            for sibling in node.find_previous_siblings():
                text = fetch_data.normalize(sibling.get_text())
                if text:
                    preceding.insert(0, text)
                    count += 1
                    if count >= 4:
                        break
            node = node.parent
            if node is None:
                break

        indicator = fetch_data.detect_indicator(table, preceding)
        if indicator not in TARGET_INDICATORS:
            continue

        header = fetch_data.find_header(table)
        if not header or fetch_data.contains_category(header):
            continue

        for tr in table.find_all("tr"):
            row = fetch_data.extract_row(tr)
            if not row or fetch_data.looks_like_header(row):
                continue

            for seg_header, seg_row in split_row_segments(header, row):
                record = extract_segment_record(seg_header, seg_row, indicator, period_label, source_url)
                if not record:
                    continue

                record_key = (record["city"], record["indicator"])
                existing = page_records.get(record_key)
                record_non_null = sum(1 for value in record["metrics"].values() if value is not None)
                if existing is None or record_non_null > sum(
                    1 for value in existing["metrics"].values() if value is not None
                ):
                    page_records[record_key] = record

    return sorted(
        page_records.values(),
        key=lambda record: (
            record["period"],
            SUPPORTED_CITIES.index(record["city"]),
            TARGET_INDICATORS.index(record["indicator"]),
        ),
    )


def validate_record_schema(record: Dict[str, object]) -> List[str]:
    """校验单条记录的数据格式。"""
    issues = []

    if not isinstance(record.get("period"), str) or not PERIOD_PATTERN.match(record["period"]):
        issues.append(f"invalid period: {record.get('period')}")
    if record.get("city") not in SUPPORTED_CITIES:
        issues.append(f"invalid city: {record.get('city')}")
    if record.get("indicator") not in TARGET_INDICATORS:
        issues.append(f"invalid indicator: {record.get('indicator')}")
    if not isinstance(record.get("source_url"), str) or not record["source_url"].startswith("https://"):
        issues.append(f"invalid source_url: {record.get('source_url')}")

    metrics = record.get("metrics")
    if not isinstance(metrics, dict) or not metrics:
        issues.append("metrics missing or invalid")
    else:
        for metric_name, metric_value in metrics.items():
            if metric_name not in VALID_METRICS:
                issues.append(f"invalid metric key: {metric_name}")
            if metric_value is not None and not isinstance(metric_value, (int, float)):
                issues.append(f"invalid metric value type for {metric_name}: {type(metric_value).__name__}")

    return issues


def compare_records(
    expected_records: List[Dict[str, object]],
    actual_records: List[Dict[str, object]],
) -> List[str]:
    """比较全量独立解析结果与按城市解析结果。"""
    issues = []
    expected_map = {record["indicator"]: record for record in expected_records}
    actual_map = {record["indicator"]: record for record in actual_records}

    if set(expected_map) != set(actual_map):
        issues.append(
            "indicator mismatch: "
            f"expected={sorted(expected_map)} actual={sorted(actual_map)}"
        )
        return issues

    for indicator in sorted(expected_map):
        expected = expected_map[indicator]
        actual = actual_map[indicator]

        if expected["city"] != actual["city"]:
            issues.append(f"city mismatch for {indicator}: expected={expected['city']} actual={actual['city']}")

        metric_names = sorted(set(expected["metrics"]) | set(actual["metrics"]))
        for metric_name in metric_names:
            expected_value = expected["metrics"].get(metric_name)
            actual_value = actual["metrics"].get(metric_name)
            if expected_value != actual_value:
                issues.append(
                    f"value mismatch for {indicator}/{metric_name}: "
                    f"expected={expected_value} actual={actual_value}"
                )

    return issues


def validate_page_records(
    period_label: str,
    url: str,
    content: bytes,
    full_records: List[Dict[str, object]],
    compare_targeted: bool,
) -> Dict[str, object]:
    """校验单页记录的格式、完整性和准确性。"""
    page_issues: List[str] = []
    targeted_mismatches: List[Dict[str, object]] = []

    for record in full_records:
        page_issues.extend(validate_record_schema(record))

    counts_by_indicator = Counter(record["indicator"] for record in full_records)
    cities_by_indicator = {
        indicator: {record["city"] for record in full_records if record["indicator"] == indicator}
        for indicator in TARGET_INDICATORS
    }

    for indicator in TARGET_INDICATORS:
        if counts_by_indicator[indicator] != len(SUPPORTED_CITIES):
            page_issues.append(
                f"{period_label} {indicator} count={counts_by_indicator[indicator]} expected={len(SUPPORTED_CITIES)}"
            )
        if cities_by_indicator[indicator] != set(SUPPORTED_CITIES):
            missing = sorted(set(SUPPORTED_CITIES) - cities_by_indicator[indicator])
            extra = sorted(cities_by_indicator[indicator] - set(SUPPORTED_CITIES))
            if missing:
                page_issues.append(f"{period_label} {indicator} missing cities: {missing[:10]}")
            if extra:
                page_issues.append(f"{period_label} {indicator} unexpected cities: {extra[:10]}")

    if compare_targeted:
        grouped_full = {
            city: [record for record in full_records if record["city"] == city]
            for city in SUPPORTED_CITIES
        }
        for city in SUPPORTED_CITIES:
            expected_records = grouped_full.get(city, [])
            actual_records = fetch_data.parse_page(content, period_label, city, VALID_METRICS, source_url=url)
            comparison_issues = compare_records(expected_records, actual_records)
            if comparison_issues:
                targeted_mismatches.append({
                    "period": period_label,
                    "city": city,
                    "issues": comparison_issues,
                })

    return {
        "period": period_label,
        "source_url": url,
        "record_count": len(full_records),
        "issues": page_issues,
        "targeted_mismatches": targeted_mismatches,
    }


def ensure_parent(path: Path) -> None:
    """确保输出目录存在。"""
    path.parent.mkdir(parents=True, exist_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="拉取并校验国家统计局70城住宅价格指数全量数据")
    parser.add_argument(
        "--dataset-output",
        type=str,
        default=None,
        help="全量数据 JSON 输出路径",
    )
    parser.add_argument(
        "--report-output",
        type=str,
        default=None,
        help="校验报告 JSON 输出路径",
    )
    parser.add_argument(
        "--skip-targeted-compare",
        action="store_true",
        help="跳过与按城市解析器的一致性比对",
    )
    args = parser.parse_args()

    compare_targeted = not args.skip_targeted_compare

    try:
        rss_items = fetch_data.fetch_rss_items()
    except (RSSFeedError, NetworkError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        sys.exit(1)

    all_records: List[Dict[str, object]] = []
    page_reports = []
    fetch_failures = []

    for period_label, url in rss_items:
        try:
            content = fetch_data.fetch_url(url)
        except NetworkError as exc:
            fetch_failures.append({
                "period": period_label,
                "source_url": url,
                "error": str(exc),
            })
            continue

        full_records = parse_full_page(content, period_label, url)
        all_records.extend(full_records)
        page_reports.append(validate_page_records(period_label, url, content, full_records, compare_targeted))

    total_issues = sum(len(page_report["issues"]) for page_report in page_reports)
    total_targeted_mismatches = sum(len(page_report["targeted_mismatches"]) for page_report in page_reports)

    report = {
        "rss_items": len(rss_items),
        "pages_fetched": len(page_reports),
        "fetch_failures": fetch_failures,
        "record_count": len(all_records),
        "expected_records_per_page": len(SUPPORTED_CITIES) * len(TARGET_INDICATORS),
        "schema_or_completeness_issue_count": total_issues,
        "targeted_mismatch_count": total_targeted_mismatches,
        "page_reports": page_reports,
    }

    if args.dataset_output:
        dataset_path = Path(args.dataset_output).expanduser()
        ensure_parent(dataset_path)
        dataset_payload = {
            "rss_items": len(rss_items),
            "record_count": len(all_records),
            "records": all_records,
        }
        dataset_path.write_text(json.dumps(dataset_payload, ensure_ascii=False, indent=2))
        report["dataset_output"] = str(dataset_path)

    if args.report_output:
        report_path = Path(args.report_output).expanduser()
        ensure_parent(report_path)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2))
        report["report_output"] = str(report_path)

    print(json.dumps(report, ensure_ascii=False, indent=2))

    if fetch_failures or total_issues or total_targeted_mismatches:
        sys.exit(1)


if __name__ == "__main__":
    main()
