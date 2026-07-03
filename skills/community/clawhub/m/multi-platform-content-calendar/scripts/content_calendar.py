#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多平台内容日历
自动规划内容排期，关联节假日，追踪发布效果，生成周/月报告
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import calendar

# ============ 平台配置 ============

PLATFORMS = {
    "douyin": {
        "name": "抖音",
        "peak_times": ["12:00", "18:00", "21:00"],
        "best_types": ["故事类", "教程类", "生活类"],
        "color": "🎬",
    },
    "xhs": {
        "name": "小红书",
        "peak_times": ["08:00", "12:00", "20:00"],
        "best_types": ["种草类", "干货类", "测评类"],
        "color": "📕",
    },
    "bilibili": {
        "name": "B站",
        "peak_times": ["18:00", "22:00"],
        "best_types": ["测评类", "教程类", "故事类"],
        "color": "📺",
    },
    "wechat": {
        "name": "公众号",
        "peak_times": ["08:00", "12:00", "20:00"],
        "best_types": ["干货类", "故事类", "案例类"],
        "color": "💬",
    },
}

# ============ 节假日数据库 ============

HOLIDAYS_2026 = {
    "2026-01-01": "元旦",
    "2026-02-14": "情人节",
    "2026-03-08": "妇女节",
    "2026-04-01": "愚人节",
    "2026-05-01": "劳动节",
    "2026-05-04": "青年节",
    "2026-06-01": "儿童节",
    "2026-06-18": "618大促",
    "2026-07-01": "建党节",
    "2026-08-01": "建军节",
    "2026-09-10": "教师节",
    "2026-10-01": "国庆节",
    "2026-11-11": "双11",
    "2026-12-12": "双12",
    "2026-12-25": "圣诞节",
}

# ============ 内容主题推荐 ============

THEMES = [
    "AI工具测评",
    "职场效率技巧",
    "副业赚钱案例",
    "自媒体运营",
    "热点解读",
    "教程干货",
    "故事分享",
    "生活vlog",
]


# ============ 核心功能 ============

def get_week_dates(year, week):
    """获取某年的某一周的所有日期"""
    first_day = datetime.strptime(f"{year}-W{week}-1", "%Y-W%W-%w")
    dates = [first_day + timedelta(days=i) for i in range(7)]
    return dates


def get_holiday(date_str):
    """检查日期是否是节假日"""
    return HOLIDAYS_2026.get(date_str)


def generate_weekly_plan(year, week, platforms):
    """生成周计划"""
    dates = get_week_dates(year, week)
    
    plan = []
    content_id = 1
    
    for date in dates:
        date_str = date.strftime("%Y-%m-%d")
        weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date.weekday()]
        holiday = get_holiday(date_str)
        
        # 为每个平台生成内容
        for i, platform in enumerate(platforms):
            cfg = PLATFORMS[platform]
            
            # 智能推荐发布时间（轮流使用流量高峰）
            time_idx = content_id % len(cfg["peak_times"])
            publish_time = cfg["peak_times"][time_idx]
            
            # 推荐内容类型（轮流）
            type_idx = content_id % len(cfg["best_types"])
            content_type = cfg["best_types"][type_idx]
            
            # 推荐主题（轮流）
            theme_idx = content_id % len(THEMES)
            theme = THEMES[theme_idx]
            
            # 如果是节假日，主题改为节假日相关
            if holiday:
                theme = f"{holiday}特辑"
            
            plan.append({
                "id": f"{content_id:03d}",
                "date": date_str,
                "weekday": weekday,
                "holiday": holiday,
                "platform": platform,
                "platform_name": cfg["name"],
                "theme": theme,
                "type": content_type,
                "time": publish_time,
                "status": "待写",
                "emoji": cfg["color"],
            })
            
            content_id += 1
    
    return plan


def format_weekly_plan_markdown(year, week, plan):
    """格式化周计划为Markdown"""
    md = f"""# 内容日历 - {year}年第{week}周

生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 本周重点

"""
    
    # 提取节假日
    holidays = [item for item in plan if item["holiday"]]
    if holidays:
        md += "### 节假日联动\n"
        for h in holidays:
            md += f"- {h['date']} {h['weekday']}：{h['holiday']}\n"
    
    md += "\n---\n\n## 排期表\n\n"
    md += "| 日期 | 平台 | 内容主题 | 类型 | 发布时间 | 状态 |\n"
    md += "|------|------|----------|------|----------|------|\n"
    
    for item in plan:
        md += f"| {item['date']} {item['weekday']} | {item['emoji']} {item['platform_name']} | {item['theme']} | {item['type']} | {item['time']} | 📝 {item['status']} |\n"
    
    md += "\n---\n\n## 平台发布建议\n\n"
    
    # 按平台分组统计
    for platform in set(item["platform"] for item in plan):
        cfg = PLATFORMS[platform]
        platform_items = [item for item in plan if item["platform"] == platform]
        
        md += f"""### {cfg['color']} {cfg['name']}

- 最佳时间：{', '.join(cfg['peak_times'])}
- 内容类型：{', '.join(cfg['best_types'])}
- 本周计划：发布{len(platform_items)}条

"""
    
    md += f"""---

## 本周目标

- 全平台发布：{len(plan)}条
- 目标涨粉：1000+
- 目标互动：5000+

---

*生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    
    return md


def add_content_entry(title, platform, date, time_str, calendar_file):
    """添加内容条目"""
    if not Path(calendar_file).exists():
        data = {"entries": []}
    else:
        data = json.loads(Path(calendar_file).read_text(encoding="utf-8"))
    
    entry = {
        "id": f"{len(data['entries']) + 1:03d}",
        "title": title,
        "platform": platform,
        "date": date,
        "time": time_str,
        "status": "待发布",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    data["entries"].append(entry)
    Path(calendar_file).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"✅ 已添加内容：{title}（{platform}，{date} {time_str}）")
    return entry["id"]


def track_performance(content_id, likes, comments, shares, performance_file):
    """追踪发布效果"""
    if not Path(performance_file).exists():
        data = {"performances": []}
    else:
        data = json.loads(Path(performance_file).read_text(encoding="utf-8"))
    
    perf = {
        "id": content_id,
        "likes": likes,
        "comments": comments,
        "shares": shares,
        "total_interactions": likes + comments + shares,
        "tracked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    data["performances"].append(perf)
    Path(performance_file).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"✅ 已追踪效果：ID={content_id}，总互动={perf['total_interactions']}")


def generate_monthly_review(year, month, performance_file):
    """生成月度复盘报告"""
    try:
        data = json.loads(Path(performance_file).read_text(encoding="utf-8"))
    except:
        data = {"performances": []}
    
    # 筛选当月数据
    month_str = f"{year}-{month:02d}"
    month_data = [p for p in data["performances"] if p["tracked_at"].startswith(month_str)]
    
    total_interactions = sum(p["total_interactions"] for p in month_data)
    avg_interactions = total_interactions / len(month_data) if month_data else 0
    
    md = f"""# {year}年{month}月内容复盘报告

