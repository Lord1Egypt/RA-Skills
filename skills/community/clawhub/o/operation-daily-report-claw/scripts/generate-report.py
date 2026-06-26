#!/usr/bin/env python3
"""
generate-report.py — 运营数据日报生成脚本
依赖：python3, pandas, jinja2
用法：
  python3 generate-report.py --date yesterday
  python3 generate-report.py --date 2026-03-31
  python3 generate-report.py --type weekly --date 2026-03-31
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ---- 路径配置 ----
SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent
DATA_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "data" / "reports"
REFS_DIR = BASE_DIR / "references"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---- 异常规则（简化版，完整规则见 references/anomaly-rules.md）----
ANOMALY_RULES = {
    "views_drop": {"threshold": -0.30, "severity": "高", "label": "播放量暴跌"},
    "followers_drop": {"threshold": -100, "severity": "高", "label": "掉粉预警"},
    "engagement_low": {
        "douyin": 0.015,
        "xiaohongshu": 0.025,
        "shipinhao": 0.02,
        "default": 0.015,
        "severity": "高",
        "label": "互动率极低",
    },
    "completion_low": {"threshold": 0.15, "severity": "高", "label": "完播率极低"},
}

PLATFORMS = ["douyin", "xiaohongshu", "shipinhao", "bilibili", "weibo"]
PLATFORM_NAMES = {
    "douyin": "抖音",
    "xiaohongshu": "小红书",
    "shipinhao": "视频号",
    "bilibili": "B站",
    "weibo": "微博",
}


def parse_date(date_str: str) -> datetime:
    if date_str == "yesterday":
        return datetime.now() - timedelta(days=1)
    if date_str == "today":
        return datetime.now()
    return datetime.strptime(date_str, "%Y-%m-%d")


def load_platform_data(platform: str, date: datetime) -> dict | None:
    """加载指定平台指定日期的数据"""
    date_str = date.strftime("%Y-%m-%d")
    path = DATA_DIR / f"{platform}_{date_str}.json"
    if not path.exists():
        return None
    try:
        with open(path) as f:
            data = json.load(f)
        if "error" in data:
            print(f"[WARN] {platform} 数据异常: {data['error']}", file=sys.stderr)
            return None
        return data
    except Exception as e:
        print(f"[WARN] 读取 {platform} 数据失败: {e}", file=sys.stderr)
        return None


def load_history(platform: str, date: datetime, days: int = 7) -> list[dict]:
    """加载近 N 天历史数据"""
    history = []
    for i in range(days):
        d = date - timedelta(days=i)
        data = load_platform_data(platform, d)
        if data:
            history.append(data)
    return history


def calc_change(current: float, previous: float) -> str:
    """计算环比变化"""
    if previous == 0:
        return "N/A"
    change = (current - previous) / previous
    sign = "▲" if change >= 0 else "▼"
    return f"{sign}{abs(change):.1%}"


def detect_anomalies(current: dict, previous: dict | None) -> list[dict]:
    """检测异常数据"""
    anomalies = []
    platform = current.get("platform", "unknown")

    # 播放量暴跌
    if previous and previous.get("views", 0) > 0:
        change = (current.get("views", 0) - previous["views"]) / previous["views"]
        if change < ANOMALY_RULES["views_drop"]["threshold"]:
            anomalies.append({
                "platform": PLATFORM_NAMES.get(platform, platform),
                "metric": "播放量",
                "current": current.get("views", 0),
                "change": f"{change:.1%}",
                "severity": ANOMALY_RULES["views_drop"]["severity"],
                "label": ANOMALY_RULES["views_drop"]["label"],
            })

    # 掉粉预警
    new_followers = current.get("new_followers", 0)
    if new_followers < ANOMALY_RULES["followers_drop"]["threshold"]:
        anomalies.append({
            "platform": PLATFORM_NAMES.get(platform, platform),
            "metric": "涨粉数",
            "current": new_followers,
            "change": str(new_followers),
            "severity": ANOMALY_RULES["followers_drop"]["severity"],
            "label": ANOMALY_RULES["followers_drop"]["label"],
        })

    # 互动率极低
    views = current.get("views", 0)
    if views > 0:
        interactions = (
            current.get("likes", 0)
            + current.get("comments", 0)
            + current.get("shares", 0)
        )
        engagement_rate = interactions / views
        threshold = ANOMALY_RULES["engagement_low"].get(
            platform, ANOMALY_RULES["engagement_low"]["default"]
        )
        if engagement_rate < threshold:
            anomalies.append({
                "platform": PLATFORM_NAMES.get(platform, platform),
                "metric": "互动率",
                "current": f"{engagement_rate:.2%}",
                "change": f"低于基准 {threshold:.1%}",
                "severity": ANOMALY_RULES["engagement_low"]["severity"],
                "label": ANOMALY_RULES["engagement_low"]["label"],
            })

    # 完播率极低（视频平台）
    completion = current.get("completion_rate", None)
    if completion is not None and completion < ANOMALY_RULES["completion_low"]["threshold"]:
        anomalies.append({
            "platform": PLATFORM_NAMES.get(platform, platform),
            "metric": "完播率",
            "current": f"{completion:.1%}",
            "change": f"低于阈值 {ANOMALY_RULES['completion_low']['threshold']:.0%}",
            "severity": ANOMALY_RULES["completion_low"]["severity"],
            "label": ANOMALY_RULES["completion_low"]["label"],
        })

    return anomalies


def render_daily_report(date: datetime) -> str:
    """生成日报 Markdown"""
    date_str = date.strftime("%Y-%m-%d")
    prev_date = date - timedelta(days=1)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    platform_sections = []
    all_anomalies = []
    total_views = 0
    total_new_followers = 0

    for platform in PLATFORMS:
        current = load_platform_data(platform, date)
        if not current:
            continue

        previous = load_platform_data(platform, prev_date)
        anomalies = detect_anomalies(current, previous)
        all_anomalies.extend(anomalies)

        views = current.get("views", 0)
        new_followers = current.get("new_followers", 0)
        total_views += views
        total_new_followers += new_followers

        views_change = calc_change(views, previous.get("views", 0)) if previous else "N/A"
        interactions = (
            current.get("likes", 0)
            + current.get("comments", 0)
            + current.get("shares", 0)
        )
        engagement_rate = f"{interactions / views:.2%}" if views > 0 else "N/A"

        section = f"""### {PLATFORM_NAMES.get(platform, platform)}
