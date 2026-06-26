#!/usr/bin/env python3
"""
今日工作台 Dashboard v1.1
=======================
合并看板：今日必跟客户 + 今日必跟渠道 + 预警信息 + 本周动态
一条消息看完所有待办事项，不再分时间推送。

用法：
  python3 dashboard.py           # 合并输出（文本）
  python3 dashboard.py --html    # 生成HTML/SVG仪表盘
  python3 dashboard.py --daily   # 每日推送专用（简洁版）

数据库：
  ~/.workbuddy/workspace/investment-assistant/local_db.sqlite
"""

import sqlite3
import os
import sys
import json
from datetime import datetime, date, timedelta

DB_PATH = os.path.expanduser("~/.workbuddy/workspace/investment-assistant/local_db.sqlite")

# 客户跟进超期阈值
CUSTOMER_THRESHOLD = {
    "A": {"warning": 7, "critical": 14},
    "B": {"warning": 14, "critical": 30},
    "C": {"warning": 30, "critical": 60},
    "D": {"warning": 60, "critical": 90},
}
DEFAULT_THRESHOLD = {"warning": 14, "critical": 30}

# 渠道超期阈值（一视同仁）
CHANNEL_HEALTHY = 7
CHANNEL_WARNING = 14
CHANNEL_OVERDUE = 30


def get_db():
    if not os.path.exists(DB_PATH):
        print("❌ 数据库不存在，请先配置招商助手。")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def calc_days_since(date_str):
    if not date_str:
        return None
    try:
        d = datetime.strptime(str(date_str)[:10], "%Y-%m-%d").date()
        return (date.today() - d).days
    except ValueError:
        return None


def get_customers_to_follow(conn):
    """获取今日需要跟进的客户"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 客户跟进记录 ORDER BY 上次跟进时间 ASC")
    rows = [dict(r) for r in cursor.fetchall()]

    # 如果客户表为空，降级使用 房源销控表 中已出租房源的状态
    if not rows:
        return {"critical": [], "warning": [], "normal": [], "total": 0}

    critical = []
    warning = []
    normal = []

    for c in rows:
        days = calc_days_since(c.get("上次跟进时间"))
        status = c.get("跟进状态", "")
        name = c.get("客户名称", "未知") or "未知"
        contact = c.get("联系人", "") or ""

        if days is None:
            normal.append({"name": name, "contact": contact, "days": "无记录", "status": status, "level": "normal"})
            continue

        # 根据跟进状态判断紧急程度
        if "洽谈" in status or "需求" in status:
            threshold = CUSTOMER_THRESHOLD.get("A", DEFAULT_THRESHOLD)
        elif "方案" in status or "对比" in status:
            threshold = CUSTOMER_THRESHOLD.get("B", DEFAULT_THRESHOLD)
        elif "谈判" in status:
            threshold = CUSTOMER_THRESHOLD.get("A", DEFAULT_THRESHOLD)
        else:
            threshold = DEFAULT_THRESHOLD

        if days >= threshold["critical"]:
            critical.append({"name": name, "contact": contact, "days": days, "status": status, "level": "critical"})
        elif days >= threshold["warning"]:
            warning.append({"name": name, "contact": contact, "days": days, "status": status, "level": "warning"})
        else:
            normal.append({"name": name, "contact": contact, "days": days, "status": status, "level": "normal"})

    return {"critical": critical, "warning": warning, "normal": normal, "total": len(rows)}


def get_channels_to_follow(conn):
    """获取今日需要联系的渠道"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 渠道跟进记录 ORDER BY 上次沟通时间 ASC")
    rows = [dict(r) for r in cursor.fetchall()]

    if not rows:
        return {"needs_contact": [], "healthy": [], "total": 0}

    needs_contact = []
    healthy = []

    for ch in rows:
        days = calc_days_since(ch.get("上次沟通时间"))
        name = ch.get("渠道名称", "未知") or "未知"
        contact = ch.get("对接人", "") or ""

        if days is None:
            needs_contact.append({"name": name, "contact": contact, "days": "无记录"})
            continue

        if days > CHANNEL_HEALTHY:
            needs_contact.append({"name": name, "contact": contact, "days": days})
        else:
            healthy.append({"name": name, "contact": contact, "days": days})

    return {"needs_contact": needs_contact, "healthy": healthy, "total": len(rows)}


