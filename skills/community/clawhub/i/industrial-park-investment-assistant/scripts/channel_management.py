#!/usr/bin/env python3
"""
渠道经营模块 v1.0
=================
功能：
  1. 渠道维护提醒（周度）- 每周提醒哪些渠道需要联系
  2. 渠道开发提醒（月度）- 每月提醒该开发新渠道了
  3. 跟进频次一视同仁，不分渠道类别

用法：
  python3 channel_management.py --weekly       # 维护周报
  python3 channel_management.py --monthly      # 开发月报
  python3 channel_management.py --check        # 快速检查：渠道健康度概览
  python3 channel_management.py --all          # 全量渠道清单
  python3 channel_management.py --analysis     # 渠道效果分析
  python3 channel_management.py --update 渠道ID "联系内容"  # 记录跟进

数据库：
  ~/.workbuddy/workspace/investment-assistant/local_db.sqlite
  表名：渠道跟进记录
"""

import sqlite3
import sys
import os
from datetime import datetime, date, timedelta

DB_PATH = os.path.expanduser("~/.workbuddy/workspace/investment-assistant/local_db.sqlite")

# 渠道健康度阈值（一视同仁）
THRESHOLD_HEALTHY = 7       # <7天 → 🟢 正常
THRESHOLD_WARNING = 14      # 7-14天 → 🟡 需联系
THRESHOLD_OVERDUE = 30      # 14-30天 → 🔴 超期
                            # >30天 → 🚨 高危