生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 发布统计

- 发布条数：{len(month_data)}条
- 总互动量：{total_interactions:,}
- 平均互动：{avg_interactions:.0f}

## 互动数据明细

| 内容ID | 点赞 | 评论 | 转发 | 总互动 |
|--------|------|------|------|--------|
"""
    
    for p in month_data[:10]:  # 只显示前10条
        md += f"| {p['id']} | {p['likes']} | {p['comments']} | {p['shares']} | {p['total_interactions']} |\n"
    
    md += f"""
---

## 改进建议

1. ✅ 继续保持高互动内容类型
2. ✅ 优化发布时间，集中在流量高峰
3. ⚠️ 分析低互动内容，调整策略

---

*生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    
    return md


# ============ 主程序 ============

def main():
    parser = argparse.ArgumentParser(description="多平台内容日历")
    parser.add_argument("--action", "-a", type=str, required=True,
                        choices=["plan", "add", "track", "review"], help="操作类型")
    parser.add_argument("--week", "-w", type=str, help="周次（格式：2026-W27）")
    parser.add_argument("--month", "-m", type=str, help="月份（格式：2026-06）")
    parser.add_argument("--platforms", "-p", type=str, default="douyin,xhs,bilibili",
                        help="平台列表（逗号分隔）")
    parser.add_argument("--title", "-t", type=str, help="内容标题（add时必填）")
    parser.add_argument("--platform", "-P", type=str, help="单个平台（add时必填）")
    parser.add_argument("--date", "-d", type=str, help="发布日期（add时必填）")
    parser.add_argument("--time", "-T", type=str, help="发布时间（add时必填）")
    parser.add_argument("--id", "-i", type=str, help="内容ID（track时必填）")
    parser.add_argument("--likes", "-l", type=int, help="点赞数（track时必填）")
    parser.add_argument("--comments", "-c", type=int, help="评论数（track时必填）")
    parser.add_argument("--shares", "-s", type=int, help="转发数（track时必填）")
    args = parser.parse_args()
    
    # 创建目录
    calendar_dir = Path.home() / "content-calendar"
    calendar_dir.mkdir(exist_ok=True)
    
    calendar_file = calendar_dir / "calendar.json"
    performance_file = calendar_dir / "performance.json"
    
    if args.action == "plan":
        if not args.week:
            print("❌ 缺少参数：--week")
            return
        
        year, week = args.week.split("-W")
        year, week = int(year), int(week)
        platforms = [p.strip() for p in args.platforms.split(",")]
        
        print(f"\n📅 正在生成{year}年第{week}周内容计划...\n")
        plan = generate_weekly_plan(year, week, platforms)
        markdown = format_weekly_plan_markdown(year, week, plan)
        
        print(markdown)
        
        # 保存到文件
        output_file = calendar_dir / "weekly" / f"{year}-W{week:02d}.md"
        output_file.parent.mkdir(exist_ok=True)
        output_file.write_text(markdown, encoding="utf-8")
        print(f"\n✅ 已保存：{output_file}\n")
    
    elif args.action == "add":
        if not all([args.title, args.platform, args.date, args.time]):
            print("❌ 缺少参数：需要 --title, --platform, --date, --time")
            return
        
        add_content_entry(args.title, args.platform, args.date, args.time, calendar_file)
    
    elif args.action == "track":
        if not all([args.id, args.likes, args.comments, args.shares]):
            print("❌ 缺少参数：需要 --id, --likes, --comments, --shares")
            return
        
        track_performance(args.id, args.likes, args.comments, args.shares, performance_file)
    
    elif args.action == "review":
        if not args.month:
            print("❌ 缺少参数：--month")
            return
        
        year, month = args.month.split("-")
        year, month = int(year), int(month)
        
        print(f"\n📊 正在生成{year}年{month}月复盘报告...\n")
        markdown = generate_monthly_review(year, month, performance_file)
        
        print(markdown)
        
        # 保存到文件
        output_file = calendar_dir / "monthly" / f"{year}-{month:02d}.md"
        output_file.parent.mkdir(exist_ok=True)
        output_file.write_text(markdown, encoding="utf-8")
        print(f"\n✅ 已保存：{output_file}\n")


if __name__ == "__main__":
    main()
