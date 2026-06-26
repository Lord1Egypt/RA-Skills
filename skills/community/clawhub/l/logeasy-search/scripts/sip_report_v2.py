#!/usr/bin/env python3
"""SIP 24小时安全态势报告 - 直接生成飞书文档"""
import sys, os, io, json, urllib.request, urllib.parse, base64
from datetime import datetime, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

RIZHIYI = 'http://10.20.51.16'
AUTH = base64.b64encode(b'admin:MIma@sec2025').decode()
headers = {'Authorization': f'Basic {AUTH}', 'Content-Type': 'application/json'}

def search_raw(query, time_range='now-24h,now', limit=100):
    params = {'query': query, 'time_range': time_range, 'index_name': 'yotta', 'limit': limit}
    url = f"{RIZHIYI}/api/v3/search/sheets/?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode('utf-8'))
        if result.get('rc') != 0:
            return {'total_hits': 0, 'rows': []}
        results = result.get('results', {})
        rows = results.get('sheets', {}).get('rows', [])
        return {'total_hits': results.get('total_hits', 0), 'rows': rows}
    except Exception as e:
        print(f"  [查询失败] {query}: {e}", file=sys.stderr)
        return {'total_hits': 0, 'rows': [], 'error': str(e)}

def extract_field(row, *fields):
    for f in fields:
        val = row.get(f)
        if val:
            return str(val)
    return ''

def count_field(rows, field):
    counts = {}
    for row in rows:
        val = extract_field(row, field)
        if val and val != '-':
            counts[val] = counts.get(val, 0) + 1
    return sorted(counts.items(), key=lambda x: -x[1])