def get_db():
    """连接SQLite数据库"""
    if not os.path.exists(DB_PATH):
        print(f"❌ 数据库不存在：{DB_PATH}")
        print("  提示：请先配置招商助手，导入渠道数据后再运行。")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_all_channels(conn):
    """获取所有渠道记录"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 渠道跟进记录 ORDER BY 上次沟通时间 DESC")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def calc_days_since(last_contact):
    """计算从上次沟通至今的天数"""
    if not last_contact:
        return None
    try:
        last_date = datetime.strptime(last_contact, "%Y-%m-%d").date()
        today = date.today()
        return (today - last_date).days
    except ValueError:
        return None


def get_channel_status(days):
    """根据天数返回渠道状态"""
    if days is None:
        return "unknown", "❓ 未知"
    if days <= THRESHOLD_HEALTHY:
        return "healthy", "🟢 正常"
    elif days <= THRESHOLD_WARNING:
        return "warning", "🟡 需联系"
    elif days <= THRESHOLD_OVERDUE:
        return "overdue", "🔴 超期"
    else:
        return "critical", "🚨 高危"


def generate_weekly_report(conn):
    """生成周报 — 渠道维护提醒"""
    channels = get_all_channels(conn)
    if not channels:
        print("📭 渠道列表为空，暂无渠道数据。")
        return

    today = date.today()
    this_week = today.isocalendar()[1]
    this_year = today.year

    # 分类
    healthy_list = []
    warning_list = []
    overdue_list = []
    critical_list = []
    unknown_list = []

    for ch in channels:
        days = calc_days_since(ch.get("上次沟通时间"))
        status, label = get_channel_status(days)
        ch["_days"] = days
        ch["_label"] = label

        if status == "healthy":
            healthy_list.append(ch)
        elif status == "warning":
            warning_list.append(ch)
        elif status == "overdue":
            overdue_list.append(ch)
        elif status == "critical":
            critical_list.append(ch)
        else:
            unknown_list.append(ch)

    # 输出
    print(f"📋 渠道维护周报 — {this_year}年第{this_week}周")
    print(f"📅 当前日期：{today}")
    print("=" * 50)

    # 今日待联系
    needs_contact = warning_list + overdue_list + critical_list
    if needs_contact:
        print(f"\n📞 本周需要联系的渠道（{len(needs_contact)}个）：")
        print("-" * 50)
        for ch in needs_contact:
            days = ch["_days"]
            name = ch.get("渠道名称", "未知")
            contact = ch.get("对接人", "未知")
            print(f"  {ch['_label']} {name}")
            print(f"     对接人：{contact} | 上次联系：{ch.get('上次沟通时间', '未知')}（{days}天前）")
            if days and days > THRESHOLD_WARNING:
                action = "建议今日电话联系" if days > THRESHOLD_OVERDUE else "建议本周内联系"
                print(f"     建议：{action}")
            print()
    else:
        print(f"\n✅ 所有渠道都在7天内联系过，暂无需要提醒的渠道。")
        print("   继续保持！")

    # 渠道健康度概览
    print(f"\n📊 渠道健康度概览：")
    print(f"  🟢 正常（{THRESHOLD_HEALTHY}天内）：{len(healthy_list)} 个")
    print(f"  🟡 需联系（{THRESHOLD_WARNING}天内）：{len(warning_list)} 个")
    print(f"  🔴 超期（{THRESHOLD_OVERDUE}天内）：{len(overdue_list)} 个")
    print(f"  🚨 高危（{THRESHOLD_OVERDUE}天以上）：{len(critical_list)} 个")
    if unknown_list:
        print(f"  ❓ 无联系记录：{len(unknown_list)} 个")

    # 总体评价
    total = len(channels)
    healthy_ratio = len(healthy_list) / total if total > 0 else 0
    if healthy_ratio >= 0.7:
        print(f"\n🏆 渠道维护状态良好！{healthy_ratio:.0%}的渠道近期都有联系。")
    elif healthy_ratio >= 0.4:
        print(f"\n⚠️ 渠道维护状态一般，{healthy_ratio:.0%}的渠道在7天内有联系。")
        print(f"   建议本周集中联系 {len(needs_contact)} 个超期渠道。")
    else:
        print(f"\n🚨 渠道维护状态较差！仅{healthy_ratio:.0%}的渠道在7天内有联系。")
        print(f"   建议立即安排时间联系 {len(needs_contact)} 个渠道！")

    return {
        "healthy": len(healthy_list),
        "warning": len(warning_list),
        "overdue": len(overdue_list),
        "critical": len(critical_list),
        "unknown": len(unknown_list),
        "needs_contact": len(needs_contact)
    }


def generate_monthly_report(conn):
    """生成月报 — 渠道开发提醒"""
    channels = get_all_channels(conn)
    today = date.today()

    print(f"📊 渠道开发月报 — {today.year}年{today.month}月")
    print(f"📅 当前日期：{today}")
    print("=" * 50)

    if not channels:
        print("📭 渠道列表为空，建议立即开始渠道开发。")
        print("\n🎯 本月渠道开发目标：")
        print("  1. 确定3-5个重点开发渠道类型（政府/五大行/协会/中介）")
        print("  2. 每周至少联系1个新渠道")
        print("  3. 建立渠道档案，记录对接人信息")
        return

    # 统计活跃渠道数量
    total = len(channels)
    active = sum(1 for ch in channels
                 if calc_days_since(ch.get("上次沟通时间")) is not None
                 and calc_days_since(ch.get("上次沟通时间")) <= THRESHOLD_HEALTHY)
    need_attention = sum(1 for ch in channels
                         if calc_days_since(ch.get("上次沟通时间")) is not None
                         and calc_days_since(ch.get("上次沟通时间")) > THRESHOLD_HEALTHY)
    no_contact = sum(1 for ch in channels if not ch.get("上次沟通时间"))

    total_recommend = sum(ch.get("推荐客户数", 0) or 0 for ch in channels)
    total_deal = sum(ch.get("成交数", 0) or 0 for ch in channels)
    conversion_rate = (total_deal / total_recommend * 100) if total_recommend > 0 else 0

    # 输出现有渠道分析
    print(f"\n📌 现有渠道概览：")
    print(f"  总渠道数：{total} 个")
    print(f"  🟢 活跃渠道（7天内联系）：{active} 个")
    print(f"  🟡 需关注渠道：{need_attention} 个")
    if no_contact:
        print(f"  ❓ 从未联系渠道：{no_contact} 个")
    print(f"  📊 总推荐客户数：{total_recommend} 个")
    print(f"  🏆 总成交数：{total_deal} 个（转化率：{conversion_rate:.1f}%）")

    # 渠道开发建议
    print(f"\n🎯 本月渠道开发目标建议：")

    target_new = max(3, total // 2)  # 建议开发数量
    print(f"  1. 新增渠道目标：{target_new} 个（现已有{total}个）")
    print(f"  2. 本周联系清单：{need_attention + no_contact} 个渠道需要跟进")
    print(f"  3. 重点关注：")

    # 给出具体建议
    if no_contact > 0:
        print(f"     - {no_contact} 个渠道从未联系，建议本周完成首次拜访")
    if need_attention > 0:
        print(f"     - {need_attention} 个渠道超期未联系，建议优先维护现有渠道")
    if len(channels) < 10:
        print(f"     - 渠道数量偏少（仅{total}个），建议加大开发力度")

    # 渠道推荐
    print(f"\n💡 推荐开发渠道类型：")
    print(f"  1. 🔴 高优：政府招商局 + 五大行（世邦魏理仕/仲量联行等）")
    print(f"  2. 🟡 中优：行业协会 + 商会 + 企业服务机构")
    print(f"  3. 🟢 日常：地产中介 + 线上平台 + 老客户推荐")

    return {
        "total": total,
        "active": active,
        "need_attention": need_attention,
        "no_contact": no_contact,
        "target_new": target_new
    }


def generate_analysis(conn):
    """渠道效果分析 — 转化率 + 排名 + 效果分级"""
    channels = get_all_channels(conn)
    if not channels:
        print("📭 渠道列表为空，暂无渠道数据。")
        return

    today = date.today()
    print(f"📊 渠道效果分析报告 — {today}")
    print("=" * 60)

    # 计算每个渠道的效果指标
    channel_stats = []
    for ch in channels:
        name = ch.get("渠道名称", "未知") or "未知"
        contact = ch.get("对接人", "") or ""
        recommend = ch.get("推荐客户数", 0) or 0
        deal = ch.get("成交数", 0) or 0
        conversion = (deal / recommend * 100) if recommend > 0 else 0
        days = calc_days_since(ch.get("上次沟通时间"))

        # 效果评级
        if conversion >= 30:
            effect_level = "🏆 卓越"
        elif conversion >= 15:
            effect_level = "✅ 优秀"
        elif conversion >= 5:
            effect_level = "📈 一般"
        elif recommend > 0:
            effect_level = "📉 待提升"
        else:
            effect_level = "❓ 未推荐"

        channel_stats.append({
            "name": name,
            "contact": contact,
            "recommend": recommend,
            "deal": deal,
            "conversion": conversion,
            "days": days,
            "effect_level": effect_level
        })

    # 按成交数排序
    sorted_by_deal = sorted(channel_stats, key=lambda x: x["deal"], reverse=True)
    # 按转化率排序
    sorted_by_conversion = sorted(
        [c for c in channel_stats if c["recommend"] > 0],
        key=lambda x: x["conversion"], reverse=True
    )

    # ------ 输出：渠道效果总览 ------
    print(f"\n📌 渠道效果总览")
    print("-" * 60)
    total_recommend = sum(c["recommend"] for c in channel_stats)
    total_deal = sum(c["deal"] for c in channel_stats)
    overall_conversion = (total_deal / total_recommend * 100) if total_recommend > 0 else 0
    effective_channels = sum(1 for c in channel_stats if c["deal"] > 0)
    print(f"  总渠道数：{len(channel_stats)} 个")
    print(f"  总推荐客户：{total_recommend} 个")
    print(f"  总成交数：{total_deal} 个")
    print(f"  整体转化率：{overall_conversion:.1f}%")
    print(f"  有效渠道（有成交）：{effective_channels} 个 / {len(channel_stats)} 个")

    # ------ 输出：渠道效果排名（按成交数） ------
    print(f"\n🏆 渠道效果排名（按成交数）")
    print("-" * 60)
    print(f"{'排名':<6} {'渠道名称':<15} {'对接人':<10} {'推荐':<6} {'成交':<6} {'转化率':<8} {'效果评级':<12}")
    print("-" * 60)
    for i, c in enumerate(sorted_by_deal, 1):
        print(f"{i:<6} {c['name']:<15} {c['contact']:<10} {c['recommend']:<6} {c['deal']:<6} {c['conversion']:<7.1f}% {c['effect_level']:<12}")

    # ------ 输出：渠道转化率排名 ------
    if sorted_by_conversion:
        print(f"\n📈 渠道转化率排名（推荐>0）")
        print("-" * 60)
        print(f"{'排名':<6} {'渠道名称':<15} {'推荐':<6} {'成交':<6} {'转化率':<8} {'效果评级':<12}")
        print("-" * 60)
        for i, c in enumerate(sorted_by_conversion[:10], 1):
            print(f"{i:<6} {c['name']:<15} {c['recommend']:<6} {c['deal']:<6} {c['conversion']:<7.1f}% {c['effect_level']:<12}")

    # ------ 输出：效果分级占比 ------
    print(f"\n📊 效果分级占比")
    print("-" * 60)
    levels = {}
    for c in channel_stats:
        levels[c["effect_level"]] = levels.get(c["effect_level"], 0) + 1
    for level, count in sorted(levels.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * count
        print(f"  {level}：{bar} {count} 个")

    # ------ 输出：改进建议 ------
    print(f"\n💡 渠道效果改进建议")
    print("-" * 60)
    no_deal = [c for c in channel_stats if c["recommend"] > 0 and c["deal"] == 0]
    no_recommend = [c for c in channel_stats if c["recommend"] == 0]

    if no_deal:
        print(f"  1. {len(no_deal)} 个渠道有推荐无成交：")
        for c in no_deal[:3]:
            print(f"     - {c['name']}（推荐 {c['recommend']} 个客户），建议沟通转化卡点")
    if no_recommend:
        print(f"  2. {len(no_recommend)} 个渠道未推荐客户：")
        for c in no_recommend[:3]:
            print(f"     - {c['name']}，建议加强合作关系，推送房源信息")
    if overall_conversion < 15:
        print(f"  3. 整体转化率 {overall_conversion:.1f}%，低于行业平均水平（15-20%）")
        print(f"     建议：评估渠道质量，优化渠道结构")
    elif overall_conversion >= 30:
        print(f"  3. 整体转化率 {overall_conversion:.1f}%，表现优秀！")
        print(f"     建议：加大与高转化渠道的合作力度")

    return channel_stats


def quick_check(conn):
    """快速检查 — 渠道健康度概览"""
    channels = get_all_channels(conn)
    if not channels:
        print("📭 暂无渠道数据。建议立即开始渠道开发！")
        return

    today = date.today()
    print(f"🔍 渠道健康度快速检查 — {today}")
    print("=" * 40)

    for ch in channels:
        days = calc_days_since(ch.get("上次沟通时间"))
        status, label = get_channel_status(days)
        name = ch.get("渠道名称", "未知")
        contact = ch.get("对接人", "未知")

        days_str = f"{days}天前" if days is not None else "无记录"
        print(f"  {label} {name}")
        print(f"     对接人：{contact} | 上次联系：{days_str}")

    total = len(channels)
    needs_contact = sum(1 for ch in channels
                        if calc_days_since(ch.get("上次沟通时间")) is not None
                        and calc_days_since(ch.get("上次沟通时间")) > THRESHOLD_HEALTHY)
    if needs_contact:
        print(f"\n📞 {needs_contact}/{total} 个渠道需要联系")
    else:
        print(f"\n✅ 所有渠道都在7天内联系过，状态良好！")


def list_all(conn):
    """全量渠道清单"""
    channels = get_all_channels(conn)
    if not channels:
        print("📭 暂无渠道数据。")
        return

    print(f"📋 全量渠道清单（共{len(channels)}个）")
    print("=" * 60)
    print(f"{'渠道名称':<15} {'对接人':<10} {'联系时间':<12} {'状态':<8} {'推荐数':<6} {'成交数':<6}")
    print("-" * 60)

    for ch in channels:
        name = ch.get("渠道名称", "未知") or "未知"
        contact = ch.get("对接人", "") or ""
        last_time = ch.get("上次沟通时间", "无记录") or "无记录"
        days = calc_days_since(ch.get("上次沟通时间"))
        _, label = get_channel_status(days)
        recommend = ch.get("推荐客户数", 0) or 0
        deal = ch.get("成交数", 0) or 0
        print(f"{name:<15} {contact:<10} {last_time:<12} {label:<8} {recommend:<6} {deal:<6}")

    print("-" * 60)


def update_channel(conn, channel_id, note):
    """记录渠道跟进"""
    if not channel_id or not note:
        print("❌ 请提供渠道ID和跟进内容")
        print("   用法：python3 channel_management.py --update 渠道ID \"跟进内容\"")
        return

    cursor = conn.cursor()
    # 检查渠道是否存在
    cursor.execute("SELECT * FROM 渠道跟进记录 WHERE 渠道ID=?", (channel_id,))
    row = cursor.fetchone()
    if not row:
        print(f"❌ 未找到渠道：{channel_id}")
        print(f"   现有渠道ID：")
        cursor.execute("SELECT 渠道ID, 渠道名称 FROM 渠道跟进记录")
        for r in cursor.fetchall():
            print(f"   - {r[0]}：{r[1]}")
        return

    today = date.today().isoformat()
    old_note = row["备注"] or ""
    new_note = f"[{today}] {note}" + (f"\n{old_note}" if old_note else "")

    cursor.execute(
        "UPDATE 渠道跟进记录 SET 上次沟通时间=?, 备注=? WHERE 渠道ID=?",
        (today, new_note, channel_id)
    )
    conn.commit()
    print(f"✅ 已记录渠道跟进：{row['渠道名称']}")
    print(f"   更新：上次沟通时间 → {today}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    conn = get_db()
    cmd = sys.argv[1]

    if cmd == "--weekly":
        generate_weekly_report(conn)
    elif cmd == "--monthly":
        generate_monthly_report(conn)
    elif cmd == "--check":
        quick_check(conn)
    elif cmd == "--all":
        list_all(conn)
    elif cmd == "--analysis" or cmd == "--effect":
        generate_analysis(conn)
    elif cmd == "--update" and len(sys.argv) >= 4:
        channel_id = sys.argv[2]
        note = sys.argv[3]
        update_channel(conn, channel_id, note)
    else:
        print(f"❌ 未知命令：{cmd}")
        print("   用法：python3 channel_management.py --weekly|--monthly|--check|--all|--analysis|--update 渠道ID \"内容\"")
        sys.exit(1)

    conn.close()


if __name__ == "__main__":
    main()
