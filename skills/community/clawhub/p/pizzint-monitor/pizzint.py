#!/usr/bin/env python3
"""
PizzINT Monitor - 披萨指数监测表 v3.0
======================================
修复版：修正指数解析、动态预测市场数据、逻辑一致性检查
"""

import subprocess
import re
import json
from datetime import datetime, timezone


def get_pizzint_data():
    """从 pizzint.watch 获取数据"""
    try:
        result = subprocess.run(
            ['curl', '-s', '--max-time', '10', 'https://pizzint.watch/'],
            capture_output=True, text=True, timeout=15
        )
        html = result.stdout
    except Exception as e:
        print(f"⚠️ 无法获取数据: {e}")
        return None

    data = {}

    # --- 1. 解析 NEH 指数 ---
    # 正确方式：找滑块的位置 "left: XX%"，这才是实时指数值
    # HTML结构: <div class="slider-track">...<div class="slider-thumb" style="left: 35%">
    neh_match = re.search(
        r'NothingEverHappens[^>]*>.*?left:\s*(\d+)%',
        html, re.DOTALL
    )
    if not neh_match:
        # 备用：找 "Status:" 附近的 aria-valuenow
        neh_match = re.search(r'Status.*?aria-valuenow["\s]*[:=]["\s]*(\d+)', html, re.DOTALL)

    neh_raw = int(neh_match.group(1)) if neh_match else None
    data['neh'] = neh_raw

    # --- 2. 解析 NEH 状态描述 ---
    # 状态标题: "Nothing Ever Happens" / "Something Might Happen" / "Something is Happening" / "It Happened"
    if neh_raw is not None:
        if neh_raw < 30:
            data['neh_status_text'] = "Nothing Ever Happens"
            data['neh_status_desc'] = "平静期，无明显异常"
            data['neh_status_emoji'] = "🟢"
        elif neh_raw < 65:
            data['neh_status_text'] = "Something Might Happen"
            data['neh_status_desc'] = "可能有事要发生，密切关注"
            data['neh_status_emoji'] = "🟡"
        elif neh_raw < 99:
            data['neh_status_text'] = "Something is Happening"
            data['neh_status_desc'] = "高风险，地缘事件进行中"
            data['neh_status_emoji'] = "🟠"
        else:
            data['neh_status_text'] = "It Happened"
            data['neh_status_desc'] = "重大事件已发生"
            data['neh_status_emoji'] = "🔴"
    else:
        data['neh_status_text'] = "Unknown"
        data['neh_status_desc'] = "无法获取"
        data['neh_status_emoji'] = "⚪"

    # --- 3. 解析 DOUGHCON ---
    doughcon_match = re.search(r'DOUGHCON\s*(\d+)', html)
    data['doughcon'] = int(doughcon_match.group(1)) if doughcon_match else None

    doughcon_desc_map = {
        1: "NORMAL - Baseline Activity",
        2: "ELEVATED - Increased Orders",
        3: "HIGH - Multiple Spikes",
        4: "DOUBLE TAKE - Intelligence Watch",
        5: "CRISIS - Military Operation Imminent",
    }
    data['doughcon_desc'] = doughcon_desc_map.get(data['doughcon'], "Unknown")

    # --- 4. 解析监控状态 ---
    status_match = re.search(r'Status:\s*OPERATIONAL', html)
    data['system_operational'] = bool(status_match)

    locations_match = re.search(r'(\d+)\s*LOCATIONS\s*MONITORED', html)
    data['locations'] = int(locations_match.group(1)) if locations_match else 8

    accounts_match = re.search(r'MONITORING\s*(\d+)\s*ACCOUNTS', html)
    data['accounts'] = int(accounts_match.group(1)) if accounts_match else None

    reports_match = re.search(r'(\d+)\s*REPORTS.*?(\d+)\s*ALERTS', html)
    data['reports'] = int(reports_match.group(1)) if reports_match else None
    data['alerts'] = int(reports_match.group(2)) if reports_match else None

    # --- 5. 解析披萨店异常 ---
    # 找所有 "XX% SPIKE" 模式的店铺
    spike_matches = re.findall(
        r'<h3[^>]*>([A-Z][A-Z\s]+)</h3>.*?(?:(\d+)%\s*SPIKE|"(\w+),\s*Busier than usual"|"(\w+),\s*Quieter than usual"|"(\w+),\s*Much busier than usual"|"(\w+),\s*Much quieter than usual")',
        html, re.DOTALL | re.IGNORECASE
    )
    # 简化：直接搜索状态文本
    pizza_alerts = []
    pizza_blocks = re.findall(
        r'<h3[^>]*>([A-Z][A-Z\s\'\-]+?)</h3>.*?<p[^>]*>([^<]+)</p>',
        html, re.DOTALL
    )
    for block in pizza_blocks:
        name = block[0].strip()
        status = block[1].strip()
        if any(x in status for x in ['SPIKE', 'spike', 'BUSIER', 'busier']):
            pizza_alerts.append({'name': name, 'status': status, 'alert': True})
        elif data['neh'] and data['neh'] >= 30:
            pizza_alerts.append({'name': name, 'status': status, 'alert': False})
    data['pizza_alerts'] = pizza_alerts[:5]  # 最多5家

    # --- 6. 解析 PolyPulse 双边威胁 ---
    threat_map = {}
    risk_levels = ['CRITICAL', 'HIGH', 'MODERATE', 'ELEVATED']
    for level in risk_levels:
        level_matches = re.findall(
            rf'{level}\s+(USA / IRAN|USA / RUS|RUS / UKR|USA / VEN|USA / CHN|CHN / TWN)',
            html
        )
        for pair in level_matches:
            threat_map[pair] = level
    data['threats'] = threat_map

    # --- 7. 解析 Breaking Ticker 预测市场 ---
    markets = []
    ticker_matches = re.findall(
        r'<p[^>]*>([^<]{10,80})</p>.*?(\d+)%',
        html, re.DOTALL
    )
    # 从 Polymarket 链接中提取市场名称
    market_links = re.findall(
        r'href="https://polymarket.com/market/([^"?]+)"[^>]*>.*?<p[^>]*>([^<]{10,80})</p>.*?(\d+)%',
        html, re.DOTALL
    )
    for link, name, prob in market_links[:5]:
        decoded_name = name.replace('%20', ' ').replace('%3F', '?')
        markets.append({
            'name': decoded_name,
            'probability': int(prob),
            'link': f"polymarket.com/market/{link}"
        })
    data['markets'] = markets

    # --- 8. 解析 OSINT 最新动态（前3条）---
    osint_items = re.findall(
        r'@(\w+)[^>]*>.*?<p[^>]*>([^<]{30,300})</p>',
        html, re.DOTALL
    )
    data['osint'] = [{'account': '@'+a, 'text': t.strip()} for a, t in osint_items[:5]]

    # --- 9. 解析市场状态 ---
    market_closed = 'CLOSED' in html
    market_match = re.search(r'OPENS IN (\d+)h', html)
    market_open_match = re.search(r'CLOSES? IN (\d+)h', html)
    if market_closed and market_match:
        data['market_status'] = f"CLOSED (距开盘 {market_match.group(1)}小时)"
    elif market_open_match:
        data['market_status'] = f"OPEN (距收盘 {market_open_match.group(1)}小时)"
    else:
        data['market_status'] = "未知"

    return data


