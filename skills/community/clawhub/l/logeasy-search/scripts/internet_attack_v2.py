#!/usr/bin/env python3
"""态势感知互联网攻击分析 - 通过 raw_message 提取攻击源"""
import sys, io, json, urllib.request, urllib.parse, base64, collections, re
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

RIZHIYI = 'http://10.20.51.16'
AUTH = base64.b64encode(b'admin:MIma@sec2025').decode()
headers = {'Authorization': f'Basic {AUTH}', 'Content-Type': 'application/json'}
INTERNAL_PREFIXES = ('10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.',
    '172.21.', '172.22.', '172.23.', '172.24.', '172.25.', '172.26.', '172.27.',
    '172.28.', '172.29.', '172.30.', '172.31.', '192.168.', '127.', '0.', '-')

def is_internal(ip):
    if not ip: return True
    return any(ip.startswith(p) for p in INTERNAL_PREFIXES)

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

# 1. 搜一批原始日志
print("\n[1/5] 获取态势感知日志...")
r = search('appname:sip', limit=100)
total = r.get('results', {}).get('total_hits', 0)
rows = r.get('results', {}).get('sheets', {}).get('rows', [])
print(f"  总告警数: {total} | 获取: {len(rows)} 条")

# 2. 从 raw_message 解析攻击源IP和关键字段
print("\n[2/5] 解析攻击数据...")
internet_attacks = []  # 互联网攻击
internal_attacks = []
unknown_attacks = []
attack_types = collections.Counter()
internet_attack_types = collections.Counter()
suffer_ips = collections.Counter()
internet_suffer = collections.Counter()
reliability_dist = collections.Counter()
threat_dist = collections.Counter()
module_dist = collections.Counter()
http_codes = collections.Counter()
internet_http = collections.Counter()
countries = collections.Counter()
internet_countries = collections.Counter()
host_risks = collections.Counter()

for row in rows:
    raw = row.get('raw_message', '')
    # 从 raw_message 的 JSON 中提取
    try:
        json_start = raw.find('{')
        if json_start > 0:
            detail = json.loads(raw[json_start:])
        else:
            detail = {}
    except:
        detail = {}
        try:
            # syslog 格式: timestamp|tag|host|{json}
            parts = raw.split('|')
            for p in parts:
                if p.strip().startswith('{'):
                    detail = json.loads(p)
                    break
        except:
            pass

    # 提取攻击源IP
    attack_ip = detail.get('ip', '') or row.get('sip.attack_ip', '')
    if not attack_ip or attack_ip in ('-', ''): 
        # 尝试从 X-Forwarded-For 第一个IP取
        xff = detail.get('X-Forwarded-For', '') or detail.get('x_forwarded_for', '')
        if xff:
            attack_ip = xff.split(',')[0].strip() if ',' in str(xff) else str(xff)

    # 提取受害IP
    suffer_ip = row.get('sip.suffer_ip', '') or ''
    
    # 提取其他字段
    atk_type = row.get('sip.sub_attack_type_name', '')
    module = row.get('sip.module_type_name', '')
    reliability = str(row.get('sip.reliability', ''))
    threat = str(row.get('sip.threat_level', ''))
    status_code = row.get('sip.status_code', '')
    country = detail.get('attack_country', '') or row.get('sip.attack_country', '') or ''
    host_risk = row.get('sip.hostRisk', '') or ''
    attack_state = str(row.get('sip.attack_state', ''))

    # 统计攻击类型
    if atk_type:
        attack_types[atk_type] += 1
    
    # 统计模块
    if module:
        module_dist[module] += 1
    
    # 统计可信度
    if reliability:
        reliability_dist[reliability] += 1
    
    # 统计威胁等级
    if threat:
        threat_dist[threat] += 1
    
    # 统计HTTP状态码
    if status_code:
        code_str = str(status_code) if not isinstance(status_code, list) else '+'.join(str(c) for c in status_code)
        http_codes[code_str] += 1
    
    # 统计国家
    if country and country not in ('未知', '', '-', '0'):
        countries[country] += 1

    # 分类
    attack_data = {
        'ip': attack_ip, 'suffer': suffer_ip, 'type': atk_type,
        'module': module, 'reliability': reliability, 'threat': threat,
        'status': status_code, 'country': country, 'risk': host_risk,
        'state': attack_state, 'detail': detail
    }

    if not attack_ip or attack_ip in ('', '-', '未知'):
        unknown_attacks.append(attack_data)
    elif is_internal(attack_ip):
        internal_attacks.append(attack_data)
        if suffer_ip:
            suffer_ips[suffer_ip] += 1
    else:
        internet_attacks.append(attack_data)
        internet_attack_types[atk_type] += 1
        if suffer_ip:
            internet_suffer[suffer_ip] += 1
        internet_http[str(status_code) if not isinstance(status_code, list) else '+'.join(str(c) for c in status_code)] += 1
        if country and country not in ('未知', '', '-', '0'):
            internet_countries[country] += 1

# 3. 输出结果
print("\n" + "=" * 60)
print("## 📊 攻击源分布")
print("=" * 60)
print(f"  总告警: {total}")
print(f"  本次采样: {len(rows)} 条")
print(f"  内网攻击: {len(internal_attacks)} ({len(internal_attacks)/len(rows)*100:.1f}%)")
print(f"  互联网攻击: {len(internet_attacks)} ({len(internet_attacks)/len(rows)*100:.1f}%)")
print(f"  未知/其他: {len(unknown_attacks)} ({len(unknown_attacks)/len(rows)*100:.1f}%)")

