#!/usr/bin/env python3
"""
柳比歇夫日报生成脚本

省token设计：
- 脚本负责：读取记录、计算统计、拼接全文、写入日报表
- 大模型只负责：写2-4句「能量洞察」

用法：
  python3 daily_report.py --date 2026-04-21 \
    --base-token YOUR_BASE_TOKEN \
    --records-table YOUR_RECORDS_TABLE_ID \
    --daily-table YOUR_DAILY_TABLE_ID \
    [--insight "能量洞察文本"] [--dry-run] \
    [--recorder YOUR_NAME] [--recorder-id YOUR_OPEN_ID]

前置条件：
  1. 安装 lark-cli 并完成 auth login
  2. 在飞书创建两个多维表格（记录表 + 日报表），字段结构见 SKILL.md

流程：
  1. 从飞书读取当天所有记录
  2. 计算统计数据（时长、占比、Top3、增量复利）
  3. 拼接日报全文模板
  4. 写入飞书日报表

如果不传 --insight，能量洞察字段留空，等大模型补填。
如果传 --dry-run，只打印结果不写入飞书。
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from collections import defaultdict

# ========== 配置（可通过命令行参数覆盖）==========
# 默认值留空，必须通过命令行 --base-token / --records-table / --daily-table 传入
BASE_TOKEN = ""
RECORDS_TABLE_ID = ""
DAILY_TABLE_ID = ""
CST = timezone(timedelta(hours=8))

# 日报表字段名→字段ID映射（运行时自动从飞书API获取）
DAILY_FIELDS = {}

# 记录表字段名→字段ID映射（运行时自动从飞书API获取）
RECORD_FIELDS = {}

SIX_CATEGORIES = ["睡觉", "日常", "输入", "输出", "关系", "回血"]

WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def run_lark_cli(args: list[str]) -> dict:
    """调用 lark-cli 并返回 JSON 结果"""
    cmd = ["lark-cli", "base"] + args + ["--as", "user"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ lark-cli 错误: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def fetch_field_map(table_id: str) -> dict:
    """从飞书API获取字段名→字段ID的映射"""
    data = run_lark_cli([
        "+field-list",
        "--base-token", BASE_TOKEN,
        "--table-id", table_id,
    ])
    fields = data["data"]["fields"]
    return {f["name"]: f["id"] for f in fields}


def fetch_records(date_str: str) -> list[dict]:
    """从飞书读取指定日期的所有记录"""
    # 计算日期的毫秒时间戳
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=CST)
    date_ts = int(date_obj.timestamp() * 1000)

    data = run_lark_cli([
        "+record-list",
        "--base-token", BASE_TOKEN,
        "--table-id", RECORDS_TABLE_ID,
        "--limit", "200",
    ])

    fields = data["data"]["fields"]
    records_raw = data["data"]["data"]
    field_names = {i: n for i, n in enumerate(fields)}

    records = []
    for raw in records_raw:
        row = {}
        for i, val in enumerate(raw):
            name = field_names.get(i, f"field_{i}")
            row[name] = val
        # 只取目标日期的记录
        rec_date = str(row.get("记录日期", ""))[:10]
        if rec_date == date_str:
            records.append(row)

    return records


def parse_category(val) -> str:
    """解析类别字段（可能是列表或字符串）"""
    if isinstance(val, list):
        return val[0] if val else ""
    return str(val) if val else ""


def parse_minutes(val) -> float:
    """解析时长（分钟）"""
    if val is None:
        return 0
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0


def parse_side_duration(val) -> float:
    """解析附带时长（分钟），数字字段直接读取"""
    if not val:
        return 0
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0


def compute_stats(records: list[dict]) -> dict:
    """计算日报所有统计数据"""
    # 各类别时长（分钟）
    category_minutes = defaultdict(float)
    # Tag时长汇总（分钟）
    tag_minutes = defaultdict(float)
    # 增量复利（附带时长）
    side_total = 0.0
    side_details = []

    for rec in records:
        main_cat = parse_category(rec.get("主类别", ""))
        main_min = parse_minutes(rec.get("时长（分钟）", 0))
        main_tag = str(rec.get("主Tag", "")).strip()

        # 主活动
        if main_cat in SIX_CATEGORIES:
            category_minutes[main_cat] += main_min
        if main_tag:
            tag_minutes[main_tag] += main_min

        # 附带活动
        side_cat = parse_category(rec.get("附带类别", ""))
        side_tag = str(rec.get("附带Tag", "")).strip()
        side_dur = parse_side_duration(rec.get("附带时长（分钟）", ""))

        if side_dur > 0 and side_tag:
            # 附带时长加到对应类别
            if side_cat in SIX_CATEGORIES:
                category_minutes[side_cat] += side_dur
            tag_minutes[side_tag] += side_dur
            side_total += side_dur
            side_details.append(f"{side_tag} {side_dur:.0f}min")

    # 总追踪时长
    tracked_total = sum(category_minutes.values())
    # 黑洞时长（24小时 - 追踪）
    blackhole = 1440 - tracked_total
    blackhole_pct = round(blackhole / 1440 * 100, 1) if tracked_total > 0 else 100.0

    # 各类别占比（占追踪总时长）
    category_pct = {}
    for cat in SIX_CATEGORIES:
        mins = category_minutes.get(cat, 0)
        pct = round(mins / tracked_total * 100, 1) if tracked_total > 0 else 0
        category_pct[cat] = pct

    # Top3 Tag（排除睡觉类别的Tag）
    sleep_tags = set()
    for rec in records:
        main_cat = parse_category(rec.get("主类别", ""))
        main_tag = str(rec.get("主Tag", "")).strip()
        if main_cat == "睡觉" and main_tag:
            sleep_tags.add(main_tag)
        side_cat = parse_category(rec.get("附带类别", ""))
        side_tag = str(rec.get("附带Tag", "")).strip()
        if side_cat == "睡觉" and side_tag:
            sleep_tags.add(side_tag)

    non_sleep_tags = {k: v for k, v in tag_minutes.items() if k not in sleep_tags}
    sorted_tags = sorted(non_sleep_tags.items(), key=lambda x: x[1], reverse=True)
    top3 = sorted_tags[:3]

    return {
        "tracked_hours": round(tracked_total / 60, 1),
        "blackhole_hours": round(blackhole / 60, 1),
        "blackhole_pct": blackhole_pct,
        "category_minutes": dict(category_minutes),
        "category_hours": {k: round(v / 60, 1) for k, v in category_minutes.items()},
        "category_pct": category_pct,
        "top3": [(tag, round(mins / 60, 1)) for tag, mins in top3],
        "side_hours": round(side_total / 60, 1),
        "side_details": side_details,
    }


def build_report_text(date_str: str, stats: dict, insight: str = "") -> str:
    """拼接日报全文"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    weekday = WEEKDAYS[date_obj.weekday()]

    lines = []
    lines.append(f"📊 {date_str} {weekday} 时间日报")
    lines.append("")
    lines.append("**1. 物理时间大盘**")

    bh_warning = ""
    if stats["blackhole_pct"] > 15:
        bh_warning = " ⚠️ 黑洞时间偏高"

    lines.append(
        f"追踪：{stats['tracked_hours']}h | 黑洞：{stats['blackhole_hours']}h"
        f"（{stats['blackhole_pct']}%）{bh_warning}"
    )

    # 七大项（黑洞+6大类）：时长+百分比+文本进度条
    # 黑洞
    bh_pct = stats["blackhole_pct"]
    bh_bar_len = int(round(bh_pct / 5))
    bh_bar = "█" * bh_bar_len + "░" * (20 - bh_bar_len)
    lines.append(f"  黑洞  {stats['blackhole_hours']}h  {bh_pct}%  {bh_bar}")

    # 六大类
    for cat in SIX_CATEGORIES:
        hours = stats['category_hours'].get(cat, 0)
        pct = stats['category_pct'].get(cat, 0)
        bar_len = int(round(pct / 5))  # 0-20格，5%一格
        bar = "█" * bar_len + "░" * (20 - bar_len)
        lines.append(f"  {cat}  {hours}h  {pct}%  {bar}")

    lines.append("")
    lines.append("**2. 增量复利清算**")
    if stats["side_hours"] > 0:
        detail_str = " · ".join(stats["side_details"])
        lines.append(f"今日通过并行额外获得 {stats['side_hours']}h：{detail_str}")
    else:
        lines.append("今日无并行增量")

    lines.append("")
    lines.append("**3. 核心资产 Top3**")
    medals = ["🥇", "🥈", "🥉"]
    for i, (tag, hours) in enumerate(stats["top3"]):
        lines.append(f"{medals[i]} {tag} {hours}h")
    if len(stats["top3"]) < 3:
        for i in range(len(stats["top3"]), 3):
            lines.append(f"{medals[i]} —")

    lines.append("")
    lines.append("**4. 能量洞察**")
    if insight:
        lines.append(insight)
    else:
        lines.append("（待AI补填）")

    return "\n".join(lines)