def check_logic(data):
    """⚠️ 逻辑一致性检查：发现矛盾时返回警告列表"""
    warnings = []

    if data is None:
        warnings.append("无法获取数据，无法进行逻辑校验")
        return warnings

    neh = data.get('neh')
    status_text = data.get('neh_status_text', '')

    # 检查1: NEH数值与状态描述是否一致
    if neh is not None:
        if neh < 30 and 'Might' in status_text:
            warnings.append(f"⚠️ 逻辑矛盾: NEH={neh}（<30）但状态为'{status_text}'，应为'Nothing Ever Happens'")
        elif 30 <= neh < 65 and ('Nothing' in status_text or 'Happened' in status_text):
            warnings.append(f"⚠️ 逻辑矛盾: NEH={neh}（30~65区间）但状态为'{status_text}'，应为'Something Might Happen'")
        elif 65 <= neh < 99 and 'Might' in status_text:
            warnings.append(f"⚠️ 逻辑矛盾: NEH={neh}（>=65）但状态为'{status_text}'，应为'Something is Happening'")
        elif neh >= 99 and 'Something Might' in status_text:
            warnings.append(f"⚠️ 逻辑矛盾: NEH={neh}（>=99）但状态为'{status_text}'，应为'It Happened'")

        # 检查2: 阈值判断
        if neh > 30:
            warnings.append(f"ℹ️ NEH={neh} > 30，进入预警状态")
        if neh > 65:
            warnings.append(f"🚨 NEH={neh} > 65，高风险区间")
        if neh > 99:
            warnings.append(f"🚨 NEH={neh} >= 100，重大事件区间")

    # 检查3: DOUGHCON
    dc = data.get('doughcon')
    if dc is not None and dc >= 4:
        warnings.append(f"⚠️ DOUGHCON={dc} >= 4，进入情报警戒状态")

    return warnings