def get_new_customers_this_week(conn):
    """获取本周新增客户（基于入库时间）"""
    cursor = conn.cursor()
    # 获取本周一日期
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    monday_str = monday.isoformat()

    cursor.execute(
        "SELECT * FROM 客户跟进记录 WHERE 入库时间 >= ?",
        (monday_str,)
    )
    return [dict(r) for r in cursor.fetchall()]


def generate_dashboard(conn):
    """生成Dashboard数据"""
    customers = get_customers_to_follow(conn)
    channels = get_channels_to_follow(conn)
    new_customers = get_new_customers_this_week(conn)

    # 预警信息汇总
    alerts = []
    # 客户超期预警
    for item in customers["critical"]:
        alerts.append({
            "type": "customer_critical",
            "level": "🔴",
            "message": f"客户 {item['name']}（{item['contact']}）已{item['days']}天未跟进！",
            "action": "建议今日电话联系"
        })
    for item in customers["warning"]:
        alerts.append({
            "type": "customer_warning",
            "level": "🟡",
            "message": f"客户 {item['name']}（{item['contact']}）{item['days']}天未跟进",
            "action": "建议本周内联系"
        })
    # 渠道超期预警
    for item in channels["needs_contact"]:
        days = item["days"]
        if isinstance(days, int) and days > CHANNEL_OVERDUE:
            alerts.append({
                "type": "channel_critical",
                "level": "🚨",
                "message": f"渠道 {item['name']}（{item['contact']}）已{days}天未联系！",
                "action": "渠道可能流失，建议立即联系"
            })
        elif isinstance(days, int) and days > CHANNEL_WARNING:
            alerts.append({
                "type": "channel_warning",
                "level": "🔴",
                "message": f"渠道 {item['name']}（{item['contact']}）{days}天未联系",
                "action": "建议今日联系"
            })

    # 按紧急程度排序
    alerts.sort(key=lambda x: {"🚨": 0, "🔴": 1, "🟡": 2}.get(x["level"], 3))

    return {
        "date": date.today().isoformat(),
        "customers": customers,
        "channels": channels,
        "new_customers_this_week": len(new_customers),
        "alerts": alerts,
        "total_alerts": len(alerts),
    }