def write_daily_report(date_str: str, stats: dict, report_text: str, insight: str = "", dry_run: bool = False, recorder: str = "", recorder_id: str = ""):
    """写入飞书日报表"""
    # 构造日期时间戳
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=CST)
    date_ts = int(date_obj.timestamp() * 1000)

    # 构造JSON
    record = {
        DAILY_FIELDS["日期"]: date_ts,
        DAILY_FIELDS["追踪总时长"]: stats["tracked_hours"],
        DAILY_FIELDS["黑洞时长"]: stats["blackhole_hours"],
        DAILY_FIELDS["黑洞占比"]: stats["blackhole_pct"],
    }

    # 写入记录人（user类型需要 [{"id": "ou_xxx"}] 格式）
    if recorder_id and "记录人" in DAILY_FIELDS:
        record[DAILY_FIELDS["记录人"]] = [{"id": recorder_id}]

    for cat in SIX_CATEGORIES:
        record[DAILY_FIELDS[f"{cat}时长"]] = stats["category_hours"].get(cat, 0)
        record[DAILY_FIELDS[f"{cat}占比"]] = stats["category_pct"].get(cat, 0)

    for i, (tag, hours) in enumerate(stats["top3"]):
        if i < 3:
            record[DAILY_FIELDS[f"Top{i+1}资产"]] = f"{tag} {hours}h"

    record[DAILY_FIELDS["增量复利"]] = stats["side_hours"]
    record[DAILY_FIELDS["增量复利明细"]] = " · ".join(stats["side_details"]) if stats["side_details"] else ""
    record[DAILY_FIELDS["能量洞察"]] = insight if insight else ""
    record[DAILY_FIELDS["日报全文"]] = report_text

    if dry_run:
        print("\n========== DRY RUN ==========")
        print(f"日期: {date_str}")
        print(f"追踪: {stats['tracked_hours']}h | 黑洞: {stats['blackhole_hours']}h ({stats['blackhole_pct']}%)")
        for cat in ["黑洞"] + SIX_CATEGORIES:
            if cat == "黑洞":
                print(f"  {cat}: {stats['blackhole_hours']}h ({stats['blackhole_pct']}%)")
            else:
                print(f"  {cat}: {stats['category_hours'].get(cat, 0)}h ({stats['category_pct'].get(cat, 0)}%)")
        for i, (tag, hours) in enumerate(stats["top3"]):
            print(f"  Top{i+1}: {tag} {hours}h")
        print(f"增量复利: {stats['side_hours']}h")
        print("\n--- 日报全文 ---")
        print(report_text)
        print("==============================")
        return

    # 写入飞书
    result = run_lark_cli([
        "+record-upsert",
        "--base-token", BASE_TOKEN,
        "--table-id", DAILY_TABLE_ID,
        "--json", json.dumps(record, ensure_ascii=False),
    ])

    if result.get("ok"):
        print(f"✅ 日报已写入飞书: {date_str}")
    else:
        print(f"❌ 写入失败: {result}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="柳比歇夫日报生成脚本")
    parser.add_argument("--date", required=True, help="日期 YYYY-MM-DD")
    parser.add_argument("--base-token", default="", help="飞书多维表格 Base Token")
    parser.add_argument("--records-table", default="", help="记录表 Table ID")
    parser.add_argument("--daily-table", default="", help="日报表 Table ID")
    parser.add_argument("--insight", default="", help="能量洞察文本（AI生成）")
    parser.add_argument("--dry-run", action="store_true", help="只打印不写入")
    parser.add_argument("--recorder", default="", help="记录人姓名（用于显示）")
    parser.add_argument("--recorder-id", default="", help="记录人open_id（飞书user类型字段必填，格式：ou_xxx）")
    args = parser.parse_args()

    # 覆盖全局配置
    global BASE_TOKEN, RECORDS_TABLE_ID, DAILY_TABLE_ID
    if args.base_token:
        BASE_TOKEN = args.base_token
    if args.records_table:
        RECORDS_TABLE_ID = args.records_table
    if args.daily_table:
        DAILY_TABLE_ID = args.daily_table

    if not BASE_TOKEN or not RECORDS_TABLE_ID or not DAILY_TABLE_ID:
        print("❌ 缺少必要参数：--base-token, --records-table, --daily-table", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    print(f"📅 正在生成 {args.date} 的日报...")

    # Step 0: 自动获取字段ID映射
    global DAILY_FIELDS, RECORD_FIELDS
    print("📋 正在获取字段映射...")
    DAILY_FIELDS = fetch_field_map(DAILY_TABLE_ID)
    RECORD_FIELDS = fetch_field_map(RECORDS_TABLE_ID)
    print(f"  日报表字段: {len(DAILY_FIELDS)} 个, 记录表字段: {len(RECORD_FIELDS)} 个")

    # Step 1: 读取记录
    records = fetch_records(args.date)
    print(f"📋 读取到 {len(records)} 条记录")

    if not records:
        print(f"⚠️ {args.date} 无记录，跳过")
        return

    # Step 2: 计算统计
    stats = compute_stats(records)

    # Step 3: 拼接全文
    report_text = build_report_text(args.date, stats, args.insight)

    # Step 4: 写入日报表
    write_daily_report(args.date, stats, report_text, args.insight, args.dry_run, args.recorder, args.recorder_id)


if __name__ == "__main__":
    main()
