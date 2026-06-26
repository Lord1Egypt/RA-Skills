#!/usr/bin/env python3
"""SIP 24小时安全态势报告生成脚本"""
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

def fmt_ts(ts):
    if ts and ts > 0:
        return datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M:%S')
    return 'N/A'

def extract_field(row, *fields):
    for f in fields:
        val = row.get(f)
        if val:
            return str(val)
    return ''

def topk(field, query_filter='appname:sip', top=10):
    """通过搜索结果手动统计topk"""
    result = search_raw(query_filter, limit=100)
    counts = {}
    for row in result.get('rows', []):
        val = extract_field(row, field)
        if val and val != '-':
            counts[val] = counts.get(val, 0) + 1
    # 排序
    sorted_items = sorted(counts.items(), key=lambda x: -x[1])[:top]
    return sorted_items

def main():
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    report_time = now.strftime('%Y-%m-%d %H:%M')
    period = f"{yesterday.strftime('%Y-%m-%d %H:%M')} ~ {now.strftime('%H:%M')}"
    
    print(f"# SIP 24小时安全态势报告")
    print(f"\n> 报告时间：{report_time}  |  统计周期：{period}")
    print(f"> 数据来源：深信服SIP → 日志易（{RIZHIYI}）")
    print()
    
    # ===== 1. 总体概况 =====
    print("## 一、总体概况")
    print()
    total = search_raw("appname:sip", limit=1)
    total_hits = total.get('total_hits', 0)
    print(f"| 指标 | 数值 |")
    print(f"|------|------|")
    print(f"| 安全事件总数 | **{total_hits:,}** |")
    
    # 按威胁等级统计
    levels = {}
    for level_name, level_query in [
        ("高危", "appname:sip sip.threat_level:1"),
        ("中危", "appname:sip sip.threat_level:2"),
        ("低危", "appname:sip sip.threat_level:3"),
        ("信息", "appname:sip sip.threat_level:4"),
    ]:
        r = search_raw(level_query, limit=1)
        cnt = r.get('total_hits', 0)
        levels[level_name] = cnt
        emoji = {"高危": "🔴", "中危": "🟠", "低危": "🟡", "信息": "🔵"}[level_name]
        print(f"| {emoji} {level_name}事件 | {cnt:,} |")
    
    # 攻击状态统计
    success = search_raw("appname:sip (sip.attack_state:成功 OR sip.attack_state:攻击成功)", limit=1).get('total_hits', 0)
    blocked = search_raw("appname:sip sip.attack_state:阻断", limit=1).get('total_hits', 0)
    print(f"| ✅ 攻击成功 | {success:,} |")
    print(f"| 🚫 已阻断 | {blocked:,} |")
    print()
    
    # ===== 2. 攻击类型分析 =====
    print("## 二、攻击类型分析（TOP10）")
    print()
    result = search_raw("appname:sip sip.attack_type_name:*", limit=100)
    type_counts = {}
    for row in result.get('rows', []):
        t = extract_field(row, 'sip.attack_type_name')
        if t:
            type_counts[t] = type_counts.get(t, 0) + 1
    sorted_types = sorted(type_counts.items(), key=lambda x: -x[1])[:10]
    
    if sorted_types:
        print("| 排名 | 攻击类型 | 事件数 | 占比 |")
        print("|------|---------|--------|------|")
        for i, (name, cnt) in enumerate(sorted_types, 1):
            pct = f"{cnt/total_hits*100:.1f}%" if total_hits > 0 else "N/A"
            print(f"| {i} | {name} | {cnt:,} | {pct} |")
    else:
        print("（无数据）")
    print()
    
    # ===== 3. 攻击子类型 TOP10 =====
    print("## 三、攻击子类型分析（TOP10）")
    print()
    result = search_raw("appname:sip sip.sub_attack_type_name:*", limit=100)
    sub_counts = {}
    for row in result.get('rows', []):
        t = extract_field(row, 'sip.sub_attack_type_name')
        if t:
            sub_counts[t] = sub_counts.get(t, 0) + 1
    sorted_subs = sorted(sub_counts.items(), key=lambda x: -x[1])[:10]
    
    if sorted_subs:
        print("| 排名 | 攻击子类型 | 事件数 |")
        print("|------|-----------|--------|")
        for i, (name, cnt) in enumerate(sorted_subs, 1):
            print(f"| {i} | {name} | {cnt:,} |")
    else:
        print("（无数据）")
    print()
    
    # ===== 4. TOP攻击源IP =====
    print("## 四、TOP20 攻击源IP")
    print()
    result = search_raw("appname:sip sip.attack_ip:*", limit=100)
    src_counts = {}
    for row in result.get('rows', []):
        ip = extract_field(row, 'sip.attack_ip')
        country = extract_field(row, 'sip.attack_country')
        province = extract_field(row, 'sip.attack_province')
        if ip and ip != '-':
            key = (ip, country, province)
            src_counts[key] = src_counts.get(key, 0) + 1
    sorted_srcs = sorted(src_counts.items(), key=lambda x: -x[1])[:20]
    
    if sorted_srcs:
        print("| 排名 | 攻击源IP | 攻击次数 | 国家 | 省份 |")
        print("|------|---------|---------|------|------|")
        for i, ((ip, country, province), cnt) in enumerate(sorted_srcs, 1):
            print(f"| {i} | `{ip}` | {cnt:,} | {country or '-'} | {province or '-'} |")
    else:
        print("（无数据）")
    print()
    
    # ===== 5. TOP被攻击目标IP =====
    print("## 五、TOP20 被攻击目标IP")
    print()
    result = search_raw("appname:sip sip.suffer_ip:*", limit=100)
    dst_counts = {}
    for row in result.get('rows', []):
        ip = extract_field(row, 'sip.suffer_ip')
        if ip and ip != '-':
            dst_counts[ip] = dst_counts.get(ip, 0) + 1
    sorted_dsts = sorted(dst_counts.items(), key=lambda x: -x[1])[:20]
    
    if sorted_dsts:
        print("| 排名 | 目标IP | 被攻击次数 |")
        print("|------|--------|-----------|")
        for i, (ip, cnt) in enumerate(sorted_dsts, 1):
            print(f"| {i} | `{ip}` | {cnt:,} |")
    else:
        print("（无数据）")
    print()
    
    # ===== 6. 暴力破解专项分析 =====
    print("## 六、暴力破解专项分析")
    print()
    brute = search_raw("appname:sip sip.sub_attack_type_name:*暴力*", limit=1)
    brute_cnt = brute.get('total_hits', 0)
    print(f"暴力破解事件总数：**{brute_cnt:,}**")
    print()
    
    if brute_cnt > 0:
        # 暴力破解目标TOP10
        result = search_raw("appname:sip sip.sub_attack_type_name:*暴力*", limit=100)
        target_counts = {}
        for row in result.get('rows', []):
            ip = extract_field(row, 'sip.suffer_ip')
            if ip and ip != '-':
                target_counts[ip] = target_counts.get(ip, 0) + 1
        sorted_targets = sorted(target_counts.items(), key=lambda x: -x[1])[:10]
        
        print("**被暴力破解TOP10目标：**")
        print()
        print("| 目标IP | 暴力破解次数 |")
        print("|--------|------------|")
        for ip, cnt in sorted_targets:
            print(f"| `{ip}` | {cnt:,} |")
        
        # 暴力破解源TOP10
        src_counts = {}
        for row in result.get('rows', []):
            ip = extract_field(row, 'sip.attack_ip')
            if ip and ip != '-':
                src_counts[ip] = src_counts.get(ip, 0) + 1
        sorted_srcs = sorted(src_counts.items(), key=lambda x: -x[1])[:10]
        
        print()
        print("**暴力破解源TOP10：**")
        print()
        print("| 源IP | 攻击次数 |")
        print("|------|---------|")
        for ip, cnt in sorted_srcs:
            print(f"| `{ip}` | {cnt:,} |")
    print()
    
    # ===== 7. 漏洞利用分析 =====
    print("## 七、漏洞利用专项分析")
    print()
    vuln = search_raw("appname:sip sip.event_desc:*CVE* OR sip.sub_attack_type_name:*漏洞*", limit=1)
    vuln_cnt = vuln.get('total_hits', 0)
    print(f"漏洞利用事件总数：**{vuln_cnt:,}**")
    print()
    
    if vuln_cnt > 0:
        result = search_raw("appname:sip (sip.event_desc:*CVE* OR sip.sub_attack_type_name:*漏洞*)", limit=100)
        vuln_details = {}
        for row in result.get('rows', []):
            desc = extract_field(row, 'sip.event_desc', 'sip.sub_attack_type_name')
            if desc:
                vuln_details[desc] = vuln_details.get(desc, 0) + 1
        sorted_vulns = sorted(vuln_details.items(), key=lambda x: -x[1])[:10]
        
        print("| 漏洞/事件 | 出现次数 |")
        print("|----------|---------|")
        for name, cnt in sorted_vulns:
            display = name[:80] + '...' if len(name) > 80 else name
            print(f"| {display} | {cnt:,} |")
    print()
    
    # ===== 8. 攻击成功事件详情 =====
    print("## 八、攻击成功事件（需重点关注）")
    print()
    if success > 0:
        result = search_raw("appname:sip (sip.attack_state:成功 OR sip.attack_state:攻击成功)", limit=50)
        print(f"共 {success} 条攻击成功事件，以下为部分详情：")
        print()
        for i, row in enumerate(result.get('rows', [])[:20], 1):
            attack_ip = extract_field(row, 'sip.attack_ip')
            suffer_ip = extract_field(row, 'sip.suffer_ip')
            attack_type = extract_field(row, 'sip.attack_type_name')
            sub_type = extract_field(row, 'sip.sub_attack_type_name')
            country = extract_field(row, 'sip.attack_country')
            desc = extract_field(row, 'sip.event_desc', 'sip.brief')
            
            print(f"**{i}. {sub_type or attack_type}**")
            print(f"   - 攻击源：`{attack_ip}`（{country or '未知'}）")
            print(f"   - 目标：`{suffer_ip}`")
            if desc and desc != '-':
                display = desc[:150] + '...' if len(desc) > 150 else desc
                print(f"   - 描述：{display}")
            print()
    else:
        print("✅ 近24小时内无攻击成功事件")
    print()
    
    # ===== 9. 小时趋势分析 =====
    print("## 九、攻击时间分布（按小时）")
    print()
    hourly = {}
    for h in range(24):
        h_start = (now - timedelta(hours=24-h)).strftime('%Y-%m-%d %H:00')
        h_end = (now - timedelta(hours=23-h)).strftime('%Y-%m-%d %H:00')
        query = f'appname:sip @d("{h_start}","{h_end}")'
        r = search_raw(query, limit=1)
        hourly[h] = r.get('total_hits', 0)
    
    max_cnt = max(hourly.values()) if hourly.values() else 1
    print("| 时段 | 事件数 | 趋势 |")
    print("|------|--------|------|")
    for h, cnt in hourly.items():
        bar_len = int(cnt / max_cnt * 20) if max_cnt > 0 else 0
        bar = '█' * bar_len + '░' * (20 - bar_len)
        print(f"| {h:02d}:00 | {cnt:,} | {bar} |")
    print()
    
    # ===== 10. 运营建议 =====
    print("## 十、运营建议")
    print()
    
    suggestions = []
    
    if success > 0:
        suggestions.append(f"🚨 **{success}条攻击成功事件需立即排查**，建议逐一确认影响范围并处置")
    
    if brute_cnt > 0:
        suggestions.append(f"⚠️ 暴力破解攻击频繁（{brute_cnt:,}次），建议：\n  1. 检查被攻击目标的密码复杂度\n  2. 考虑封堵高频暴力破解源IP\n  3. 启用登录失败锁定策略")
    
    if levels.get("高危", 0) > 100:
        suggestions.append(f"🔴 高危事件较多（{levels.get('高危',0):,}次），建议优先处理高危告警")
    
    if total_hits > 0 and sorted_dsts:
        top_target, top_cnt = sorted_dsts[0]
        if top_cnt > total_hits * 0.3:
            suggestions.append(f"🎯 目标 `{top_target}` 承受了 {top_cnt/total_hits*100:.1f}% 的攻击，建议重点加固")
    
    if sorted_srcs:
        top_src = sorted_srcs[0][0][0] if isinstance(sorted_srcs[0][0], tuple) else sorted_srcs[0][0]
        suggestions.append(f"🌐 攻击源IP `{top_src}` 活跃度最高，建议加入防火墙黑名单观察")
    
    if not suggestions:
        suggestions.append("✅ 近24小时安全态势整体平稳，无重大安全事件")
    
    for i, s in enumerate(suggestions, 1):
        print(f"{i}. {s}")
    
    print()
    print("---")
    print()
    print(f"*报告由 OpenClaw 自动生成 | 数据统计截至 {report_time}*")

if __name__ == '__main__':
    main()
