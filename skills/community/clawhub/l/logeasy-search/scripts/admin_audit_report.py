#!/usr/bin/env python3
"""飞廉 admin_audit_log 分析报告"""
import sys, io, json, urllib.request, urllib.parse, base64, collections
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

RIZHIYI = 'http://10.20.51.16'
AUTH = base64.b64encode(b'admin:MIma@sec2025').decode()
headers = {'Authorization': f'Basic {AUTH}', 'Content-Type': 'application/json'}

def search(query, time_range='now-7d,now', limit=100):
    params = {'query': query, 'time_range': time_range, 'index_name': 'yotta', 'limit': limit}
    url = f"{RIZHIYI}/api/v3/search/sheets/?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode('utf-8'))

print("=" * 60)
print("🔍 飞廉 admin_audit_log — 分析报告")
print(f"  统计周期: 最近7天")
print(f"  报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 60)

# 获取数据
r = search('feilian.content.x_key:admin_audit_log', limit=100)
total = r['results']['total_hits']
rows = r['results']['sheets']['rows']
print(f"\n  总日志: {total} | 采样: {len(rows)} 条")

# 先看字段结构
print("\n## 📋 字段概览")
all_keys = set()
for row in rows:
    all_keys.update(row.keys())
content_keys = sorted(k for k in all_keys if k.startswith('feilian.content.'))
other_keys = sorted(k for k in all_keys if not k.startswith('feilian.') and k not in ('raw_message', 'source', 'tag', 'hostname', 'appname', 'logtype', '_index'))
print(f"  feilian.content.* 字段: {len(content_keys)}")
print(f"  其他字段: {other_keys}")

# 统计
print("\n## 📊 数据分析")

# 按日期分布
dates = collections.Counter()
for row in rows:
    raw = row.get('raw_message', '')
    # 提取日期
    try:
        idx = raw.find('{')
        if idx >= 0:
            detail = json.loads(raw[idx:])
        else:
            detail = {}
    except:
        detail = {}
    t = detail.get('time', '') or row.get('feilian.time', '') or row.get('timestamp', '')
    if t:
        dt = str(t)[:10]
        dates[dt] += 1

if dates:
    print(f"\n### 日期分布")
    for d, cnt in sorted(dates.items()):
        bar = '█' * min(cnt * 2, 40)
        print(f"  {d}  {cnt:4d} {bar}")

# 各字段分布
print(f"\n### feilian.content.* 字段值分布")
field_stats = collections.defaultdict(collections.Counter)
for row in rows:
    for k in content_keys:
        v = row.get(k, None)
        if v is not None and str(v) not in ('', '0', 'None', '-', '[]'):
            field_stats[k][str(v)[:100]] += 1

for k, cnt in field_stats.items():
    unique = len(cnt)
    short_name = k.replace('feilian.content.', '')
    if unique <= 20:
        print(f"\n  [{short_name}] ({unique} 种)")
        for val, c in cnt.most_common(10):
            bar = '█' * min(c, 25)
            print(f"    {c:4d} {bar} {val}")
    else:
        print(f"\n  [{short_name}] ({unique} 种) TOP 5:")
        for val, c in cnt.most_common(5):
            print(f"    {c:4d} {val}")

# raw_message 样本
print(f"\n## 📝 raw_message 样本")
for i, row in enumerate(rows[:3], 1):
    raw = row.get('raw_message', '')
    print(f"\n--- 样本 {i} ---")
    print(raw[:600])
