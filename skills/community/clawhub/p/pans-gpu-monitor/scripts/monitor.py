#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pans-gpu-monitor: AI算力销售GPU监控工具
接入客户GPU使用数据，生成用量/效率周报，支持异常告警
"""

import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

# ── 路径配置 ────────────────────────────────────────────────────────────────
SKILL_DIR   = Path.home() / ".qclaw/skills/pans-gpu-monitor"
DATA_DIR    = SKILL_DIR  / "data"
DEFAULT_DB  = DATA_DIR   / "metrics.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)


# ── 数据模型 ─────────────────────────────────────────────────────────────────
def load_db(path: Path = DEFAULT_DB) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {"records": []}
    return {"records": []}


def save_db(db: dict, path: Path = DEFAULT_DB):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")


# ── 数据导入 ─────────────────────────────────────────────────────────────────
def import_csv(fp: Path, client: str = "unknown") -> int:
    """从CSV导入监控数据，返回导入记录数"""
    records = []
    with fp.open(encoding="utf-8-sig" if sys.platform == "darwin" else "utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                "client":        client,
                "timestamp":     row.get("timestamp", ""),
                "gpu_util":      float(row.get("gpu_utilization", 0)),
                "mem_util":      float(row.get("memory_utilization", 0)),
                "mem_used_gb":   float(row.get("memory_used_gb", 0)),
                "gpu_count":     int(row.get("gpu_count", 1)),
                "train_tasks":   int(row.get("training_tasks", 0)),
                "infer_tasks":   int(row.get("inference_tasks", 0)),
                "queue_time":    float(row.get("queue_time_minutes", 0)),
                "cost_per_token":float(row.get("cost_per_token", 0)),
                "tokens":        float(row.get("tokens_processed", 0)),
                "cost_usd":      float(row.get("cost_usd", 0)),
                "region":        row.get("region", ""),
                "gpu_type":      row.get("gpu_type", ""),
            })
    return records


def import_json(fp: Path, client: str = "unknown") -> list:
    """从JSON导入监控数据"""
    data = json.loads(fp.read_text(encoding="utf-8"))
    records = []
    items = data if isinstance(data, list) else data.get("records", [])
    for item in items:
        records.append({
            "client":         item.get("client", client),
            "timestamp":       item.get("timestamp", ""),
            "gpu_util":        float(item.get("gpu_utilization", item.get("gpu_util", 0))),
            "mem_util":        float(item.get("memory_utilization", item.get("mem_util", 0))),
            "mem_used_gb":     float(item.get("memory_used_gb", 0)),
            "gpu_count":       int(item.get("gpu_count", 1)),
            "train_tasks":     int(item.get("training_tasks", 0)),
            "infer_tasks":     int(item.get("inference_tasks", 0)),
            "queue_time":      float(item.get("queue_time_minutes", 0)),
            "cost_per_token": float(item.get("cost_per_token", 0)),
            "tokens":          float(item.get("tokens_processed", 0)),
            "cost_usd":        float(item.get("cost_usd", 0)),
            "region":          item.get("region", ""),
            "gpu_type":        item.get("gpu_type", ""),
        })
    return records


def cmd_import(args) -> int:
    """导入命令入口"""
    fp = Path(args.import_file)
    if not fp.exists():
        print(f"[ERROR] 文件不存在: {fp}", file=sys.stderr)
        return 1

    client = args.client or "default"
    ext = fp.suffix.lower()

    if ext == ".csv":
        records = import_csv(fp, client)
    elif ext == ".json":
        records = import_json(fp, client)
    else:
        print(f"[ERROR] 不支持的格式: {ext}，仅支持 CSV/JSON", file=sys.stderr)
        return 1

    if not records:
        print("[WARN] 未读取到任何记录")
        return 0

    db = load_db()
    db["records"].extend(records)
    save_db(db)
    print(f"[OK] 成功导入 {len(records)} 条记录（客户: {client}）")
    return 0


# ── 日期范围解析 ─────────────────────────────────────────────────────────────
def parse_date_range(s: str):
    """解析 YYYY-MM-DD,YYYY-MM-DD 格式或 'last7days' 等预设"""
    s = s.strip().lower()
    presets = {
        "last7days": (datetime.now() - timedelta(days=7), datetime.now()),
        "last30days": (datetime.now() - timedelta(days=30), datetime.now()),
        "lastweek": (
            datetime.now() - timedelta(weeks=1, days=datetime.now().weekday()),
            datetime.now() - timedelta(days=datetime.now().weekday()),
        ),
        "thismonth": (
            datetime.now().replace(day=1, hour=0, minute=0, second=0),
            datetime.now(),
        ),
    }
    if s in presets:
        return presets[s]

    parts = s.split(",")
    if len(parts) == 2:
        try:
            s1 = datetime.strptime(parts[0].strip(), "%Y-%m-%d")
            s2 = datetime.strptime(parts[1].strip(), "%Y-%m-%d")
            return s1, s2
        except ValueError:
            pass
    return None, None


def filter_by_date(records: list, start, end) -> list:
    if not start and not end:
        return records
    result = []
    for r in records:
        try:
            ts = datetime.fromisoformat(r["timestamp"].replace("Z", "+00:00"))
            if (not start or ts >= start) and (not end or ts <= end):
                result.append(r)
        except (ValueError, KeyError):
            pass
    return result


def filter_by_client(records: list, client: str) -> list:
    if not client:
        return records
    return [r for r in records if r.get("client") == client]


# ── 统计汇总 ─────────────────────────────────────────────────────────────────
def summarize(records: list) -> dict:
    if not records:
        return {}
    n = len(records)
    sum_util  = sum(r["gpu_util"] for r in records)
    sum_mem   = sum(r["mem_util"] for r in records)
    sum_queue = sum(r["queue_time"] for r in records)
    sum_cpt   = sum(r["cost_per_token"] for r in records if r["cost_per_token"] > 0)
    sum_cost  = sum(r["cost_usd"] for r in records)
    sum_tokens= sum(r["tokens"] for r in records)
    sum_train = sum(r["train_tasks"] for r in records)
    sum_infer = sum(r["infer_tasks"] for r in records)
    cpt_count = sum(1 for r in records if r["cost_per_token"] > 0)

    return {
        "count":         n,
        "gpu_util_avg":  round(sum_util  / n, 2),
        "gpu_util_max":  round(max(r["gpu_util"]  for r in records), 2),
        "gpu_util_min":  round(min(r["gpu_util"]  for r in records), 2),
        "mem_util_avg":  round(sum_mem   / n, 2),
        "mem_util_max":  round(max(r["mem_util"]  for r in records), 2),
        "queue_avg":     round(sum_queue / n, 2),
        "cost_per_token_avg": round(sum_cpt / cpt_count, 6) if cpt_count else 0,
        "total_cost":    round(sum_cost, 4),
        "total_tokens":  round(sum_tokens, 0),
        "train_tasks":   sum_train,
        "infer_tasks":   sum_infer,
        "total_tasks":   sum_train + sum_infer,
    }


def daily_breakdown(records: list) -> dict:
    by_day = defaultdict(list)
    for r in records:
        try:
            day = r["timestamp"][:10]
            by_day[day].append(r)
        except KeyError:
            continue
    return {d: summarize(recs) for d, recs in sorted(by_day.items())}


# ── 报告格式化 ─────────────────────────────────────────────────────────────────
def color_bar(val: float, max_val: float = 100, width: int = 20) -> str:
    filled = int(round(val / max_val * width))
    return "█" * filled + "░" * (width - filled)


def fmt_mini_chart(values: list, width: int = 40) -> str:
    if not values:
        return ""
    lo, hi = min(values), max(values)
    rng = hi - lo or 1
    bars = []
    for v in values:
        h = max(1, int(round((v - lo) / rng * (width - 1))) + 1)
        bars.append("▏" + "▄" * h)
    return "".join(bars)


def print_weekly_report(db: dict, args):
    client = args.client
    start, end = parse_date_range(args.date) if args.date else (datetime.now() - timedelta(days=7), datetime.now())
    records = filter_by_client(db["records"], client) if client else db["records"]
    records = filter_by_date(records, start, end)

    if not records:
        print("[WARN] 指定范围内无数据，使用示例数据生成报告")
        records = _sample_data(start, end, client or "demo")
        print()

    by_day  = daily_breakdown(records)
    summary = summarize(records)
    days    = sorted(by_day.keys())

    # ── 标题 ──
    client_tag = f"[{client}]" if client else "[全部客户]"
    s_str = start.strftime("%Y-%m-%d") if start else "最早"
    e_str = end.strftime("%Y-%m-%d")   if end   else "最晚"
    print(f"{'═' * 64}")
    print(f"  GPU 周报  {client_tag}  {s_str} → {e_str}")
    print(f"{'═' * 64}")
    print()

    # ── 1. 总体概览 ──
    print(f"  📊 总体概览")
    print(f"  ─────────────────────────────────────────────")
    print(f"  数据点数:       {summary.get('count', 0):>8}")
    print(f"  总训练任务:     {summary.get('train_tasks', 0):>8}")
    print(f"  总推理任务:     {summary.get('infer_tasks', 0):>8}")
    print(f"  总 Token 数:    {summary.get('total_tokens', 0):>12,.0f}")
    print(f"  总成本 (USD):   ${summary.get('total_cost', 0):>12.4f}")
    print(f"  $/Token 均值:   ${summary.get('cost_per_token_avg', 0):>12.6f}")
    print()

    # ── 2. GPU 利用率趋势 ──
    util_vals = [by_day[d]["gpu_util_avg"] for d in days]
    print(f"  🟢 GPU 利用率")
    print(f"  ─────────────────────────────────────────────")
    print(f"  平均: {summary.get('gpu_util_avg',0):.1f}%   "
          f"最高: {summary.get('gpu_util_max',0):.1f}%   "
          f"最低: {summary.get('gpu_util_min',0):.1f}%")
    if util_vals:
        print(f"  趋势: {fmt_mini_chart(util_vals)}")
        for d in days:
            b = color_bar(by_day[d]["gpu_util_avg"])
            print(f"    {d}  {b}  {by_day[d]['gpu_util_avg']:.1f}%")
    print()

    # ── 3. 显存使用 ──
    mem_vals = [by_day[d]["mem_util_avg"] for d in days]
    print(f"  🔵 显存使用率")
    print(f"  ─────────────────────────────────────────────")
    print(f"  平均: {summary.get('mem_util_avg',0):.1f}%   "
          f"峰值: {summary.get('mem_util_max',0):.1f}%")
    if mem_vals:
        print(f"  趋势: {fmt_mini_chart(mem_vals)}")
        for d in days:
            b = color_bar(by_day[d]["mem_util_avg"])
            print(f"    {d}  {b}  {by_day[d]['mem_util_avg']:.1f}%")
    print()

    # ── 4. 任务排队时间 ──
    queue_vals = [by_day[d]["queue_avg"] for d in days]
    print(f"  ⏳ 平均排队时间 (分钟)")
    print(f"  ─────────────────────────────────────────────")
    avg_q = summary.get("queue_avg", 0)
    print(f"  周均值: {avg_q:.1f} min")
    if queue_vals:
        print(f"  趋势: {fmt_mini_chart(queue_vals)}")
        for d in days:
            q = by_day[d]["queue_avg"]
            flag = "⚠" if q > 60 else ("🔶" if q > 30 else "")
            print(f"    {d}  {q:6.1f} min  {flag}")
    print()

    # ── 5. 优化建议 ──
    suggestions = _generate_suggestions(summary)
    print(f"  💡 优化建议")
    print(f"  ─────────────────────────────────────────────")
    for i, s in enumerate(suggestions, 1):
        print(f"  {i}. {s}")
    print()
    print(f"{'═' * 64}")


def print_monthly_report(db: dict, args):
    client = args.client
    start  = datetime.now().replace(day=1, hour=0, minute=0, second=0)
    end    = datetime.now()
    if args.date:
        s2, e2 = parse_date_range(args.date)
        if s2: start = s2
        if e2: end   = e2

    records = filter_by_client(db["records"], client) if client else db["records"]
    records = filter_by_date(records, start, end)

    if not records:
        print("[WARN] 指定范围内无数据，使用示例数据生成报告")
        records = _sample_data(start, end, client or "demo")
        print()

    by_week = _weekly_breakdown(records)
    summary = summarize(records)

    print(f"{'═' * 64}")
    print(f"  GPU 月报  {f'[{client}]' if client else '[全部客户]'}")
    print(f"{'═' * 64}")
    print()

    # ── 月度成本总览 ──
    print(f"  💰 月度成本分析")
    print(f"  ─────────────────────────────────────────────")
    print(f"  总成本:        ${summary.get('total_cost', 0):>12.4f}")
    print(f"  总 Token:      {summary.get('total_tokens', 0):>14,.0f}")
    print(f"  $/Token 均值:  ${summary.get('cost_per_token_avg', 0):>12.6f}")
    print(f"  总任务数:      {summary.get('total_tasks', 0):>12}")
    print()

    # ── 周度趋势 ──
    print(f"  📅 周度用量趋势")
    print(f"  ───────────────────────────────────────────────────────────")
    print(f"  {'周次':<12} {'GPU利用率':>10} {'显存':>8} {'排队(min)':>12} {'成本($)':>10}")
    print(f"  {'─'*12} {'─'*10} {'─'*8} {'─'*12} {'─'*10}")
    for week, s in by_week.items():
        print(f"  {week:<12} {s['gpu_util_avg']:>9.1f}% {s['mem_util_avg']:>7.1f}% "
              f"{s['queue_avg']:>11.1f} ${s['total_cost']:>9.4f}")
    print()

    # ── 容量规划建议 ──
    cap_plan = _capacity_planning(summary)
    print(f"  📐 容量规划建议")
    print(f"  ─────────────────────────────────────────────")
    for line in cap_plan:
        print(f"  {line}")
    print()
    print(f"{'═' * 64}")


def _weekly_breakdown(records: list) -> dict:
    by_week = defaultdict(list)
    for r in records:
        try:
            dt = datetime.fromisoformat(r["timestamp"].replace("Z", "+00:00"))
            week = dt.strftime("%Y-W%W")
            by_week[week].append(r)
        except (ValueError, KeyError):
            continue
    return {w: summarize(recs) for w, recs in sorted(by_week.items())}


def _generate_suggestions(summary: dict) -> list:
    suggestions = []
    util = summary.get("gpu_util_avg", 0)
    mem  = summary.get("mem_util_avg", 0)
    queue= summary.get("queue_avg", 0)
    cpt  = summary.get("cost_per_token_avg", 0)

    if util < 40:
        suggestions.append(f"GPU 利用率均值仅 {util:.1f}%，存在大量闲置资源，建议合并任务或缩减 GPU 数量以降低成本")
    elif util > 90:
        suggestions.append(f"GPU 利用率均值高达 {util:.1f}%，接近饱和，建议扩容或优化任务分配策略")
    if mem > 90:
        suggestions.append(f"显存使用率峰值 {mem:.1f}%，建议升级至更大显存 GPU（A100 80G/H100）以避免 OOM")
    if mem < 30:
        suggestions.append(f"显存平均使用率仅 {mem:.1f}%，存在显存浪费，建议评估 batch_size 配置")
    if queue > 60:
        suggestions.append(f"平均排队时间 {queue:.1f} 分钟，严重影响效率，建议增加 GPU 实例数量")
    elif queue > 30:
        suggestions.append(f"平均排队时间 {queue:.1f} 分钟，建议适当扩容或优化任务调度")
    if cpt > 0.01:
        suggestions.append(f"$/Token = ${cpt:.6f}，成本偏高，建议评估模型量化方案或选择更优实例类型")
    if summary.get("total_tasks", 0) == 0:
        suggestions.append("当前无任务记录，请确认数据导入是否成功")
    if not suggestions:
        suggestions.append("各项指标正常，继续保持当前配置")
    return suggestions


def _capacity_planning(summary: dict) -> list:
    lines = []
    util = summary.get("gpu_util_avg", 0)
    mem  = summary.get("mem_util_avg", 0)
    tasks= summary.get("total_tasks", 0)
    cost = summary.get("total_cost", 0)

    lines.append(f"• 当前月成本: ${cost:.2f}")
    if util > 80:
        lines.append(f"• 利用率 {util:.1f}% 持续偏高，建议扩容 20-30% GPU 资源")
        lines.append(f"• 参考扩容方案: 增加 2-4 张 A100 80G 或切换至高配实例")
    elif util < 50:
        lines.append(f"• 利用率 {util:.1f}% 偏低，建议缩减 10-20% GPU 资源以节省成本")
    if mem > 85:
        lines.append(f"• 显存紧张，建议关注大模型训练场景，预留更多显存预算")
    if tasks > 0 and cost > 0:
        est = cost / tasks
        lines.append(f"• 单任务平均成本: ${est:.4f}（含 GPU + 存储 + 网络）")
    return lines


# ── 异常告警 ─────────────────────────────────────────────────────────────────
def check_alerts(db: dict, args):
    client = args.client
    start, end = parse_date_range(args.date) if args.date else (datetime.now() - timedelta(days=7), datetime.now())
    records = filter_by_client(db["records"], client) if client else db["records"]
    records = filter_by_date(records, start, end)

    if not records:
        print("[INFO] 指定范围内无数据，生成示例告警演示")
        records = _sample_data(start, end, client or "demo")

    alerts = []
    # 按天/条记录检查异常
    for r in records:
        tag = []
        if r["gpu_util"] < 15:
            tag.append(f"【严重】GPU 利用率过低 ({r['gpu_util']:.1f}%)，资源严重闲置")
        elif r["gpu_util"] > 95:
            tag.append(f"【警告】GPU 利用率过高 ({r['gpu_util']:.1f}%)，存在过热/排队风险")
        if r["mem_util"] > 98:
            tag.append(f"【严重】显存接近 100% ({r['mem_util']:.1f}%)，即将 OOM")
        if r["queue_time"] > 120:
            tag.append(f"【严重】排队时间过长 ({r['queue_time']:.0f} min)，严重影响交付")
        if r["cost_per_token"] > 0.05:
            tag.append(f"【警告】$/Token 异常偏高 (${r['cost_per_token']:.6f})，需排查")
        if tag:
            alerts.append((r, tag))

    print(f"{'═' * 64}")
    print(f"  🔔 GPU 异常告警报告")
    print(f"  客户: {client or '全部'}  范围: {start.strftime('%Y-%m-%d') if start else '最早'} → {end.strftime('%Y-%m-%d') if end else '最晚'}")
    print(f"{'═' * 64}")
    print()

    if not alerts:
        print("  ✅ 未检测到明显异常，各项指标在正常范围内")
    else:
        print(f"  检测到 {len(alerts)} 条异常记录:")
        print()
        for r, tags in alerts[:20]:
            ts = r.get("timestamp", "?")[:19]
            c  = r.get("client", "?")
            print(f"  [{ts}] {c}")
            for t in tags:
                print(f"    ⚠  {t}")
            print()

    # 汇总统计告警
    summary = summarize(records)
    print(f"  📊 告警统计（整体）")
    print(f"  ─────────────────────────────────────────────")
    print(f"  GPU 利用率均值:  {summary.get('gpu_util_avg',0):.1f}%  "
          f"{'⚠ 过低' if summary.get('gpu_util_avg',0) < 30 else '⚠ 过高' if summary.get('gpu_util_avg',0) > 90 else '✅ 正常'}")
    print(f"  显存均值:        {summary.get('mem_util_avg',0):.1f}%  "
          f"{'⚠ 接近饱和' if summary.get('mem_util_avg',0) > 90 else '✅ 正常'}")
    print(f"  排队时间均值:    {summary.get('queue_avg',0):.1f} min  "
          f"{'⚠ 过长' if summary.get('queue_avg',0) > 60 else '✅ 正常'}")
    print()
    print(f"{'═' * 64}")


# ── 示例数据生成 ─────────────────────────────────────────────────────────────
def _sample_data(start, end, client: str) -> list:
    import random
    records = []
    cur = (start or datetime.now() - timedelta(days=7))
    delta = (end or datetime.now()) - cur
    steps = max(1, delta.days)
    for i in range(steps):
        day = cur + timedelta(days=i)
        for h in [9, 12, 15, 18, 21]:
            ts = day.replace(hour=h, minute=0, second=0).isoformat()
            records.append({
                "client":         client,
                "timestamp":      ts,
                "gpu_util":        round(random.uniform(35, 92), 1),
                "mem_util":        round(random.uniform(55, 97), 1),
                "mem_used_gb":     round(random.uniform(40, 80), 1),
                "gpu_count":       random.choice([1, 2, 4, 8]),
                "train_tasks":     random.randint(0, 3),
                "infer_tasks":     random.randint(5, 20),
                "queue_time":      round(random.uniform(5, 80), 1),
                "cost_per_token":  round(random.uniform(0.001, 0.008), 6),
                "tokens":          round(random.uniform(1e6, 5e7), 0),
                "cost_usd":        round(random.uniform(10, 500), 4),
                "region":          random.choice(["cn-bj", "cn-sh", "us-west"]),
                "gpu_type":        random.choice(["A100", "A100", "H100", "L40S"]),
            })
    return records


# ── CLI 入口 ─────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        prog="pans-gpu-monitor",
        description="AI算力销售 GPU 监控工具 — 用量/效率报告 & 异常告警",
    )
    parser.add_argument("--import", dest="import_file", metavar="FILE",
                        help="导入监控数据文件（CSV 或 JSON）")
    parser.add_argument("--weekly", action="store_true",
                        help="生成周报")
    parser.add_argument("--monthly", action="store_true",
                        help="生成月报")
    parser.add_argument("--alert", action="store_true",
                        help="检查异常并输出告警")
    parser.add_argument("--client", metavar="NAME",
                        help="指定客户名称筛选")
    parser.add_argument("--date", metavar="RANGE",
                        help="日期范围: YYYY-MM-DD,YYYY-MM-DD 或 last7days/thismonth")
    parser.add_argument("--db", metavar="PATH",
                        help=f"数据文件路径（默认: {DEFAULT_DB}）")

    args = parser.parse_args()
    db_path = Path(args.db) if args.db else DEFAULT_DB

    # 无任何报告参数时默认输出帮助
    if not any([args.import_file, args.weekly, args.monthly, args.alert]):
        parser.print_help()
        return 0

    if args.import_file:
        return cmd_import(args)

    db = load_db(db_path)

    if args.weekly:
        print_weekly_report(db, args)
    elif args.monthly:
        print_monthly_report(db, args)
    elif args.alert:
        check_alerts(db, args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