def main():
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    report_time = now.strftime('%Y-%m-%d %H:%M')
    period = f"{yesterday.strftime('%Y-%m-%d %H:%M')} ~ {now.strftime('%H:%M')}"
    
    lines = []
    lines.append(f"# SIP 24小时安全态势报告")
    lines.append(f"\n> 报告时间：{report_time}  |  统计周期：{period}")
    lines.append(f"> 数据来源：深信服SIP → 日志易（{RIZHIYI}）")
    lines.append("")
    
    # 1. 总体概况
    lines.append("## 一、总体概况")
    lines.append("")
    total = search_raw("appname:sip", limit=1)
    total_hits = total.get('total_hits', 0)
    
    lines.append("| 指标 | 数值 |")
    lines.append("|------|------|")
    lines.append(f"| 安全事件总数 | **{total_hits:,}** |")
    
    levels = {}
    level_cfg = [
        ("高危", "appname:sip sip.threat_level:1", "🔴"),
        ("中危", "appname:sip sip.threat_level:2", "🟠"),
        ("低危", "appname:sip sip.threat_level:3", "🟡"),
        ("信息", "appname:sip sip.threat_level:4", "🔵"),
    ]
    for name, query, emoji in level_cfg:
        r = search_raw(query, limit=1)
        cnt = r.get('total_hits', 0)
        levels[name] = cnt
        lines.append(f"| {emoji} {name}事件 | {cnt:,} |")
    
    success_q = search_raw("appname:sip (sip.attack_state:成功 OR sip.attack_state:攻击成功)", limit=1).get('total_hits', 0)
    blocked = search_raw("appname:sip sip.attack_state:阻断", limit=1).get('total_hits', 0)
    lines.append(f"| ✅ 攻击成功 | {success_q:,} |")
    lines.append(f"| 🚫 已阻断 | {blocked:,} |")
    lines.append("")
    
    # 2. 攻击类型TOP10
    lines.append("## 二、攻击类型分析（TOP10）")
    lines.append("")
    result = search_raw("appname:sip sip.attack_type_name:*", limit=100)
    types = count_field(result.get('rows', []), 'sip.attack_type_name')
    
    if types:
        lines.append("| 排名 | 攻击类型 | 事件数 | 占比 |")
        lines.append("|------|---------|--------|------|")
        for i, (name, cnt) in enumerate(types[:10], 1):
            pct = f"{cnt/total_hits*100:.1f}%" if total_hits > 0 else "N/A"
            lines.append(f"| {i} | {name} | {cnt:,} | {pct} |")
    else:
        lines.append("（无数据）")
    lines.append("")
    
    # 3. 攻击子类型TOP10
    lines.append("## 三、攻击子类型分析（TOP10）")
    lines.append("")
    result = search_raw("appname:sip sip.sub_attack_type_name:*", limit=100)
    subs = count_field(result.get('rows', []), 'sip.sub_attack_type_name')
    
    if subs:
        lines.append("| 排名 | 攻击子类型 | 事件数 |")
        lines.append("|------|-----------|--------|")
        for i, (name, cnt) in enumerate(subs[:10], 1):
            lines.append(f"| {i} | {name} | {cnt:,} |")
    else:
        lines.append("（无数据）")
    lines.append("")
    
    # 4. TOP20攻击源
    lines.append("## 四、TOP20 攻击源IP")
    lines.append("")
    result = search_raw("appname:sip sip.attack_ip:*", limit=100)
    src_data = {}
    for row in result.get('rows', []):
        ip = extract_field(row, 'sip.attack_ip')
        country = extract_field(row, 'sip.attack_country')
        province = extract_field(row, 'sip.attack_province')
        if ip and ip != '-':
            key = (ip, country, province)
            src_data[key] = src_data.get(key, 0) + 1
    sorted_srcs = sorted(src_data.items(), key=lambda x: -x[1])[:20]
    
    if sorted_srcs:
        lines.append("| 排名 | 攻击源IP | 攻击次数 | 国家 | 省份 |")
        lines.append("|------|---------|---------|------|------|")
        for i, ((ip, country, province), cnt) in enumerate(sorted_srcs, 1):
            lines.append(f"| {i} | `{ip}` | {cnt:,} | {country or '-'} | {province or '-'} |")
    else:
        lines.append("（无数据）")
    lines.append("")
    
    # 5. TOP20被攻击目标
    lines.append("## 五、TOP20 被攻击目标IP")
    lines.append("")
    result = search_raw("appname:sip sip.suffer_ip:*", limit=100)
    dst_counts = count_field(result.get('rows', []), 'sip.suffer_ip')
    
    if dst_counts:
        lines.append("| 排名 | 目标IP | 被攻击次数 |")
        lines.append("|------|--------|-----------|")
        for i, (ip, cnt) in enumerate(dst_counts[:20], 1):
            lines.append(f"| {i} | `{ip}` | {cnt:,} |")
    else:
        lines.append("（无数据）")
    lines.append("")
    
    # 6. 暴力破解分析
    lines.append("## 六、暴力破解专项分析")
    lines.append("")
    brute_cnt = search_raw("appname:sip sip.sub_attack_type_name:*暴力*", limit=1).get('total_hits', 0)
    lines.append(f"暴力破解事件总数：**{brute_cnt:,}**")
    lines.append("")
    
    if brute_cnt > 0:
        result = search_raw("appname:sip sip.sub_attack_type_name:*暴力*", limit=100)
        targets = count_field(result.get('rows', []), 'sip.suffer_ip')
        if targets:
            lines.append("**被暴力破解TOP10目标：**")
            lines.append("")
            lines.append("| 目标IP | 暴力破解次数 |")
            lines.append("|--------|------------|")
            for ip, cnt in targets[:10]:
                lines.append(f"| `{ip}` | {cnt:,} |")
        
        srcs = count_field(result.get('rows', []), 'sip.attack_ip')
        if srcs:
            lines.append("")
            lines.append("**暴力破解源TOP10：**")
            lines.append("")
            lines.append("| 源IP | 攻击次数 |")
            lines.append("|------|---------|")
            for ip, cnt in srcs[:10]:
                lines.append(f"| `{ip}` | {cnt:,} |")
    lines.append("")
    
    # 7. 漏洞利用分析
    lines.append("## 七、漏洞利用专项分析")
    lines.append("")
    vuln_cnt = search_raw("appname:sip sip.event_desc:*CVE* OR sip.sub_attack_type_name:*漏洞*", limit=1).get('total_hits', 0)
    lines.append(f"漏洞利用事件总数：**{vuln_cnt:,}**")
    lines.append("")
    
    if vuln_cnt > 0:
        result = search_raw("appname:sip (sip.event_desc:*CVE* OR sip.sub_attack_type_name:*漏洞*)", limit=100)
        vuln_items = {}
        for row in result.get('rows', []):
            desc = extract_field(row, 'sip.event_desc', 'sip.sub_attack_type_name')
            if desc:
                # truncate long CVE descriptions
                short = desc[:90] + '...' if len(desc) > 90 else desc
                vuln_items[short] = vuln_items.get(short, 0) + 1
        sorted_vulns = sorted(vuln_items.items(), key=lambda x: -x[1])[:10]
        
        if sorted_vulns:
            lines.append("| 漏洞/事件 | 出现次数 |")
            lines.append("|----------|---------|")
            for name, cnt in sorted_vulns:
                lines.append(f"| {name} | {cnt:,} |")
    lines.append("")
    
    # 8. 攻击成功事件
    lines.append("## 八、攻击成功事件（需重点关注）")
    lines.append("")
    if success_q > 0:
        result = search_raw("appname:sip (sip.attack_state:成功 OR sip.attack_state:攻击成功)", limit=50)
        lines.append(f"共 {success_q} 条攻击成功事件，以下为部分详情：")
        lines.append("")
        for i, row in enumerate(result.get('rows', [])[:20], 1):
            attack_ip = extract_field(row, 'sip.attack_ip')
            suffer_ip = extract_field(row, 'sip.suffer_ip')
            attack_type = extract_field(row, 'sip.attack_type_name')
            sub_type = extract_field(row, 'sip.sub_attack_type_name')
            country = extract_field(row, 'sip.attack_country')
            desc = extract_field(row, 'sip.event_desc', 'sip.brief')
            
            lines.append(f"**{i}. {sub_type or attack_type}**")
            lines.append(f"   - 攻击源：`{attack_ip}`（{country or '未知'}）")
            lines.append(f"   - 目标：`{suffer_ip}`")
            if desc and desc != '-':
                display = desc[:150] + '...' if len(desc) > 150 else desc
                lines.append(f"   - 描述：{display}")
            lines.append("")
    else:
        lines.append("✅ 近24小时内无攻击成功事件")
    lines.append("")
    
    # 9. 小时趋势
    lines.append("## 九、攻击时间分布（按小时）")
    lines.append("")
    hourly = {}
    for h in range(24):
        h_start = (now - timedelta(hours=24-h)).strftime('%Y-%m-%d %H:00')
        h_end = (now - timedelta(hours=23-h)).strftime('%Y-%m-%d %H:00')
        query = f'appname:sip @d("{h_start}","{h_end}")'
        r = search_raw(query, limit=1)
        hourly[h] = r.get('total_hits', 0)
    
    max_cnt = max(hourly.values()) if hourly.values() else 1
    lines.append("| 时段 | 事件数 | 分布 |")
    lines.append("|------|--------|------|")
    for h, cnt in hourly.items():
        bar_len = int(cnt / max_cnt * 20) if max_cnt > 0 else 0
        bar = '█' * bar_len + '░' * (20 - bar_len)
        lines.append(f"| {h:02d}:00 | {cnt:,} | {bar} |")
    lines.append("")
    
    # 10. 运营建议
    lines.append("## 十、运营建议")
    lines.append("")
    
    suggestions = []
    if success_q > 0:
        suggestions.append(f"🚨 **{success_q}条攻击成功事件需立即排查**，建议逐一确认影响范围并处置")
    if brute_cnt > 0:
        suggestions.append(f"⚠️ 暴力破解攻击频繁（{brute_cnt:,}次），建议：\n  1. 检查被攻击目标的密码复杂度\n  2. 考虑封堵高频暴力破解源IP\n  3. 启用登录失败锁定策略")
    if levels.get("高危", 0) > 100:
        suggestions.append(f"🔴 高危事件较多（{levels.get('高危',0):,}次），建议优先处理高危告警")
    if total_hits > 0 and dst_counts:
        top_target, top_cnt = dst_counts[0]
        if top_cnt > total_hits * 0.2:
            suggestions.append(f"🎯 目标 `{top_target}` 承受了大量攻击，建议重点加固")
    if sorted_srcs:
        top_src_ip = sorted_srcs[0][0][0] if isinstance(sorted_srcs[0][0], tuple) else sorted_srcs[0][0]
        suggestions.append(f"🌐 攻击源IP `{top_src_ip}` 活跃度最高，建议加入防火墙黑名单观察")
    if not suggestions:
        suggestions.append("✅ 近24小时安全态势整体平稳，无重大安全事件")
    
    for i, s in enumerate(suggestions, 1):
        lines.append(f"{i}. {s}")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*报告由 OpenClaw 自动生成 | 数据统计截至 {report_time}*")
    
    # Output
    content = '\n'.join(lines)
    
    # Save to file
    outpath = os.path.join(os.environ.get('USERPROFILE', ''), '.openclaw', 'workspace', 'tmp', 'sip_report_clean.md')
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"报告已生成: {outpath}")
    print(f"总行数: {len(lines)}")

if __name__ == '__main__':
    main()
