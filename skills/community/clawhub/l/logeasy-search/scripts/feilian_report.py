#!/usr/bin/env python3
"""飞廉(feilian)日志 24h 分析报告"""
import sys, io, json, urllib.request, urllib.parse, base64, collections, re
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

RIZHIYI = 'http://10.20.51.16'
AUTH = base64.b64encode(b'admin:MIma@sec2025').decode()
headers = {'Authorization': f'Basic {AUTH}', 'Content-Type': 'application/json'}

def search(query, time_range='now-24h,now', limit=100):
    params = {'query': query, 'time_range': time_range, 'index_name': 'yotta', 'limit': limit}
    url = f"{RIZHIYI}/api/v3/search/sheets/?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode('utf-8'))

print("=" * 60)
print("🔍 飞廉(Feilian)日志 — 24h 分析报告")
print(f"  统计周期: 最近24小时")
print(f"  报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 60)

# 1. 获取总量
print("\n[1/3] 获取飞廉日志...")
r = search('logtype:feilian', limit=100)
total = r.get('results', {}).get('total_hits', 0)
rows = r.get('results', {}).get('sheets', {}).get('rows', [])
print(f"  总日志数: {total} | 获取: {len(rows)} 条")

if total == 0:
    print("  无飞廉日志")
    sys.exit(0)

# 2. 查看所有字段名
all_keys = set()
for row in rows:
    all_keys.update(row.keys())
feilian_keys = sorted(k for k in all_keys if not k.startswith('_') and k not in ('raw_message', 'source', 'tag', 'hostname', 'appname', 'logtype'))
print(f"  飞廉字段数: {len(feilian_keys)}")

# 3. 统计各字段
print("\n[2/3] 分析字段分布...")

# 收集所有字段值
field_values = collections.defaultdict(collections.Counter)
field_types = {}  # field -> type

for row in rows:
    for k in feilian_keys:
        v = row.get(k, None)
        if v is not None and str(v) not in ('', '0', 'None', '-', '未知'):
            sv = str(v)
            field_values[k][sv[:80]] += 1
            field_types[k] = type(v).__name__

# 4. 解析 raw_message
print("\n[3/3] 解析 raw_message...")

raw_ips_src = collections.Counter()
raw_ips_dst = collections.Counter()
raw_events = collections.Counter()
raw_ports_dst = collections.Counter()
raw_details = []  # 保存前5条详细

for i, row in enumerate(rows):
    raw = row.get('raw_message', '')
    
    # syslog 格式，提取 JSON
    detail = {}
    try:
        idx = raw.find('{')
        if idx >= 0:
            detail = json.loads(raw[idx:])
    except:
        try:
            for part in raw.split('|'):
                if part.strip().startswith('{'):
                    detail = json.loads(part)
                    break
        except:
            pass
    
    # 提取IP
    src_ip = detail.get('src_ip', '') or detail.get('client_ip', '') or detail.get('source_ip', '') or ''
    dst_ip = detail.get('dst_ip', '') or detail.get('dest_ip', '') or detail.get('server_ip', '') or detail.get('target_ip', '') or ''
    dst_port = detail.get('dst_port', '') or detail.get('dest_port', '') or detail.get('server_port', '') or ''
    
    if src_ip and src_ip != '0': raw_ips_src[src_ip] += 1
    if dst_ip and dst_ip != '0': raw_ips_dst[dst_ip] += 1
    if dst_port and dst_port != '0': raw_ports_dst[str(dst_port)] += 1
    
    # 事件类型
    event = detail.get('event_type', '') or detail.get('action', '') or detail.get('event_name', '') or ''
    if event: raw_events[event] += 1
    
    # 保存前5条详情
    if i < 3:
        raw_details.append({
            'raw': raw[:500],
            'detail_keys': list(detail.keys())[:30],
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'dst_port': dst_port
        })

# ========== 输出报告 ==========
print(f"\n{'=' * 60}")
print("## 📊 飞廉日志概览")
print(f"{'=' * 60}")
print(f"  24h 总量: {total}")
print(f"  采样: {len(rows)} 条")

# 字段统计（取值少于20个的显示分布）
print(f"\n## 📋 字段分布（高基数字段已折叠）")
for k, cnt in field_values.items():
    unique = len(cnt)
    if unique <= 15:
        print(f"\n  [{k}] ({unique} 种取值)")
        for val, c in cnt.most_common(10):
            bar = '█' * min(c, 30)
            print(f"    {c:4d} {bar} {val}")
    elif unique <= 50:
        print(f"\n  [{k}] ({unique} 种取值) TOP 5:")
        for val, c in cnt.most_common(5):
            print(f"    {c:4d} {val}")

# raw_message 解析结果
print(f"\n{'=' * 60}")
print("## 🌐 网络连接分析（从 raw_message 提取）")
print(f"{'=' * 60}")

if raw_ips_src:
    print(f"\n### 源 IP TOP 15")
    for ip, cnt in raw_ips_src.most_common(15):
        bar = '█' * min(cnt, 30)
        print(f"  {cnt:4d} {bar} {ip}")

if raw_ips_dst:
    print(f"\n### 目标 IP TOP 15")
    for ip, cnt in raw_ips_dst.most_common(15):
        bar = '█' * min(cnt, 30)
        print(f"  {cnt:4d} {bar} {ip}")

if raw_ports_dst:
    print(f"\n### 目标端口 TOP 10")
    for port, cnt in raw_ports_dst.most_common(10):
        # 常见端口映射
        port_map = {'22': 'SSH', '23': 'Telnet', '25': 'SMTP', '53': 'DNS', '80': 'HTTP', '443': 'HTTPS',
                    '445': 'SMB', '1433': 'MSSQL', '3306': 'MySQL', '3389': 'RDP', '6379': 'Redis',
                    '8080': 'HTTP-Proxy', '8443': 'HTTPS-Alt', '9200': 'Elasticsearch', '27017': 'MongoDB'}
        label = port_map.get(port, '')
        print(f"  {cnt:4d} — {port} {label}")

if raw_events:
    print(f"\n### 事件类型")
    for ev, cnt in raw_events.most_common(10):
        print(f"  {cnt:4d} — {ev}")

# raw_message 样本
print(f"\n{'=' * 60}")
print("## 📝 raw_message 样本")
print(f"{'=' * 60}")
for i, d in enumerate(raw_details, 1):
    print(f"\n--- 样本 {i} ---")
    print(f"  src_ip: {d['src_ip']} | dst_ip: {d['dst_ip']} | dst_port: {d['dst_port']}")
    print(f"  JSON字段: {', '.join(d['detail_keys'][:15])}")
    print(f"  raw: {d['raw'][:300]}")

# 时间线
timeline = r.get('results', {}).get('sheets', {}).get('timeline', {})
tl_rows = timeline.get('rows', [])
if tl_rows:
    print(f"\n{'=' * 60}")
    print("## ⏰ 24h 时间线趋势")
    max_cnt = max(row.get('count', 0) for row in tl_rows)
    for row in tl_rows:
        ts = row.get('start_ts', 0)
        cnt = row.get('count', 0)
        hour = datetime.fromtimestamp(ts/1000).strftime('%H:%M')
        bar = '█' * int(cnt / max_cnt * 40) if max_cnt > 0 else ''
        level = '🔴' if cnt > max_cnt * 0.8 else '🟠' if cnt > max_cnt * 0.5 else '🟡' if cnt > max_cnt * 0.2 else '🟢'
        print(f"  {level} {hour}  {cnt:5d} {bar}")
    peak = max(tl_rows, key=lambda x: x.get('count', 0))
    peak_time = datetime.fromtimestamp(peak['start_ts']/1000).strftime('%H:%M')
    print(f"  峰值: {peak_time} ({peak['count']} 条)")

# 总结
print(f"\n{'=' * 60}")
print("## 📋 总结")
print(f"{'=' * 60}")
print(f"\n  飞廉 24h 日志量: {total}")
if raw_ips_src:
    print(f"  活跃源IP数: {len(raw_ips_src)}")
    print(f"  最活跃源: {raw_ips_src.most_common(1)[0]}")
if raw_ips_dst:
    print(f"  活跃目标IP数: {len(raw_ips_dst)}")
    print(f"  最活跃目标: {raw_ips_dst.most_common(1)[0]}")
if raw_ports_dst:
    print(f"  热门端口: {raw_ports_dst.most_common(3)}")
