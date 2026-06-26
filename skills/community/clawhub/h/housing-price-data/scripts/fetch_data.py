#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_data.py - 抓取国家统计局70城住宅价格指数数据

用法：
  python fetch_data.py [--city <城市>] [--metrics <环比,同比>] [--limit <N>] [--latest] [--chart]

输出：JSON 格式数据到 stdout，或生成图表文件
"""
import argparse
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print(json.dumps({"error": "缺少依赖包，请运行: pip install -r requirements.txt"}, ensure_ascii=False))
    sys.exit(1)

from cache import SimpleCache
from config import (
    CACHE_CONFIG,
    CITY_ALIASES,
    DEFAULTS,
    INDICATORS,
    METRIC_ALIASES,
    REQUEST_CONFIG,
    RSS_URL,
    SUPPORTED_CITIES,
    TITLE_KEY,
    VALID_METRICS,
)
from exceptions import CityNotFoundError, DataUnavailableError, NetworkError, RSSFeedError

_cache = SimpleCache(
    max_size=CACHE_CONFIG["max_size"],
    ttl_seconds=CACHE_CONFIG["ttl_seconds"],
) if CACHE_CONFIG["enabled"] else None

PERIOD_RE = re.compile(r"(\d{4})\s*年\s*(\d{1,2})\s*月(?:份)?")
INDICATOR_ORDER = {
    INDICATORS["new"]: 0,
    INDICATORS["used"]: 1,
}
CHART_METRICS = ("环比", "同比")


def normalize(s: str) -> str:
    """规范化字符串。"""
    import html as html_mod

    s = html_mod.unescape(str(s))
    s = s.replace("\u00a0", " ").replace("\u3000", " ")
    s = s.replace("\t", " ").replace("\n", " ").replace("\r", " ")
    return " ".join(s.split())


def compact(s: str) -> str:
    """移除所有空白。"""
    return "".join(normalize(s).split())


def build_metric_alias_lookup() -> Dict[str, str]:
    """构建指标别名查找表。"""
    lookup = {}
    for canonical, aliases in METRIC_ALIASES.items():
        for alias in [canonical, *aliases]:
            lookup[compact(alias).lower()] = canonical
    return lookup


METRIC_ALIAS_LOOKUP = build_metric_alias_lookup()
SUPPORTED_CITY_LOOKUP = {compact(city): city for city in SUPPORTED_CITIES}


def normalize_metric_name(metric: str) -> Optional[str]:
    """将指标名称归一化为规范字段。"""
    key = compact(metric).lower()
    if not key:
        return None
    return METRIC_ALIAS_LOOKUP.get(key)


def normalize_city_name(city: str) -> str:
    """将城市名归一化为统计局使用的规范名称。"""
    normalized = normalize(city).strip()
    if not normalized:
        return normalized

    candidate = CITY_ALIASES.get(normalized, normalized)
    if candidate in SUPPORTED_CITIES:
        return candidate

    compact_candidate = compact(candidate)
    if compact_candidate in SUPPORTED_CITY_LOOKUP:
        return SUPPORTED_CITY_LOOKUP[compact_candidate]

    if candidate.endswith("市"):
        trimmed = candidate[:-1]
        if trimmed in SUPPORTED_CITIES:
            return trimmed
        compact_trimmed = compact(trimmed)
        if compact_trimmed in SUPPORTED_CITY_LOOKUP:
            return SUPPORTED_CITY_LOOKUP[compact_trimmed]

    return candidate


def parse_number(s: str) -> Optional[float]:
    """解析数字。"""
    s = normalize(s).rstrip("%").replace("，", "").replace(",", "").strip()
    if not s or s in ("-", "--"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def parse_period(title: str) -> Optional[str]:
    """从标题提取期次。"""
    match = PERIOD_RE.search(title)
    if not match:
        return None
    year, month = int(match.group(1)), int(match.group(2))
    return f"{year:04d}-{month:02d}"


def fetch_url(url: str, timeout: int = None) -> bytes:
    """获取 URL 内容，支持重试。"""
    if timeout is None:
        timeout = REQUEST_CONFIG["timeout"]

    normalized_url = url.strip()
    if _cache:
        cached = _cache.get(normalized_url)
        if cached:
            return cached

    last_err = None
    for attempt in range(REQUEST_CONFIG["max_attempts"]):
        try:
            response = requests.get(
                normalized_url,
                headers=REQUEST_CONFIG["headers"],
                timeout=timeout,
            )
            response.raise_for_status()
            content = response.content
            if _cache:
                _cache.set(normalized_url, content)
            return content
        except Exception as exc:
            last_err = exc
            if attempt < len(REQUEST_CONFIG["retry_delays"]):
                time.sleep(REQUEST_CONFIG["retry_delays"][attempt])

    raise NetworkError(f"网络请求失败: {last_err}", url=normalized_url)


def fetch_rss_items() -> List[Tuple[str, str]]:
    """获取 RSS 条目。"""
    try:
        content = fetch_url(RSS_URL)
        root = ET.fromstring(content)
    except Exception as exc:
        raise RSSFeedError(f"RSS 获取失败: {exc}", feed_url=RSS_URL) from exc

    items = []
    for item in root.iter("item"):
        title_el = item.find("title")
        link_el = item.find("link")
        if title_el is None or link_el is None:
            continue

        title = normalize(title_el.text or "")
        link = (link_el.text or "").strip()
        if TITLE_KEY not in title:
            continue

        label = parse_period(title)
        if label:
            items.append((label, link))

    if not items:
        raise RSSFeedError("RSS 中未找到匹配条目", feed_url=RSS_URL)

    items.sort(key=lambda item: item[0])
    return items


def looks_like_header(cells: List[str]) -> bool:
    """判断是否为表头行。"""
    for cell in cells:
        value = normalize(cell)
        if any(keyword in value for keyword in ("城市", "环比", "同比", "定基")):
            return True
    return False


def contains_category(cells: List[str]) -> bool:
    """判断是否包含分类表。"""
    return any("分类" in normalize(cell) for cell in cells)


def detect_indicator(table, preceding_text: List[str]) -> Optional[str]:
    """检测表格对应的指标类型。"""
    for text in reversed(preceding_text):
        normalized_text = compact(text)
        if compact(INDICATORS["new"]) in normalized_text and compact(INDICATORS["new_cat"]) not in normalized_text:
            return INDICATORS["new"]
        if compact(INDICATORS["used"]) in normalized_text and compact(INDICATORS["used_cat"]) not in normalized_text:
            return INDICATORS["used"]

    rows = table.find_all("tr")[:2]
    head_text = compact(" ".join(row.get_text() for row in rows))
    if compact(INDICATORS["new"]) in head_text and compact(INDICATORS["new_cat"]) not in head_text:
        return INDICATORS["new"]
    if compact(INDICATORS["used"]) in head_text and compact(INDICATORS["used_cat"]) not in head_text:
        return INDICATORS["used"]
    return None


def extract_row(tr) -> List[str]:
    """提取表格行文本。"""
    return [normalize(cell.get_text()) for cell in tr.find_all(["th", "td"]) if normalize(cell.get_text())]


def find_header(table) -> List[str]:
    """查找表头行。"""
    for tr in table.find_all("tr"):
        row = extract_row(tr)
        if row and looks_like_header(row):
            return row
    return []


def pick_city_segment(
    row: List[str],
    header: List[str],
    city: str,
) -> Tuple[Optional[List[str]], Optional[List[str]]]:
    """在可能包含多城市的行里找到目标城市所在片段。"""
    if not row:
        return None, None

    if header:
        city_columns = [idx for idx, name in enumerate(header) if "城市" in normalize(name)]
        if city_columns:
            for index, start in enumerate(city_columns):
                end = city_columns[index + 1] if index + 1 < len(city_columns) else len(header)
                row_slice = row[start:min(end, len(row))]
                if any(compact(city) in compact(cell) for cell in row_slice):
                    return header[start:end], row_slice

    header_length = len(header)
    if header_length > 0 and len(row) % header_length == 0:
        for start in range(0, len(row), header_length):
            row_slice = row[start:start + header_length]
            if any(compact(city) in compact(cell) for cell in row_slice):
                return header, row_slice

    if any(compact(city) in compact(cell) for cell in row):
        return header, row

    return None, None


def extract_city_metrics(
    seg_header: List[str],
    seg_row: List[str],
    target_city: str,
    target_metrics: List[str],
) -> Tuple[str, Dict[str, Optional[float]]]:
    """提取城市指标数据。"""
    size = min(len(seg_header), len(seg_row))
    city = ""
    metrics = {metric: None for metric in target_metrics}

    for index in range(size):
        key = normalize(seg_header[index])
        value = normalize(seg_row[index])
        if not key or not value:
            continue

        if any(label in key for label in ("城市", "地区", "城市名称")):
            if not city or compact(target_city) in compact(value):
                city = value
            continue

        if "分类" in key:
            continue

        matched_metrics = [metric for metric in target_metrics if metric in key]
        if not matched_metrics:
            continue

        parsed_value = parse_number(value)
        for metric in matched_metrics:
            metrics[metric] = parsed_value

    if not city:
        for cell in seg_row:
            if compact(target_city) in compact(cell):
                city = cell
                break

    return city, metrics


def parse_page(
    content: bytes,
    period_label: str,
    target_city: str,
    target_metrics: List[str],
    source_url: str = "",
) -> List[Dict]:
    """解析文章页面。"""
    soup = BeautifulSoup(content, "html.parser")

    tables = soup.select(".detail-text-content .txt-content .trs_editor_view table")
    if not tables:
        tables = soup.select(".trs_editor_view table")
    if not tables:
        tables = soup.find_all("table")

    records = {}

    for table in tables:
        preceding = []
        node = table
        for _ in range(4):
            count = 0
            for sibling in node.find_previous_siblings():
                text = normalize(sibling.get_text())
                if text:
                    preceding.insert(0, text)
                    count += 1
                    if count >= 4:
                        break
            node = node.parent
            if node is None:
                break

        indicator = detect_indicator(table, preceding)
        if not indicator:
            continue

        header = find_header(table)
        if not header or contains_category(header):
            continue

        for tr in table.find_all("tr"):
            row = extract_row(tr)
            if not row or looks_like_header(row):
                continue

            seg_header, seg_row = pick_city_segment(row, header, target_city)
            if not seg_header or not seg_row:
                continue

            city, metrics = extract_city_metrics(seg_header, seg_row, target_city, target_metrics)
            normalized_city = normalize_city_name(city) or target_city
            if compact(target_city) not in compact(normalized_city) and compact(target_city) not in compact(city):
                continue
            if not any(value is not None for value in metrics.values()):
                continue

            existing = records.get(indicator)
            non_null_count = sum(1 for value in metrics.values() if value is not None)
            if existing is None or non_null_count > sum(
                1 for value in existing["metrics"].values() if value is not None
            ):
                records[indicator] = {
                    "period": period_label,
                    "city": normalized_city,
                    "indicator": indicator,
                    "metrics": metrics,
                    "source_url": source_url,
                }

    return list(records.values())


def validate_params(city: str, metrics: List[str], limit: int) -> Tuple[str, List[str], Optional[str]]:
    """验证参数并返回规范化结果。"""
    resolved_city = normalize_city_name(city)
    if not resolved_city:
        return resolved_city, metrics, "城市名不能为空"
    if resolved_city not in SUPPORTED_CITIES:
        error = CityNotFoundError(city)
        return resolved_city, metrics, str(error)

    valid_metrics = []
    invalid_metrics = []
    for metric in metrics:
        normalized_metric = normalize_metric_name(metric)
        if normalized_metric:
            if normalized_metric not in valid_metrics:
                valid_metrics.append(normalized_metric)
        else:
            invalid_metrics.append(metric)

    if invalid_metrics:
        return resolved_city, valid_metrics, (
            f"无效指标: {', '.join(invalid_metrics)}。有效指标: {', '.join(VALID_METRICS)}"
        )
    if not valid_metrics:
        return resolved_city, metrics, f"至少需要一个有效指标。有效指标: {', '.join(VALID_METRICS)}"
    if limit < 1:
        return resolved_city, valid_metrics, "limit 必须大于等于 1"

    return resolved_city, valid_metrics, None


def build_chart_series(records: List[Dict]) -> Dict[str, object]:
    """构建按期次对齐的图表序列。"""
    periods = sorted({record["period"] for record in records})
    indexed_records = {period: {} for period in periods}
    for record in records:
        indexed_records.setdefault(record["period"], {})[record["indicator"]] = record

    series = {
        INDICATORS["new"]: {metric: [] for metric in CHART_METRICS},
        INDICATORS["used"]: {metric: [] for metric in CHART_METRICS},
    }

    for period in periods:
        for indicator in (INDICATORS["new"], INDICATORS["used"]):
            record = indexed_records.get(period, {}).get(indicator)
            for metric in CHART_METRICS:
                value = None
                if record:
                    value = record["metrics"].get(metric)
                series[indicator][metric].append(value)

    gap = []
    for new_value, used_value in zip(series[INDICATORS["new"]]["同比"], series[INDICATORS["used"]]["同比"]):
        gap.append(None if new_value is None or used_value is None else new_value - used_value)

    return {
        "periods": periods,
        "series": series,
        "gap": gap,
    }


def points_from_series(values: List[Optional[float]]) -> List[Tuple[int, float]]:
    """提取折线图有效点位。"""
    return [(index, value) for index, value in enumerate(values) if value is not None]


def sort_records(records: List[Dict]) -> List[Dict]:
    """稳定排序结果。"""
    return sorted(
        records,
        key=lambda record: (
            record["period"],
            INDICATOR_ORDER.get(record["indicator"], 99),
        ),
    )


def generate_chart(records: List[Dict], city: str, output_path: str = None) -> str:
    """生成分析图表。"""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print(json.dumps({"error": "缺少 matplotlib，请运行: pip install matplotlib"}, ensure_ascii=False))
        return None

    plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "SimHei", "STHeiti", "PingFang SC"]
    plt.rcParams["axes.unicode_minus"] = False

    chart_data = build_chart_series(records)
    periods = chart_data["periods"]
    new_series = chart_data["series"][INDICATORS["new"]]
    used_series = chart_data["series"][INDICATORS["used"]]
    gap_series = chart_data["gap"]

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f"{city}住宅销售价格指数分析", fontsize=16, fontweight="bold")

    x_positions = list(range(len(periods)))
    tick_step = 1 if len(periods) <= 6 else 3

    ax1 = axes[0, 0]
    for values, color, label, marker in (
        (new_series["环比"], "#2E86AB", "新建商品住宅", "o"),
        (used_series["环比"], "#E94F37", "二手住宅", "s"),
    ):
        valid_points = points_from_series(values)
        if valid_points:
            x_values, y_values = zip(*valid_points)
            ax1.plot(x_values, y_values, f"{marker}-", color=color, label=label, linewidth=2, markersize=4)
    ax1.axhline(y=100, color="gray", linestyle="--", alpha=0.5, label="基准线(100)")
    ax1.set_title("环比指数趋势 (上月=100)", fontsize=12)
    ax1.set_xlabel("期次")
    ax1.set_ylabel("指数")
    ax1.legend(loc="lower left")
    ax1.set_ylim(97, 102)
    ax1.set_xticks(x_positions[::tick_step])
    ax1.set_xticklabels(periods[::tick_step], rotation=45, ha="right")
    ax1.grid(True, alpha=0.3)

    ax2 = axes[0, 1]
    for values, color, label, marker in (
        (new_series["同比"], "#2E86AB", "新建商品住宅", "o"),
        (used_series["同比"], "#E94F37", "二手住宅", "s"),
    ):
        valid_points = points_from_series(values)
        if valid_points:
            x_values, y_values = zip(*valid_points)
            ax2.plot(x_values, y_values, f"{marker}-", color=color, label=label, linewidth=2, markersize=4)
    ax2.axhline(y=100, color="gray", linestyle="--", alpha=0.5, label="基准线(100)")
    ax2.set_title("同比指数趋势 (上年同月=100)", fontsize=12)
    ax2.set_xlabel("期次")
    ax2.set_ylabel("指数")
    ax2.legend(loc="lower left")
    ax2.set_ylim(85, 105)
    ax2.set_xticks(x_positions[::tick_step])
    ax2.set_xticklabels(periods[::tick_step], rotation=45, ha="right")
    ax2.grid(True, alpha=0.3)

    ax3 = axes[1, 0]
    width = 0.35
    new_change = [np.nan if value is None else value - 100 for value in new_series["同比"]]
    used_change = [np.nan if value is None else value - 100 for value in used_series["同比"]]
    ax3.bar([index - width / 2 for index in x_positions], new_change, width, color="#2E86AB", label="新建商品住宅", alpha=0.8)
    ax3.bar([index + width / 2 for index in x_positions], used_change, width, color="#E94F37", label="二手住宅", alpha=0.8)
    ax3.axhline(y=0, color="gray", linestyle="-", alpha=0.5)
    ax3.set_title("同比涨跌幅 (%)", fontsize=12)
    ax3.set_xlabel("期次")
    ax3.set_ylabel("涨跌幅 (%)")
    ax3.legend(loc="lower left")
    ax3.set_xticks(x_positions[::tick_step])
    ax3.set_xticklabels(periods[::tick_step], rotation=45, ha="right")
    ax3.grid(True, alpha=0.3, axis="y")

    ax4 = axes[1, 1]
    gap_values = [np.nan if value is None else value for value in gap_series]
    colors = ["#CFCFCF" if value is None else ("#2E86AB" if value > 0 else "#E94F37") for value in gap_series]
    ax4.bar(x_positions, gap_values, color=colors, alpha=0.8)
    ax4.axhline(y=0, color="gray", linestyle="-", alpha=0.5)
    ax4.set_title("新房与二手房同比指数差值", fontsize=12)
    ax4.set_xlabel("期次")
    ax4.set_ylabel("差值 (新房 - 二手房)")
    ax4.set_xticks(x_positions[::tick_step])
    ax4.set_xticklabels(periods[::tick_step], rotation=45, ha="right")
    ax4.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()

    if output_path is None:
        output_file = Path(__file__).resolve().parent.parent / f"{city}_housing_analysis.png"
    else:
        output_file = Path(output_path).expanduser()
    output_file.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(str(output_file), dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    return str(output_file)


def make_output(
    requested_city: str,
    matched_city: str,
    metrics: List[str],
    records: List[Dict],
    items_scanned: int,
) -> Dict[str, object]:
    """组装统一输出。"""
    latest_period = max(record["period"] for record in records)
    output = {
        "city": matched_city,
        "requested_city": requested_city,
        "matched_city": matched_city,
        "metrics": metrics,
        "latest_period": latest_period,
        "record_count": len(records),
        "records": records,
        "items_scanned": items_scanned,
    }
    if _cache:
        output["cache_size"] = _cache.size()
    return output


def main():
    parser = argparse.ArgumentParser(
        description="获取中国70城住宅价格指数数据",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python fetch_data.py --city 武汉 --metrics 环比,同比 --latest
  python fetch_data.py --city 上海市 --metrics yoy --limit 12
  python fetch_data.py --city 北京 --metrics 环比,同比 --chart --limit 24
        """,
    )
    parser.add_argument(
        "--city",
        default=DEFAULTS["city"],
        help=f"目标城市名称 (默认: {DEFAULTS['city']})",
    )
    parser.add_argument(
        "--metrics",
        default=DEFAULTS["metrics"],
        help=f"指标，逗号分隔 (默认: {DEFAULTS['metrics']})",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULTS["limit"],
        help=f"最多返回期数 (默认: {DEFAULTS['limit']})",
    )
    parser.add_argument(
        "--latest",
        action="store_true",
        help="只返回最新一期数据",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="禁用缓存",
    )
    parser.add_argument(
        "--chart",
        action="store_true",
        help="生成分析图表",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="图表输出路径 (仅与 --chart 配合使用)",
    )
    args = parser.parse_args()

    requested_city = normalize(args.city).strip()
    requested_metrics = [metric.strip() for metric in args.metrics.split(",") if metric.strip()]
    target_city, target_metrics, error = validate_params(requested_city, requested_metrics, args.limit)
    if error:
        error_payload = {
            "error": error,
            "requested_city": requested_city,
            "matched_city": target_city or None,
            "metrics": target_metrics,
        }
        if "未在70个大中城市列表中" in error:
            error_payload["hint"] = "参考 references/REFERENCE.md 中的城市列表"
        print(json.dumps(error_payload, ensure_ascii=False))
        sys.exit(1)

    global _cache
    if args.no_cache:
        _cache = None

    try:
        rss_items = fetch_rss_items()
    except (RSSFeedError, NetworkError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        sys.exit(1)

    selected_items = rss_items[-1:] if args.latest else rss_items[-args.limit:]
    all_records = []
    page_failures = 0

    for period_label, url in selected_items:
        try:
            content = fetch_url(url)
        except NetworkError:
            page_failures += 1
            continue

        records = parse_page(content, period_label, target_city, target_metrics, source_url=url)
        all_records.extend(records)

    if selected_items and page_failures == len(selected_items):
        error = NetworkError("所有数据详情页请求均失败")
        print(json.dumps({"error": str(error)}, ensure_ascii=False))
        sys.exit(1)

    if not all_records:
        error = DataUnavailableError(
            f"城市「{target_city}」暂无可用数据，或所选指标在已扫描期次中未匹配到",
            city=target_city,
        )
        print(json.dumps({
            "error": str(error),
            "requested_city": requested_city,
            "matched_city": target_city,
            "metrics": target_metrics,
            "items_scanned": len(selected_items),
        }, ensure_ascii=False))
        sys.exit(1)

    all_records = sort_records(all_records)
    matched_city = next((record["city"] for record in all_records if record.get("city")), target_city)
    output = make_output(requested_city, matched_city, target_metrics, all_records, len(selected_items))

    if args.chart:
        chart_path = generate_chart(all_records, matched_city, args.output)
        if not chart_path:
            sys.exit(1)
        output["chart_path"] = chart_path

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