- 播放量/阅读量：{views:,}（环比 {views_change}）
- 点赞：{current.get('likes', 0):,} | 评论：{current.get('comments', 0):,} | 转发：{current.get('shares', 0):,}
- 涨粉：+{new_followers:,}（总粉丝：{current.get('total_followers', 0):,}）
- 互动率：{engagement_rate}"""

        if current.get("completion_rate") is not None:
            section += f"\n- 完播率：{current['completion_rate']:.1%}"

        platform_sections.append(section)

    # 异常区块
    if all_anomalies:
        anomaly_lines = "\n".join(
            f"- ⚠️ **{a['platform']}** {a['label']}：{a['metric']} = {a['current']}（{a['change']}）"
            for a in all_anomalies
        )
        anomaly_section = f"## ⚠️ 异常提醒\n\n{anomaly_lines}"
    else:
        anomaly_section = "## ✅ 今日数据无异常"

    platforms_text = "\n\n".join(platform_sections) if platform_sections else "暂无数据（请检查 API 配置）"

    report = f"""# 运营数据日报 · {date_str}

> 生成时间：{generated_at} | 数据来源：各平台 API

---

## 📊 数据概览

**合计播放量**：{total_views:,}　**合计涨粉**：+{total_new_followers:,}

---

## 各平台详情

{platforms_text}

---

{anomaly_section}
"""
    return report


def render_weekly_report(end_date: datetime) -> str:
    """生成周报 Markdown"""
    start_date = end_date - timedelta(days=6)
    date_range = f"{start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}"
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    rows = []
    for i in range(7):
        d = start_date + timedelta(days=i)
        date_str = d.strftime("%Y-%m-%d")
        day_total_views = 0
        day_total_followers = 0
        for platform in PLATFORMS:
            data = load_platform_data(platform, d)
            if data:
                day_total_views += data.get("views", 0)
                day_total_followers += data.get("new_followers", 0)
        rows.append(f"| {date_str} | {day_total_views:,} | +{day_total_followers:,} |")

    table = "\n".join(rows)

    report = f"""# 运营数据周报 · {date_range}

> 生成时间：{generated_at}

---

## 近 7 日趋势

| 日期 | 合计播放量 | 合计涨粉 |
|------|-----------|---------|
{table}

---

*详细平台数据请查看各日日报*
"""
    return report


def main():
    parser = argparse.ArgumentParser(description="运营数据日报生成脚本")
    parser.add_argument("--date", default="yesterday", help="日期（yesterday/today/YYYY-MM-DD）")
    parser.add_argument("--type", choices=["daily", "weekly"], default="daily", help="报告类型")
    parser.add_argument("--output", help="输出文件路径（默认自动生成）")
    args = parser.parse_args()

    target_date = parse_date(args.date)
    date_str = target_date.strftime("%Y-%m-%d")

    if args.type == "weekly":
        content = render_weekly_report(target_date)
        filename = f"weekly_{date_str}.md"
    else:
        content = render_daily_report(target_date)
        filename = f"daily_{date_str}.md"

    output_path = Path(args.output) if args.output else OUTPUT_DIR / filename
    output_path.write_text(content, encoding="utf-8")
    print(f"[OK] 报告已生成：{output_path}")
    print(content)


if __name__ == "__main__":
    main()