def format_text_dashboard(data):
    """文本格式输出Dashboard（合并客户+渠道+预警）"""
    today = data["date"]
    c = data["customers"]
    ch = data["channels"]
    alerts = data.get("alerts", [])

    output = f"📋 今日工作台 — {today}\n"
    output += "=" * 50 + "\n"

    # ====== 预警信息（最前面） ======
    if alerts:
        output += f"\n🚨 预警信息（{len(alerts)}条）\n"
        output += "-" * 40 + "\n"
        for a in alerts[:5]:
            output += f"  {a['level']} {a['message']}\n"
            output += f"     → {a['action']}\n"
        if len(alerts) > 5:
            output += f"  ...还有{len(alerts)-5}条预警，说「今日待办」查看全部\n"
    else:
        output += "\n✅ 暂无预警，状态良好！\n"

    # ====== 概览 ======
    output += f"\n📊 今日概览\n"
    output += f"  🔴 紧急客户：{len(c['critical'])} 个    🟡 重要客户：{len(c['warning'])} 个\n"
    output += f"  📞 渠道待联系：{len(ch['needs_contact'])} 个  🆕 本周新增：{data['new_customers_this_week']} 个\n"

    # ====== 客户必跟清单 ======
    total_follow = len(c['critical']) + len(c['warning'])
    output += f"\n📋 待办事项（共{total_follow + len(ch['needs_contact'])}项）\n"
    output += "-" * 40 + "\n"

    if c['critical']:
        for item in c['critical']:
            output += f"  🔴 {item['name']}（{item['contact']}）{item['days']}天未跟进 → 今日必须处理！\n"
    if c['warning']:
        for item in c['warning']:
            output += f"  🟡 {item['name']}（{item['contact']}）{item['days']}天未跟进 → 本周内处理\n"
    if ch['needs_contact']:
        for item in ch['needs_contact'][:5]:
            days_str = f"{item['days']}天前" if isinstance(item['days'], int) else item['days']
            output += f"  📞 {item['name']}（{item['contact']}）上次联系：{days_str}\n"
        if len(ch['needs_contact']) > 5:
            output += f"  ...还有{len(ch['needs_contact'])-5}个渠道需要联系\n"
    if total_follow == 0 and len(ch['needs_contact']) == 0:
        output += "  今日无待办事项，继续保持！✅\n"

    # ====== 新手上路（无数据时） ======
    if c['total'] == 0 and ch['total'] == 0:
        output += f"\n💡 新手上路：\n"
        output += f"  1. 说「这是我的数据」+ 发腾讯文档链接/上传Excel\n"
        output += f"  2. 开始跟进客户（说「刚才见了XX科技」）\n"
        output += f"  3. 每天查看这里（说「今日待办」）\n"

    output += "\n" + "=" * 50 + "\n"
    output += f"💬 说「今日待办」刷新 | 语音录入自动更新数据\n"
    return output


def format_daily_digest(data):
    """每日推送专用版（简洁、可读、一条消息看完）"""
    today = data["date"]
    c = data["customers"]
    ch = data["channels"]
    alerts = data.get("alerts", [])

    output = f"🌅 早安！今日工作台 — {today}\n"
    output += "=" * 40 + "\n"

    # 概览（一句话）
    critical = len(c['critical'])
    warning = len(c['warning'])
    channels = len(ch['needs_contact'])
    new_c = data['new_customers_this_week']

    items = []
    if critical:
        items.append(f"🔴{critical}个紧急客户")
    if warning:
        items.append(f"🟡{warning}个待跟进客户")
    if channels:
        items.append(f"📞{channels}个渠道需联系")
    if new_c:
        items.append(f"🆕{new_c}个本周新客户")

    if items:
        output += f"📊 今日有 {' · '.join(items)}\n\n"
    else:
        output += "✅ 今日无待办事项，继续保持！\n"
        return output

    # 预警（最多3条）
    if alerts:
        for a in alerts[:3]:
            output += f"  {a['level']} {a['message']}\n"
        if len(alerts) > 3:
            output += f"  ...还有{len(alerts)-3}条预警\n"

    output += f"\n📋 待办清单\n"
    output += "-" * 30 + "\n"

    for item in c['critical'][:3]:
        output += f"  🔴 {item['name']} — {item['days']}天未跟进\n"
    for item in c['warning'][:3]:
        output += f"  🟡 {item['name']} — {item['days']}天未跟进\n"
    for item in ch['needs_contact'][:3]:
        days_str = f"{item['days']}天" if isinstance(item['days'], int) else item['days']
        output += f"  📞 {item['name']} — 上次联系：{days_str}前\n"

    output += f"\n💬 说「今日待办」查看完整清单 | 语音录入自动同步\n"
    return output


