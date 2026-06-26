#!/usr/bin/env python3
"""
report.py - Generate a markdown evidence report for ISP complaints or upgrade decisions.

Usage:
  python3 report.py
  python3 report.py --log /path/to/speed_log.jsonl --out report.md
  python3 report.py --days 30
"""

import json
import os
import subprocess
import sys
from datetime import datetime

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANALYZE_SCRIPT = os.path.join(SKILL_DIR, "scripts", "analyze.py")
DEFAULT_LOG_FILE = os.path.expanduser("~/.isp-throttle-detective/speed_log.jsonl")
DEFAULT_REPORT_DIR = os.path.expanduser("~/.isp-throttle-detective/reports")


def run_analysis(log_path: str, days: int) -> dict:
    result = subprocess.run(
        [sys.executable, ANALYZE_SCRIPT, "--log", log_path, "--days", str(days), "--json"],
        capture_output=True, text=True
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError(f"Analysis failed: {result.stderr}")
    return json.loads(result.stdout)


def spark_line(values: list[float], width: int = 20) -> str:
    """Generate a text-based sparkline from a list of values."""
    blocks = " ▁▂▃▄▅▆▇█"
    if not values:
        return ""
    mn, mx = min(values), max(values)
    if mx == mn:
        return blocks[4] * min(len(values), width)
    scaled = [int((v - mn) / (mx - mn) * (len(blocks) - 1)) for v in values[-width:]]
    return "".join(blocks[s] for s in scaled)


def peak_table(peak_data: dict) -> str:
    lines = [
        "| Period | Avg Speed | Sample Count |",
        "|--------|-----------|--------------|",
        f"| Peak hours | **{peak_data['peak']['avg_mbps']} Mbps** | {peak_data['peak']['count']} |",
        f"| Off-peak | **{peak_data['off_peak']['avg_mbps']} Mbps** | {peak_data['off_peak']['count']} |",
    ]
    diff = peak_data.get("difference_mbps")
    if diff is not None and diff > 0:
        lines.append(f"| **Degradation** | **{diff} Mbps slower at peak** | — |")
    return "\n".join(lines)


def endpoint_table(by_endpoint: dict) -> str:
    lines = [
        "| Endpoint | Category | Avg (Mbps) | Min | Max | Std Dev | Tests |",
        "|----------|----------|-----------|-----|-----|---------|-------|",
    ]
    for k, v in by_endpoint.items():
        lines.append(
            f"| {v['label']} | {v['category']} | **{v['avg_mbps']}** | {v['min_mbps']} | {v['max_mbps']} | {v['stdev']} | {v['count']} |"
        )
    return "\n".join(lines)


def hour_chart(by_hour: dict) -> str:
    if not by_hour:
        return "_No hourly data available._"
    hours = sorted(by_hour.keys(), key=int)
    speeds = [by_hour[h]["avg_mbps"] for h in hours]
    max_speed = max(speeds) if speeds else 1
    lines = ["```"]
    for h, s in zip(hours, speeds):
        bar_len = int((s / max_speed) * 30) if max_speed > 0 else 0
        bar = "█" * bar_len
        lines.append(f"  {int(h):02d}:00  {bar:<30s}  {s:.1f} Mbps")
    lines.append("```")
    return "\n".join(lines)


def throttle_indicators(analysis: dict) -> list[str]:
    indicators = []
    cdn = analysis.get("cdn_discrimination", {})
    peak = analysis.get("peak_vs_offpeak", {})
    trend = analysis.get("trend", {})
    anomalies = analysis.get("anomalies", [])

    # Peak throttling
    diff = peak.get("difference_mbps")
    peak_avg = peak.get("peak", {}).get("avg_mbps", 0)
    offpeak_avg = peak.get("off_peak", {}).get("avg_mbps", 0)
    if diff and offpeak_avg and diff / offpeak_avg > 0.20:
        indicators.append(
            f"⚠️ **Peak-hour throttling**: Speeds drop {diff} Mbps ({round(diff/offpeak_avg*100)}%) "
            f"during peak hours ({offpeak_avg} → {peak_avg} Mbps)"
        )

    # CDN discrimination
    if cdn.get("cdn_throttling_suspected"):
        ratio = cdn.get("cdn_vs_general_ratio", "?")
        indicators.append(
            f"⚠️ **CDN/streaming throttling**: CDN speeds are only {round(ratio*100)}% of general internet speeds. "
            f"CDN avg: {cdn.get('cdn_avg_mbps')} Mbps vs general: {cdn.get('general_avg_mbps')} Mbps"
        )

    # Declining trend
    if trend.get("trend") == "declining":
        slope = trend.get("slope_mbps_per_day", 0)
        first = trend.get("first_week_avg", "?")
        last = trend.get("last_week_avg", "?")
        indicators.append(
            f"📉 **Degrading service**: Speed declining at {abs(slope):.2f} Mbps/day. "
            f"First week avg: {first} Mbps → Last week avg: {last} Mbps"
        )

    # Frequent anomalies
    if len(anomalies) >= 5:
        indicators.append(
            f"⚠️ **Frequent speed drops**: {len(anomalies)} statistically anomalous low-speed measurements detected"
        )

    if not indicators:
        indicators.append("✅ **No strong throttling signatures detected** in available data")

    return indicators


def generate_report(analysis: dict, days: int) -> str:
    now = datetime.now()
    summary = analysis.get("summary", {})
    by_endpoint = analysis.get("by_endpoint", {})
    peak = analysis.get("peak_vs_offpeak", {})
    trend = analysis.get("trend", {})
    by_hour = analysis.get("by_hour", {})
    anomalies = analysis.get("anomalies", [])
    cdn = analysis.get("cdn_discrimination", {})
    indicators = throttle_indicators(analysis)

    # Overall avg download
    dl_speeds = [v["avg_mbps"] for v in by_endpoint.values() if v["category"] != "upload" and v["avg_mbps"] > 0]
    overall_avg = round(sum(dl_speeds) / len(dl_speeds), 2) if dl_speeds else 0

    lines = [
        f"# ISP Speed & Throttling Evidence Report",
        f"",
        f"**Generated:** {now.strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**Period:** Last {days} days  ",
        f"**Total tests:** {summary.get('total_tests', '?')}  ",
        f"**Log file:** `{summary.get('log_file', '?')}`",
        f"",
        f"---",
        f"",
        f"## Executive Summary",
        f"",
        f"Overall average download speed: **{overall_avg} Mbps**",
    ]

    if cdn.get("upload_avg_mbps"):
        lines.append(f"Average upload speed: **{cdn['upload_avg_mbps']} Mbps**")

    lines += [
        f"",
        f"### Throttling Indicators",
        f"",
    ]
    for ind in indicators:
        lines.append(f"- {ind}")

    lines += [
        f"",
        f"---",
        f"",
        f"## Peak vs Off-Peak Comparison",
        f"",
        f"Peak hours are defined as: {peak.get('peak_hours', [])}",
        f"",
        peak_table(peak),
        f"",
        f"---",
        f"",
        f"## Per-Endpoint Analysis",
        f"",
        endpoint_table(by_endpoint),
    ]

    if cdn.get("cdn_vs_general_ratio") is not None:
        lines += [
            f"",
            f"**CDN vs General Internet ratio:** {round(cdn['cdn_vs_general_ratio'] * 100)}%",
            f"> A ratio below 75% suggests the ISP is selectively throttling CDN/streaming traffic.",
        ]

    lines += [
        f"",
        f"---",
        f"",
        f"## Speed by Hour of Day",
        f"",
        f"Average download speed for each hour (all endpoints combined):",
        f"",
        hour_chart(by_hour),
    ]

    # Hourly sparkline
    if by_hour:
        sorted_hours = sorted(by_hour.keys(), key=int)
        hour_speeds = [by_hour[h]["avg_mbps"] for h in sorted_hours]
        lines += [
            f"",
            f"Sparkline (00:00 → 23:00): `{spark_line(hour_speeds, 24)}`",
        ]

    lines += [
        f"",
        f"---",
        f"",
        f"## Trend Analysis",
        f"",
    ]
    if trend.get("status") == "insufficient_data":
        lines.append("_Insufficient data for trend analysis. Run more tests over multiple days._")
    else:
        lines += [
            f"- **Trend:** {trend.get('trend', 'unknown').title()}",
            f"- **Slope:** {trend.get('slope_mbps_per_day', '?')} Mbps/day",
            f"- **First week avg:** {trend.get('first_week_avg', '?')} Mbps",
            f"- **Last week avg:** {trend.get('last_week_avg', '?')} Mbps",
            f"- **Days sampled:** {trend.get('days_sampled', '?')} ({trend.get('first_day', '?')} to {trend.get('last_day', '?')})",
        ]

    if anomalies:
        lines += [
            f"",
            f"---",
            f"",
            f"## Anomalous Readings",
            f"",
            f"The following measurements were statistical outliers (> 2 standard deviations below mean):",
            f"",
            f"| Date | Hour | Endpoint | Speed | Mean Speed |",
            f"|------|------|----------|-------|------------|",
        ]
        for a in anomalies[:15]:
            lines.append(
                f"| {a['date']} | {a['hour']:02d}:00 | {a['endpoint']} | {a['speed_mbps']} Mbps | {a['mean_mbps']} Mbps |"
            )

    lines += [
        f"",
        f"---",
        f"",
        f"## Plain-English Conclusion",
        f"",
    ]

    # Build conclusion
    conclusion_parts = []
    diff = peak.get("difference_mbps")
    offpeak_avg = peak.get("off_peak", {}).get("avg_mbps", 0)

    if diff and offpeak_avg and diff / offpeak_avg > 0.20:
        conclusion_parts.append(
            f"Your internet speeds drop noticeably during peak evening hours — "
            f"by about {diff} Mbps on average. This is a classic congestion or throttling pattern."
        )
    else:
        conclusion_parts.append(
            f"Peak-hour performance is relatively consistent with off-peak performance, "
            f"which suggests your ISP is not heavily throttling based on time of day."
        )

    if cdn.get("cdn_throttling_suspected"):
        conclusion_parts.append(
            f"CDN and streaming traffic is significantly slower than general web traffic, "
            f"which is a strong indicator of protocol- or destination-based throttling. "
            f"This pattern is commonly used by ISPs to degrade streaming services."
        )

    if trend.get("trend") == "declining":
        conclusion_parts.append(
            f"Overall speeds have been declining over the measured period. "
            f"This warrants a conversation with your ISP about line quality or network congestion."
        )
    elif trend.get("trend") == "stable":
        conclusion_parts.append(
            f"Speed trends are stable — no long-term degradation detected."
        )

    conclusion_parts.append(
        f"**To use this report:** Share the Peak vs Off-Peak table and Per-Endpoint analysis "
        f"with your ISP's support team. Ask them to explain the discrepancy between peak and "
        f"off-peak speeds. If CDN throttling is suspected, reference the endpoint ratio data directly."
    )

    lines += [f"{p}" for p in conclusion_parts]
    lines += [
        f"",
        f"---",
        f"",
        f"_Report generated by isp-throttle-detective_",
    ]

    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    log_path = DEFAULT_LOG_FILE
    days = 30
    out_path = None

    i = 0
    while i < len(args):
        if args[i] == "--log" and i + 1 < len(args):
            log_path = os.path.expanduser(args[i + 1])
            i += 2
        elif args[i] == "--days" and i + 1 < len(args):
            days = int(args[i + 1])
            i += 2
        elif args[i] == "--out" and i + 1 < len(args):
            out_path = os.path.expanduser(args[i + 1])
            i += 2
        elif args[i] == "--config" and i + 1 < len(args):
            config_path = args[i + 1]
            if os.path.exists(config_path):
                with open(config_path) as f:
                    cfg = json.load(f)
                log_path = os.path.expanduser(cfg.get("log_file", log_path))
            i += 2
        else:
            i += 1

    try:
        analysis = run_analysis(log_path, days)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if "error" in analysis:
        print(f"Error: {analysis['error']}", file=sys.stderr)
        sys.exit(1)

    report = generate_report(analysis, days)

    if out_path:
        os.makedirs(os.path.dirname(out_path) if os.path.dirname(out_path) else ".", exist_ok=True)
        with open(out_path, "w") as f:
            f.write(report)
        print(f"Report written to: {out_path}", file=sys.stderr)
    else:
        # Default: save to reports dir and print path
        os.makedirs(DEFAULT_REPORT_DIR, exist_ok=True)
        filename = f"report-{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.md"
        out_path = os.path.join(DEFAULT_REPORT_DIR, filename)
        with open(out_path, "w") as f:
            f.write(report)
        print(f"Report saved to: {out_path}")
        print()
        print(report)


if __name__ == "__main__":
    main()
