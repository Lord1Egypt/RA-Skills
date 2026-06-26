#!/usr/bin/env python3
"""分析态势感知(SIP)最近24小时来自互联网的攻击"""
import sys, io, json, urllib.request, urllib.parse, base64
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

RIZHIYI = 'http://10.20.51.16'
AUTH = base64.b64encode(b'admin:MIma@sec2025').decode()
headers = {'Authorization': f'Basic {AUTH}', 'Content-Type': 'application/json'}

def search_raw(query, time_range='now-24h,now', limit=100):
    params = {'query': query, 'time_range': time_range, 'index_name': 'yotta', 'limit': limit}
    url = f"{RIZHIYI}/api/v3/search/sheets/?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode('utf-8'))

# 互联网攻击：非内网IP（排除10.x、172.16-31.x、192.168.x）
# 用 SIP 数据的 hostRisk 字段或 sip.ip 字段，排除内网
# 先搜总量和分布
print("=" * 60)
print("🔍 态势感知(SIP) — 互联网攻击分析")
print("  统计周期: 最近24小时")
print("=" * 60)

# 1. 先查 SIP 总体数据
print("\n## 📊 态势感知日志总量...")
r = search_raw('appname:sip', limit=100)
if r.get('rc') != 0:
    print(f"❌ 搜索失败: {r}")
    sys.exit(1)

total_hits = r.get('results', {}).get('total_hits', 0)
print(f"  SIP 总告警数: {total_hits}")

# 2. 从 topk 字段中找攻击源分布
fields = r.get('results', {}).get('sheets', {}).get('fields', [])
ip_field = None
suffer_field = None
host_risk_field = None
attack_type_field = None
attack_name_field = None
threat_field = None
module_field = None
reliability_field = None
status_code_field = None
attack_state_field = None
url_field = None
suggest_field = None
tags_field = None

for f in fields:
    name = f.get('name', '')
    if name == 'sip.ip': ip_field = f
    elif name == 'sip.suffer_ip': suffer_field = f
    elif name == 'sip.hostRisk': host_risk_field = f
    elif name == 'sip.sub_attack_type_name': attack_type_field = f
    elif name == 'sip.sub_attack_name': attack_name_field = f
    elif name == 'sip.threat_level': threat_field = f
    elif name == 'sip.module_type_name': module_field = f
    elif name == 'sip.reliability': reliability_field = f
    elif name == 'sip.status_code': status_code_field = f
    elif name == 'sip.attack_state': attack_state_field = f
    elif name == 'sip.url': url_field = f
    elif name == 'sip.suggest': suggest_field = f
    elif name == 'sip.tags': tags_field = f

# 分析攻击源IP - 区分内网/互联网
internal_prefixes = ('10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.', '172.21.',
                     '172.22.', '172.23.', '172.24.', '172.25.', '172.26.', '172.27.',
                     '172.28.', '172.29.', '172.30.', '172.31.', '192.168.', '127.', '0.')

def is_internal_ip(ip_str):
    if not ip_str or ip_str == '未知' or ip_str == '-':
        return True  # 未知视为内网
    if isinstance(ip_str, list):
        return all(is_internal_ip(i) for i in ip_str)
    return any(ip_str.startswith(p) for p in internal_prefixes)

internet_ips = {}
internal_ips = {}
all_ips = {}

if ip_field:
    for item in ip_field.get('topk', []):
        ip = item.get('value', '')
        cnt = item.get('count', 0)
        if isinstance(ip, list):
            ip = ip[0] if ip else ''
        if not ip or ip == '-' or ip == '未知':
            continue
        all_ips[ip] = all_ips.get(ip, 0) + cnt
        if is_internal_ip(ip):
            internal_ips[ip] = internal_ips.get(ip, 0) + cnt
        else:
            internet_ips[ip] = internet_ips.get(ip, 0) + cnt

internal_total = sum(internal_ips.values())
internet_total = sum(internet_ips.values())

print(f"\n## 🌍 攻击源区分（基于 sip.ip topk）")
print(f"  内网攻击源: {internal_total} 次")
print(f"  互联网攻击源: {internet_total} 次")
print(f"  其他/未知: {total_hits - internal_total - internet_total} 次")

# 3. 互联网攻击 TOP IP
print(f"\n## 🌐 互联网攻击源 IP TOP 20")
if internet_ips:
    for ip, cnt in sorted(internet_ips.items(), key=lambda x: -x[1])[:20]:
        bar = '█' * min(cnt, 30)
        print(f"  {cnt:5d} {bar} {ip}")
else:
    print("  (无互联网IP在topk中)")