def generate_html_dashboard(data):
    """生成HTML仪表盘（用于show_widget或预览）"""
    today = data["date"]
    c = data["customers"]
    ch = data["channels"]

    critical_count = len(c["critical"])
    warning_count = len(c["warning"])
    channel_count = len(ch["needs_contact"])
    new_customers = data["new_customers_this_week"]

    # 生成客户列表HTML
    customer_rows = ""
    for item in c["critical"]:
        customer_rows += f"""
        <tr style="background:#fef2f2;">
            <td>🚨 {item['name']}</td>
            <td>{item['contact']}</td>
            <td>{item['days']}天</td>
            <td><span class="badge badge-red">紧急</span></td>
        </tr>"""
    for item in c["warning"]:
        customer_rows += f"""
        <tr style="background:#fffbeb;">
            <td>⚠️ {item['name']}</td>
            <td>{item['contact']}</td>
            <td>{item['days']}天</td>
            <td><span class="badge badge-yellow">重要</span></td>
        </tr>"""
    if not c["critical"] and not c["warning"]:
        customer_rows = """
        <tr>
            <td colspan="4" style="text-align:center;color:#6b7280;padding:20px;">
                暂无待跟进客户 ✅
            </td>
        </tr>"""

    # 生成渠道列表HTML
    channel_rows = ""
    for item in ch["needs_contact"][:8]:
        days_str = f"{item['days']}天前" if isinstance(item['days'], int) else item['days']
        channel_rows += f"""
        <tr>
            <td>{item['name']}</td>
            <td>{item['contact']}</td>
            <td>{days_str}</td>
        </tr>"""
    if not ch["needs_contact"]:
        channel_rows = """
        <tr>
            <td colspan="3" style="text-align:center;color:#6b7280;padding:20px;">
                所有渠道都在7天内联系过 ✅
            </td>
        </tr>"""

    html = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 520" style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.1"/>
    </filter>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1e40af"/>
      <stop offset="100%" style="stop-color:#3b82f6"/>
    </linearGradient>
  </defs>

  <!-- 背景 -->
  <rect width="680" height="520" fill="#f8fafc" rx="12"/>

  <!-- 头部 -->
  <rect width="680" height="64" fill="url(#headerGrad)" rx="12"/>
  <rect y="52" width="680" height="12" fill="url(#headerGrad)"/>
  <text x="24" y="40" fill="white" font-size="20" font-weight="bold">📋 今日工作台</text>
  <text x="24" y="58" fill="#bfdbfe" font-size="12">{today}</text>

  <!-- 概览卡片 -->
  <!-- 紧急客户 -->
  <rect x="20" y="80" width="150" height="80" rx="10" fill="white" filter="url(#shadow)"/>
  <text x="95" y="110" text-anchor="middle" font-size="36" font-weight="bold" fill={'"#ef4444"' if critical_count > 0 else '"#22c55e"'}>
    {critical_count}
  </text>
  <text x="95" y="135" text-anchor="middle" font-size="12" fill="#6b7280">🔴 紧急客户</text>

  <!-- 重要客户 -->
  <rect x="185" y="80" width="150" height="80" rx="10" fill="white" filter="url(#shadow)"/>
  <text x="260" y="110" text-anchor="middle" font-size="36" font-weight="bold" fill={'"#f59e0b"' if warning_count > 0 else '"#22c55e"'}>
    {warning_count}
  </text>
  <text x="260" y="135" text-anchor="middle" font-size="12" fill="#6b7280">🟡 重要客户</text>

  <!-- 渠道待联系 -->
  <rect x="350" y="80" width="150" height="80" rx="10" fill="white" filter="url(#shadow)"/>
  <text x="425" y="110" text-anchor="middle" font-size="36" font-weight="bold" fill={'"#f59e0b"' if channel_count > 0 else '"#22c55e"'}>
    {channel_count}
  </text>
  <text x="425" y="135" text-anchor="middle" font-size="12" fill="#6b7280">📞 渠道待联系</text>

  <!-- 本周新增 -->
  <rect x="515" y="80" width="150" height="80" rx="10" fill="white" filter="url(#shadow)"/>
  <text x="590" y="110" text-anchor="middle" font-size="36" font-weight="bold" fill="#3b82f6">
    {new_customers}
  </text>
  <text x="590" y="135" text-anchor="middle" font-size="12" fill="#6b7280">🆕 本周新增</text>

  <!-- 客户必跟清单标题 -->
  <text x="24" y="190" font-size="14" font-weight="bold" fill="#1f2937">🔴 客户必跟清单（紧急+重要：{critical_count + warning_count} 个）</text>
  <line x1="24" y1="198" x2="660" y2="198" stroke="#e5e7eb" stroke-width="1"/>

  <!-- 客户清单（用文本模拟） -->
  <text x="24" y="216" font-size="11" fill="#6b7280">{'客户名称':<16}{'联系人':<12}{'超期':<8}{'状态':<8}</text>
  <line x1="24" y1="222" x2="660" y2="222" stroke="#e5e7eb" stroke-width="0.5"/>