def format_report(data):
    """生成 PizzINT 状态报告"""
    if data is None:
        return "⚠️ 无法获取数据，请稍后重试或手动访问 https://pizzint.watch/"

    neh = data.get('neh')
    beijing_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    utc_time = datetime.now(timezone.utc).strftime("%H:%M")

    lines = []
    lines.append(f"🦞 **PizzINT 指数状态报告**")
    lines.append(f"更新时间: {beijing_time} (北京时间) / {utc_time} (UTC)")
    lines.append("")

    # 整体状态
    lines.append("**📊 整体状态**")
    system_status = "✅ OPERATIONAL" if data.get('system_operational') else "⚠️ 未知"
    lines.append(f"| 指标 | 状态 |")
    lines.append(f"|------|------|")
    lines.append(f"| 系统状态 | {system_status} |")
    lines.append(f"| 市场状态 | {data.get('market_status', '未知')} |")
    lines.append(f"| 监控店铺 | {data.get('locations', '?')}处 |")
    if data.get('accounts'):
        lines.append(f"| OSINT账号 | 监控 {data.get('accounts')} 个 |")
    if data.get('reports'):
        lines.append(f"| OSINT报告 | {data.get('reports')} 条 / {data.get('alerts', '?')} 警报 |")
    lines.append("")

    # 核心指数（NEH）
    lines.append("**🎯 Nothing Ever Happens 指数**")
    neh_val = f"**{neh}**" if neh is not None else "**?**"
    status_emoji = data.get('neh_status_emoji', '⚪')
    status_text = data.get('neh_status_text', 'Unknown')
    status_desc = data.get('neh_status_desc', '')
    lines.append(f"| 指数 | 状态 | 说明 |")
    lines.append(f"|------|------|------|")
    lines.append(f"| {neh_val} | {status_emoji} {status_text} | {status_desc} |")
    lines.append("")

    # DOUGHCON
    dc = data.get('doughcon')
    dc_desc = data.get('doughcon_desc', 'Unknown')
    dc_emoji = "🔴" if (dc and dc >= 4) else ("🟠" if (dc and dc >= 3) else ("🟡" if dc else "⚪"))
    lines.append(f"**🚨 DOUGHCON 等级: {dc_emoji} {dc} — {dc_desc}**")
    lines.append("")

    # 披萨店异常
    pizza = data.get('pizza_alerts', [])
    if pizza:
        lines.append("**🍕 披萨店活动异常**")
        for shop in pizza:
            flag = "🚨" if shop['alert'] else "  "
            lines.append(f"{flag} **{shop['name']}**: {shop['status']}")
        lines.append("")

    # PolyPulse 双边威胁
    threats = data.get('threats', {})
    if threats:
        lines.append("**🌍 地缘威胁 (PolyPulse)**")
        level_emoji = {
            'CRITICAL': '🔴', 'HIGH': '🟠',
            'MODERATE': '🟡', 'ELEVATED': '🟡'
        }
        pair_name = {
            'USA / IRAN': '🇺🇸/🇮🇷 美国-伊朗',
            'RUS / UKR': '🇷🇺/🇺🇦 俄罗斯-乌克兰',
            'USA / VEN': '🇺🇸/🇻🇪 美国-委内瑞拉',
            'USA / CHN': '🇺🇸/🇨🇳 美国-中国',
            'USA / RUS': '🇺🇸/🇷🇺 美国-俄罗斯',
            'CHN / TWN': '🇨🇳/🇹🇼 中国-台湾',
        }
        lines.append("| 地区 | 风险等级 |")
        lines.append("|------|----------|")
        for pair, level in sorted(threats.items(), key=lambda x: ['CRITICAL','HIGH','ELEVATED','MODERATE'].index(x[1]) if x[1] in ['CRITICAL','HIGH','ELEVATED','MODERATE'] else 99):
            emoji = level_emoji.get(level, '⚪')
            name = pair_name.get(pair, pair)
            lines.append(f"| {name} | {emoji} {level} |")
        lines.append("")

    # 预测市场（Breaking Ticker）
    markets = data.get('markets', [])
    if markets:
        lines.append("**📈 预测市场 (Polymarket)**")
        for m in markets[:5]:
            prob_emoji = "🔴" if m['probability'] >= 70 else ("🟠" if m['probability'] >= 50 else "🟡")
            lines.append(f"{prob_emoji} **{m['name']}** → {m['probability']}%")
        lines.append("")

    # 最新 OSINT 动态
    osint = data.get('osint', [])
    if osint:
        lines.append("**📰 最新 OSINT 动态**")
        for item in osint[:3]:
            text = item['text'][:120] + ('...' if len(item['text']) > 120 else '')
            lines.append(f"• {item['account']}: {text}")
        lines.append("")

    # 逻辑校验警告
    warnings = check_logic(data)
    if warnings:
        for w in warnings:
            lines.append(w)
        lines.append("")

    # 风险提示
    lines.append("⚠️ *披萨指数是 OSINT 开源情报工具，相关性≠因果性，仅供参考。*")
    lines.append(f"📡 数据来源: https://pizzint.watch/")

    return "\n".join(lines)


def main():
    print("正在获取 PizzINT 数据...")
    data = get_pizzint_data()

    # 先做逻辑检查
    warnings = check_logic(data)
    for w in warnings:
        print(w)

    print("")
    print(format_report(data))


if __name__ == "__main__":
    main()