# 4. 互联网攻击的受害者
print(f"\n## 🎯 互联网攻击的受害目标")
if suffer_field:
    all_suffer = {}
    for item in suffer_field.get('topk', []):
        ip = item.get('value', '')
        cnt = item.get('count', 0)
        if isinstance(ip, list):
            ip = ip[0] if ip else ''
        all_suffer[ip] = all_suffer.get(ip, 0) + cnt
    for ip, cnt in sorted(all_suffer.items(), key=lambda x: -x[1])[:15]:
        bar = '█' * min(cnt, 30)
        print(f"  {cnt:5d} {bar} {ip}")

# 5. 攻击类型分布
print(f"\n## ⚔️ 攻击类型分布 TOP 15")
if attack_type_field:
    for item in attack_type_field.get('topk', [])[:15]:
        name = item.get('value', '未知')
        cnt = item.get('count', 0)
        pct = cnt / total_hits * 100 if total_hits > 0 else 0
        bar = '█' * min(int(pct / 2), 40)
        print(f"  {cnt:5d} ({pct:5.1f}%) {bar} {name}")

# 6. 攻击模块
print(f"\n## 📦 攻击模块分布")
if module_field:
    for item in module_field.get('topk', []):
        name = item.get('value', '未知')
        cnt = item.get('count', 0)
        pct = cnt / total_hits * 100 if total_hits > 0 else 0
        print(f"  {cnt:5d} ({pct:5.1f}%) — {name}")

# 7. 威胁等级
print(f"\n## ⚠️ 威胁等级分布")
threat_map = {'1': '🔴 高危', '2': '🟠 中危', '3': '🟡 低危', '4': '🔵 信息'}
if threat_field:
    for item in threat_field.get('topk', []):
        level = str(item.get('value', '?'))
        cnt = item.get('count', 0)
        label = threat_map.get(level, f'等级{level}')
        pct = cnt / total_hits * 100 if total_hits > 0 else 0
        print(f"  {label}: {cnt} ({pct:.1f}%)")

# 8. 可信度
print(f"\n## 🛡️ 可信度分布")
rel_map = {'1': '低', '2': '中', '3': '高'}
if reliability_field:
    for item in reliability_field.get('topk', []):
        rel = str(item.get('value', '?'))
        cnt = item.get('count', 0)
        label = rel_map.get(rel, f'等级{rel}')
        pct = cnt / total_hits * 100 if total_hits > 0 else 0
        print(f"  {label}: {cnt} ({pct:.1f}%)")

# 9. HTTP状态码
print(f"\n## 📡 HTTP响应状态码 TOP 10")
if status_code_field:
    for item in status_code_field.get('topk', [])[:10]:
        code = item.get('value', '?')
        cnt = item.get('count', 0)
        if isinstance(code, list):
            code = '+'.join(str(c) for c in code)
        print(f"  {cnt:5d} — {code}")

# 10. 处置建议汇总
print(f"\n## 💡 系统处置建议分布")
if suggest_field:
    for item in suggest_field.get('topk', [])[:5]:
        text = item.get('value', '').replace('\\n', ' | ')[:100]
        cnt = item.get('count', 0)
        print(f"  [{cnt}] {text}")

# 11. 重点被攻击目标的 hostRisk
print(f"\n## 📍 受害目标风险评估")
if host_risk_field:
    for item in host_risk_field.get('topk', [])[:10]:
        risk = item.get('value', '未知')
        cnt = item.get('count', 0)
        print(f"  {cnt:5d} — {risk}")

# 12. 时间线
timeline = r.get('results', {}).get('sheets', {}).get('timeline', {})
timeline_rows = timeline.get('rows', [])
if timeline_rows:
    print(f"\n## ⏰ 24小时攻击趋势")
    max_count = max(row.get('count', 0) for row in timeline_rows)
    for row in timeline_rows:
        ts = row.get('start_ts', 0)
        cnt = row.get('count', 0)
        hour = datetime.fromtimestamp(ts/1000).strftime('%H:%M')
        bar = '█' * int(cnt / max_count * 40) if max_count > 0 else ''
        level = '🔴' if cnt > max_count * 0.8 else '🟠' if cnt > max_count * 0.5 else '🟡' if cnt > max_count * 0.2 else '🟢'
        print(f"  {level} {hour}  {cnt:5d} {bar}")

# 总结
print(f"\n{'=' * 60}")
print("## 📋 总结")
print("=" * 60)
print(f"\n  SIP 24h 总告警: {total_hits}")
print(f"  内网源: {internal_total} | 互联网源: {internet_total}")
if internet_total > 0:
    top_internet_ip = sorted(internet_ips.items(), key=lambda x: -x[1])[0]
    print(f"  互联网攻击 TOP: {top_internet_ip[0]} ({top_internet_ip[1]}次)")
else:
    print(f"  ⚠️ topk 中未发现互联网 IP，可能互联网攻击占比小或在更深层的数据中")
print()