"""
    # 添加客户行
    y_pos = 240
    for item in c["critical"][:3]:
        html += f'  <text x="24" y="{y_pos}" font-size="11" fill="#dc2626">🚨 {item["name"]:<13}{item["contact"]:<10}{item["days"]}天{"":<5}紧急</text>\n'
        y_pos += 18
    for item in c["warning"][:3]:
        html += f'  <text x="24" y="{y_pos}" font-size="11" fill="#d97706">⚠️ {item["name"]:<13}{item["contact"]:<10}{item["days"]}天{"":<5}重要</text>\n'
        y_pos += 18
    if not c["critical"] and not c["warning"]:
        html += f'  <text x="24" y="{y_pos}" font-size="11" fill="#6b7280">暂无待跟进客户</text>\n'
        y_pos += 18

    # 渠道必跟清单
    y_pos = max(y_pos + 10, 300)
    html += f'  <text x="24" y="{y_pos}" font-size="14" font-weight="bold" fill="#1f2937">📞 渠道必跟清单（{channel_count} 个）</text>\n'
    y_pos += 18
    html += f'  <text x="24" y="{y_pos}" font-size="11" fill="#6b7280">{"渠道名称":<16}{"对接人":<12}{"上次联系":<12}</text>\n'
    y_pos += 6
    html += f'  <line x1="24" y1="{y_pos}" x2="660" y2="{y_pos}" stroke="#e5e7eb" stroke-width="0.5"/>\n'
    y_pos += 18

    for item in ch["needs_contact"][:4]:
        days_str = f"{item['days']}天前" if isinstance(item['days'], int) else item['days']
        html += f'  <text x="24" y="{y_pos}" font-size="11" fill="#d97706">🟡 {item["name"]:<13}{item["contact"]:<10}{days_str:<10}</text>\n'
        y_pos += 16
    if not ch["needs_contact"]:
        html += f'  <text x="24" y="{y_pos}" font-size="11" fill="#6b7280">所有渠道都在7天内联系过</text>\n'

    # 底部提示
    y_pos = max(y_pos + 20, 460)
    html += f'  <text x="340" y="{y_pos}" text-anchor="middle" font-size="11" fill="#9ca3af">说「今日待办」刷新 · 语音录入自动更新</text>\n'

    html += '</svg>'
    return html


def main():
    conn = get_db()
    data = generate_dashboard(conn)
    conn.close()

    if len(sys.argv) > 1 and sys.argv[1] == "--html":
        # 输出HTML到文件
        html = generate_html_dashboard(data)
        output_dir = os.path.expanduser("~/.workbuddy/workspace/investment-assistant")
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "dashboard.html")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f'<!DOCTYPE html><html><body>{html}</body></html>')
        print(f"✅ Dashboard已生成：{output_file}")
        return output_file
    elif len(sys.argv) > 1 and sys.argv[1] == "--daily":
        # 每日推送专用（简洁版）
        print(format_daily_digest(data))
    else:
        # 完整版
        print(format_text_dashboard(data))


if __name__ == "__main__":
    main()
