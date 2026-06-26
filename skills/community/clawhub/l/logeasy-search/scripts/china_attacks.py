#!/usr/bin/env python3
"""分析114条有国家标注的SIP告警"""
import sys, io, json, urllib.request, urllib.parse, base64, collections, re
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

RIZHIYI = 'http://10.20.51.16'
AUTH = base64.b64encode(b'admin:MIma@sec2025').decode()
headers = {'Authorization': f'Basic {AUTH}', 'Content-Type': 'application/json'}

params = {'query': 'appname:sip sip.attack_country:"中国" NOT sip.attack_province:"未知"',
          'time_range': 'now-24h,now', 'index_name': 'yotta', 'limit': 100}
url = f"{RIZHIYI}/api/v3/search/sheets/?{urllib.parse.urlencode(params)}"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=120) as resp:
    r = json.loads(resp.read().decode('utf-8'))

total = r['results']['total_hits']
rows = r['results']['sheets']['rows']
print(f"Total: {total}, Rows: {len(rows)}")

# 看第一行所有字段
print("\n=== Row 0 ALL fields ===")
row = rows[0]
for k, v in sorted(row.items()):
    if k.startswith('sip.') and v is not None and str(v) not in ('', '0', 'None'):
        sv = str(v)[:200]
        print(f"  {k}: {sv}")

# 看raw_message
print("\n=== raw_message (row 0) ===")
print(row.get('raw_message', '')[:2000])

# 统计
print("\n\n=== 统计 ===")
suffer_ips = collections.Counter()
attack_types = collections.Counter()
modules = collections.Counter()
countries = collections.Counter()
provinces = collections.Counter()
reliabilities = collections.Counter()
threats = collections.Counter()
statuses = collections.Counter()
host_risks = collections.Counter()
source_ips = collections.Counter()  # from raw_message

for row in rows:
    s = str(row.get('sip.suffer_ip', ''))
    if s and s != '0': suffer_ips[s] += 1
    t = str(row.get('sip.sub_attack_type_name', ''))
    if t: attack_types[t] += 1
    m = str(row.get('sip.module_type_name', ''))
    if m: modules[m] += 1
    c = str(row.get('sip.attack_country', ''))
    if c: countries[c] += 1
    p = str(row.get('sip.attack_province', ''))
    if p: provinces[p] += 1
    rel = str(row.get('sip.reliability', ''))
    if rel: reliabilities[rel] += 1
    th = str(row.get('sip.threat_level', ''))
    if th: threats[th] += 1
    st = row.get('sip.status_code', '')
    if st:
        sc = str(st) if not isinstance(st, list) else '+'.join(str(x) for x in st)
        statuses[sc] += 1
    hr = str(row.get('sip.hostRisk', ''))
    if hr: host_risks[hr] += 1

    # 从 raw 提取所有IP
    raw = row.get('raw_message', '')
    for m in re.finditer(r'"(ip|src_ip|source_ip|client_ip|remote_addr|attack_ip)"\s*:\s*"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"', raw):
        source_ips[m.group(2)] += 1

print(f"\n## 被攻击目标 (suffer_ip) TOP:")
for ip, cnt in suffer_ips.most_common(15):
    print(f"  {cnt:4d} {ip}")

print(f"\n## 攻击类型:")
for t, cnt in attack_types.most_common(10):
    print(f"  {cnt:4d} {t}")

print(f"\n## 攻击模块:")
for m, cnt in modules.most_common():
    print(f"  {cnt:4d} {m}")

print(f"\n## 来源省份:")
for p, cnt in provinces.most_common(10):
    print(f"  {cnt:4d} {p}")

print(f"\n## 来源国家:")
for c, cnt in countries.most_common(10):
    print(f"  {cnt:4d} {c}")

print(f"\n## 可信度:")
rel_map = {'1': '低', '2': '中', '3': '高'}
for r2, cnt in reliabilities.most_common():
    print(f"  {rel_map.get(r2, r2)}: {cnt}")

print(f"\n## 威胁等级:")
th_map = {'1': '高危', '2': '中危', '3': '低危', '4': '信息'}
for t2, cnt in threats.most_common():
    print(f"  {th_map.get(t2, t2)}: {cnt}")

print(f"\n## HTTP状态码:")
for sc, cnt in statuses.most_common(10):
    print(f"  {cnt:4d} {sc}")

print(f"\n## 资产风险标注:")
for hr, cnt in host_risks.most_common(5):
    print(f"  {cnt:4d} {hr[:100]}")

print(f"\n## raw_message中提取的IP (可能含攻击源):")
for ip, cnt in source_ips.most_common(20):
    print(f"  {cnt:4d} {ip}")