# 互联网攻击详情
if internet_attacks:
    print(f"\n## 🌐 互联网攻击详情")
    print(f"  总计: {len(internet_attacks)} 条 (采样)")
    
    # 互联网攻击源IP TOP 15
    ip_counter = collections.Counter(a['ip'] for a in internet_attacks)
    print(f"\n  ### 攻击源 IP TOP 15")
    for ip, cnt in ip_counter.most_common(15):
        bar = '█' * min(cnt * 3, 40)
        print(f"    {cnt:4d} {bar} {ip}")
    
    # 互联网攻击的国家分布
    if internet_countries:
        print(f"\n  ### 攻击来源国家/地区")
        for country, cnt in internet_countries.most_common(10):
            print(f"    {cnt:4d} — {country}")
    
    # 互联网攻击类型
    if internet_attack_types:
        print(f"\n  ### 互联网攻击类型")
        for t, cnt in internet_attack_types.most_common(10):
            print(f"    {cnt:4d} — {t}")
    
    # 互联网攻击受害目标
    if internet_suffer:
        print(f"\n  ### 被攻击的内网目标")
        for ip, cnt in internet_suffer.most_common(10):
            bar = '█' * min(cnt * 3, 30)
            print(f"    {cnt:4d} {bar} {ip}")
    
    # 互联网攻击 HTTP 状态码
    if internet_http:
        print(f"\n  ### 互联网攻击 HTTP 状态码")
        for code, cnt in internet_http.most_common(5):
            print(f"    {cnt:4d} — {code}")
    
    # 高可信度互联网攻击
    high_rel = [a for a in internet_attacks if a['reliability'] in ('3', '2')]
    print(f"\n  ### 高/中可信度互联网攻击: {len(high_rel)} 条")
    if high_rel:
        # 按攻击源聚合
        hr_ips = collections.Counter(a['ip'] for a in high_rel)
        for ip, cnt in hr_ips.most_common(10):
            rel = '高' if any(a['reliability'] == '3' for a in high_rel if a['ip'] == ip) else '中'
            types = set(a['type'] for a in high_rel if a['ip'] == ip and a['type'])
            print(f"    {cnt:4d} [{rel}] {ip} — 攻击类型: {', '.join(types) or '未知'}")
else:
    print(f"\n  ⚠️ 本次采样的 {len(rows)} 条中未发现明确的互联网攻击源IP")
    print(f"  大部分告警的攻击源字段 (sip.ip) 为空或内网IP")

# 总体攻击类型分布
print(f"\n{'=' * 60}")
print("## ⚔️ 全部攻击类型分布 TOP 10")
for t, cnt in attack_types.most_common(10):
    pct = cnt / len(rows) * 100
    bar = '█' * int(pct)
    print(f"  {cnt:4d} ({pct:5.1f}%) {bar} {t}")

# 攻击模块
print(f"\n## 📦 攻击模块分布")
for m, cnt in module_dist.most_common():
    pct = cnt / len(rows) * 100
    print(f"  {cnt:4d} ({pct:5.1f}%) — {m}")

# 可信度
print(f"\n## 🛡️ 可信度分布")
rel_map = {'1': '低', '2': '中', '3': '高'}
for rel, cnt in reliability_dist.most_common():
    label = rel_map.get(rel, f'等级{rel}')
    pct = cnt / len(rows) * 100
    print(f"  {label}: {cnt} ({pct:.1f}%)")

# 威胁等级
print(f"\n## ⚠️ 威胁等级")
threat_map = {'1': '🔴 高危', '2': '🟠 中危', '3': '🟡 低危', '4': '🔵 信息'}
for t, cnt in threat_dist.most_common():
    label = threat_map.get(t, f'等级{t}')
    pct = cnt / len(rows) * 100
    print(f"  {label}: {cnt} ({pct:.1f}%)")

# HTTP 状态码
print(f"\n## 📡 HTTP 状态码 TOP 5")
for code, cnt in http_codes.most_common(5):
    print(f"  {cnt:4d} — {code}")

# 受害目标
print(f"\n## 🎯 内网被攻击目标 TOP 10")
for ip, cnt in suffer_ips.most_common(10):
    bar = '█' * min(cnt * 2, 30)
    print(f"  {cnt:4d} {bar} {ip}")

# 总结
print(f"\n{'=' * 60}")
print("## 📋 总结")
print("=" * 60)
print(f"\n  SIP 24h 总告警: {total}")
print(f"  采样分析: {len(rows)} 条")
print(f"  内网源: {len(internal_attacks)} | 互联网源: {len(internet_attacks)} | 未知: {len(unknown_attacks)}")

if internet_attacks:
    print(f"\n  🔴 互联网攻击概况:")
    top_ip = ip_counter.most_common(1)[0]
    print(f"    • 主要攻击源: {top_ip[0]} ({top_ip[1]}次)")
    if internet_countries:
        top_country = internet_countries.most_common(1)[0]
        print(f"    • 主要来源: {top_country[0]} ({top_country[1]}次)")
    if internet_suffer:
        top_target = internet_suffer.most_common(1)[0]
        print(f"    • 主要目标: {top_target[0]} ({top_target[1]}次)")
    high_danger = [a for a in internet_attacks if a['reliability'] == '3' and a['threat'] == '1']
    print(f"    • 高危高可信: {len(high_danger)} 次")
    success = [a for a in internet_attacks if isinstance(a['status'], int) and a['status'] == 200]
    print(f"    • HTTP 200 (可能成功): {len(success)} 次")
else:
    print(f"\n  ⚠️ 本次采样中未发现互联网攻击")
    print(f"  攻击主要集中在内网，可能需要更大采样量或换查询条件")
