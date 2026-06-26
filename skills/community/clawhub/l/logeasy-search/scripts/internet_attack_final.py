#!/usr/bin/env python3
"""态势感知(SIP)互联网攻击完整报告 - 使用正确字段 sip.attack_ip"""
import sys, io, json, urllib.request, urllib.parse, base64, collections
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

RIZHIYI = 'http://10.20.51.16'
AUTH = base64.b64encode(b'admin:MIma@sec2025').decode()
headers = {'Authorization': f'Basic {AUTH}', 'Content-Type': 'application/json'}

INTERNAL = ('10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.',
    '172.21.', '172.22.', '172.23.', '172.24.', '172.25.', '172.26.', '172.27.',
    '172.28.', '172.29.', '172.30.', '172.31.', '192.168.', '127.')

def is_internal(ip):
    if not ip or ip in ('-', '', '未知', '0'): return 'unknown'
    return 'internal' if any(ip.startswith(p) for p in INTERNAL) else 'internet'

def search(query, time_range='now-24h,now', limit=100):
    params = {'query': query, 'time_range': time_range, 'index_name': 'yotta', 'limit': limit}
    url = f"{RIZHIYI}/api/v3/search/sheets/?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode('utf-8'))

print("=" * 60)
print("🔍 态势感知(SIP) — 互联网攻击分析报告")
print(f"  统计周期: 最近24小时")
print(f"  报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 60)

# ========== 搜索所有SIP告警 ==========
print("\n[1/4] 获取SIP态势感知全量告警...")
r = search('appname:sip', limit=100)
total = r['results']['total_hits']
rows = r['results']['sheets']['rows']
print(f"  总告警: {total} | 采样: {len(rows)} 条")

# ========== 分类统计 ==========
print("\n[2/4] 分类分析攻击源...")
internet = []    # 互联网
internal = []    # 内网
unknown_list = []

atk_types = collections.Counter()
atk_types_net = collections.Counter()
suffer_ips = collections.Counter()
suffer_net = collections.Counter()
countries = collections.Counter()
provinces = collections.Counter()
modules = collections.Counter()
modules_net = collections.Counter()
rel = collections.Counter()
rel_net = collections.Counter()
threat = collections.Counter()
threat_net = collections.Counter()
statuses = collections.Counter()
statuses_net = collections.Counter()
src_ips = collections.Counter()
src_ips_net = collections.Counter()
events = collections.Counter()
events_net = collections.Counter()

for row in rows:
    aip = str(row.get('sip.attack_ip', '') or '')
    sip = str(row.get('sip.suffer_ip', '') or '')
    at = str(row.get('sip.sub_attack_type_name', '') or '')
    atn = str(row.get('sip.attack_type_name', '') or '')
    mod = str(row.get('sip.module_type_name', '') or '')
    r_val = str(row.get('sip.reliability', '') or '')
    t_val = str(row.get('sip.threat_level', '') or '')
    st = row.get('sip.status_code', '')
    cn = str(row.get('sip.attack_country', '') or '')
    pv = str(row.get('sip.attack_province', '') or '')
    event = str(row.get('sip.event_desc', '') or '')
    risk = str(row.get('sip.hostRisk', '') or '')
    branch = str(row.get('sip.suffer_branch_name', '') or '')
    inv = str(row.get('sip.invasion_stage', '') or '')

    entry = {
        'ip': aip, 'suffer': sip, 'type': at, 'type_name': atn,
        'module': mod, 'rel': r_val, 'threat': t_val,
        'status': st, 'country': cn, 'province': pv,
        'event': event, 'risk': risk, 'branch': branch, 'inv': inv
    }

    # 总统计
    if at: atk_types[at] += 1
    if atn: events[atn] += 1
    if mod: modules[mod] += 1
    if r_val: rel[r_val] += 1
    if t_val: threat[t_val] += 1
    if cn and cn not in ('未知', '', '-'): countries[cn] += 1
    if pv and pv not in ('未知', '', '-'): provinces[pv] += 1
    sc = str(st) if not isinstance(st, list) else '+'.join(str(x) for x in st)
    if sc: statuses[sc] += 1
    if sip and sip != '0': suffer_ips[sip] += 1
    if aip and aip not in ('', '-', '0'): src_ips[aip] += 1

    # 分类
    cat = is_internal(aip)
    if cat == 'internet':
        internet.append(entry)
        if at: atk_types_net[at] += 1
        if mod: modules_net[mod] += 1
        if r_val: rel_net[r_val] += 1
        if t_val: threat_net[t_val] += 1
        if cn and cn not in ('未知', '', '-'): countries[cn] += 1
        if pv and pv not in ('未知', '', '-'): provinces[pv] += 1
        if sc: statuses_net[sc] += 1
        if sip and sip != '0': suffer_net[sip] += 1
        src_ips_net[aip] += 1
        if event: events_net[event] += 1
    elif cat == 'internal':
        internal.append(entry)
    else:
        unknown_list.append(entry)

internal_total = len(internal)
internet_total = len(internet)
unknown_total = len(unknown_list)

# ========== 搜索有国家标注的（补充互联网数据）==========
print("[3/4] 补充搜索有国家标注的告警...")
r2 = search('appname:sip sip.attack_country:"中国" NOT sip.attack_province:"未知"', limit=100)
extra_total = r2['results']['total_hits']
extra_rows = r2['results']['sheets']['rows']
print(f"  有国家标注（排除未知省份）: {extra_total} 条")

extra_net_ips = collections.Counter()
extra_net_suffer = collections.Counter()
extra_events = collections.Counter()
extra_provinces = collections.Counter()

for row in extra_rows:
    aip = str(row.get('sip.attack_ip', '') or '')
    sip = str(row.get('sip.suffer_ip', '') or '')
    event = str(row.get('sip.event_desc', '') or '')
    pv = str(row.get('sip.attack_province', '') or '')
    if aip:
        extra_net_ips[aip] += 1
    if sip and sip != '0': extra_net_suffer[sip] += 1
    if event: extra_events[event] += 1
    if pv and pv != '未知': extra_provinces[pv] += 1

# ========== 输出报告 ==========
print("\n[4/4] 生成报告...\n")

print(f"{'=' * 60}")
print("## 📊 攻击源分布概览")
print(f"{'=' * 60}")
print(f"  SIP 24h 总告警: {total}")
print(f"  本次采样: {len(rows)} 条")
print(f"  ┌ 互联网攻击: {internet_total} ({internet_total/len(rows)*100:.1f}%)")
print(f"  ├ 内网攻击:   {internal_total} ({internal_total/len(rows)*100:.1f}%)")
print(f"  └ 未知/空:   {unknown_total} ({unknown_total/len(rows)*100:.1f}%)")
print(f"\n  有国家标注的告警: {extra_total} 条 (单独统计)")

# 互联网攻击
print(f"\n{'=' * 60}")
print("## 🌐 互联网攻击详情")
print(f"{'=' * 60}")

if internet:
    print(f"\n### 攻击源 IP TOP 15")
    for ip, cnt in src_ips_net.most_common(15):
        bar = '█' * min(cnt * 4, 40)
        print(f"  {cnt:4d} {bar} {ip}")

    if events_net:
        print(f"\n### 互联网攻击事件类型")
        for ev, cnt in events_net.most_common(10):
            print(f"  {cnt:4d} — {ev[:80]}")

    if atk_types_net:
        print(f"\n### 互联网攻击子类型")
        for t, cnt in atk_types_net.most_common(10):
            if t:
                print(f"  {cnt:4d} — {t}")

    if suffer_net:
        print(f"\n### 被攻击的内网目标")
        for ip, cnt in suffer_net.most_common(10):
            bar = '█' * min(cnt * 3, 30)
            print(f"  {cnt:4d} {bar} {ip}")

    if modules_net:
        print(f"\n### 互联网攻击模块")
        for m, cnt in modules_net.most_common():
            if m: print(f"  {cnt:4d} — {m}")

    if rel_net:
        print(f"\n### 互联网攻击可信度")
        rm = {'1': '低', '2': '中', '3': '高'}
        for r2, cnt in rel_net.most_common():
            print(f"  {rm.get(r2, r2)}: {cnt}")

    if threat_net:
        print(f"\n### 互联网攻击威胁等级")
        tm = {'1': '🔴 高危', '2': '🟠 中危', '3': '🟡 低危', '4': '🔵 信息'}
        for t2, cnt in threat_net.most_common():
            print(f"  {tm.get(t2, t2)}: {cnt}")

    if statuses_net:
        print(f"\n### 互联网攻击 HTTP 状态码")
        for sc, cnt in statuses_net.most_common(5):
            print(f"  {cnt:4d} — {sc}")

    print(f"\n### 互联网攻击详细记录")
    for i, a in enumerate(internet, 1):
        rl = {'3': '高', '2': '中', '1': '低'}.get(a['rel'], '?')
        tl = {'1': '高危', '2': '中危', '3': '低危'}.get(a['threat'], '?')
        sc = str(a['status']) if not isinstance(a['status'], list) else '+'.join(str(x) for x in a['status'])
        print(f"  [{i:2d}] {a['ip']:18s} → {a['suffer']:18s} | {a['type'] or a['type_name'] or '?':20s} | 可信:{rl} 威胁:{tl} | HTTP:{sc}")
        if a['event'] and len(a['event']) > 20:
            print(f"       事件: {a['event'][:100]}")

# 有国家标注的114条（更全面的互联网攻击画像）
print(f"\n{'=' * 60}")
print(f"## 🗺️ 有国家标注的互联网攻击 ({extra_total} 条)")
print(f"{'=' * 60}")

if extra_provinces:
    print(f"\n### 来源省份 TOP 10")
    for pv, cnt in extra_provinces.most_common(10):
        bar = '█' * min(cnt * 2, 40)
        print(f"  {cnt:4d} {bar} {pv}")

if extra_net_ips:
    print(f"\n### 攻击源 IP TOP 15")
    for ip, cnt in extra_net_ips.most_common(15):
        bar = '█' * min(cnt, 30)
        print(f"  {cnt:4d} {bar} {ip}")

if extra_net_suffer:
    print(f"\n### 被攻击目标 TOP 10")
    for ip, cnt in extra_net_suffer.most_common(10):
        bar = '█' * min(cnt, 25)
        print(f"  {cnt:4d} {bar} {ip}")

if extra_events:
    print(f"\n### 攻击事件 TOP 10")
    for ev, cnt in extra_events.most_common(10):
        print(f"  {cnt:4d} — {ev[:80]}")

# 全局统计
print(f"\n{'=' * 60}")
print("## 📈 全局攻击统计")
print(f"{'=' * 60}")

print(f"\n### 所有攻击模块分布")
for m, cnt in modules.most_common():
    pct = cnt / len(rows) * 100
    print(f"  {cnt:4d} ({pct:5.1f}%) — {m}")

print(f"\n### 所有攻击子类型 TOP 10")
for t, cnt in atk_types.most_common(10):
    pct = cnt / len(rows) * 100
    print(f"  {cnt:4d} ({pct:5.1f}%) — {t}")

print(f"\n### 攻击事件大类 TOP 10")
for ev, cnt in events.most_common(10):
    pct = cnt / len(rows) * 100
    print(f"  {cnt:4d} ({pct:5.1f}%) — {ev[:70]}")

print(f"\n### 被攻击目标 TOP 10（含内网+互联网）")
for ip, cnt in suffer_ips.most_common(10):
    bar = '█' * min(cnt, 25)
    print(f"  {cnt:4d} {bar} {ip}")

# 总结
print(f"\n{'=' * 60}")
print("## 📋 总结")
print(f"{'=' * 60}")

print(f"\n  24h SIP 态势感知告警: {total} 条")
print(f"  采样分析: {len(rows)} 条")
print(f"\n  攻击来源:")
print(f"    • 互联网: {internet_total} 条 ({internet_total/len(rows)*100:.1f}%)")
print(f"    • 内网:   {internal_total} 条 ({internal_total/len(rows)*100:.1f}%)")
print(f"    • 未知:   {unknown_total} 条 ({unknown_total/len(rows)*100:.1f}%)")
print(f"    • 有国家标注: {extra_total} 条（独立统计，含省份信息）")

if internet:
    top_src = src_ips_net.most_common(3)
    print(f"\n  互联网攻击主要来源:")
    for ip, cnt in top_src:
        print(f"    • {ip} ({cnt}次)")

if extra_net_suffer:
    top_tgt = extra_net_suffer.most_common(3)
    print(f"\n  互联网攻击主要目标:")
    for ip, cnt in top_tgt:
        print(f"    • {ip} ({cnt}次)")

# 风险评估
high_danger = [a for a in internet if a['rel'] == '3' and a['threat'] == '1']
success_200 = [a for a in internet if isinstance(a['status'], int) and a['status'] == 200]
print(f"\n  风险指标:")
print(f"    • 高可信高危: {len(high_danger)} 条")
print(f"    • HTTP 200 (可能成功): {len(success_200)} 条")

# 建议
print(f"\n  💡 建议:")
if internal_total > internet_total:
    print(f"    1. 内网攻击占比 {internal_total/len(rows)*100:.0f}%，远超互联网，建议排查内网安全扫描/测试行为")
print(f"    2. 114条有国家标注的互联网攻击需持续关注")
if extra_net_suffer:
    print(f"    3. {extra_net_suffer.most_common(1)[0][0]} 是互联网攻击最集中目标，建议重点防护")
