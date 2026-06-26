#!/usr/bin/env python3
"""态势感知互联网攻击 - 通过排除法和多条件搜索"""
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

def extract_json(raw):
    """从 raw_message 提取 JSON"""
    try:
        idx = raw.find('{')
        if idx >= 0:
            return json.loads(raw[idx:])
    except:
        pass
    try:
        for part in raw.split('|'):
            part = part.strip()
            if part.startswith('{'):
                return json.loads(part)
    except:
        pass
    return {}

INTERNAL_PREFIXES = ('10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.',
    '172.21.', '172.22.', '172.23.', '172.24.', '172.25.', '172.26.', '172.27.',
    '172.28.', '172.29.', '172.30.', '172.31.', '192.168.', '127.')

def is_internal(ip):
    if not ip or ip in ('-', '', '未知'): return 'unknown'
    return any(ip.startswith(p) for p in INTERNAL_PREFIXES)

print("=" * 60)
print("🔍 态势感知 — 互联网攻击全面分析")
print(f"  统计周期: 最近24小时")
print("=" * 60)

# 策略：分多次搜索不同维度的互联网攻击
all_internet = []
all_stats = {
    'attack_types': collections.Counter(),
    'suffer_ips': collections.Counter(),
    'countries': collections.Counter(),
    'reliability': collections.Counter(),
    'threat': collections.Counter(),
    'modules': collections.Counter(),
    'http_codes': collections.Counter(),
    'source_ips': collections.Counter(),
    'total_hits': 0,
}

queries = [
    ('SIP非内网攻击(排除10.x/172.x/192.168)', 'appname:sip NOT sip.ip:"10." NOT sip.ip:"172." NOT sip.ip:"192.168"'),
    ('SIP有国家标注的攻击', 'appname:sip sip.attack_country:"中国" NOT sip.attack_province:"未知"'),
    ('SIP外部攻击-攻击资产ID非内网', 'appname:sip sip.attack_asset_id:"*"'),
]

for desc, query in queries:
    print(f"\n[搜索] {desc}...")
    r = search(query, limit=100)
    total = r.get('results', {}).get('total_hits', 0)
    rows = r.get('results', {}).get('sheets', {}).get('rows', [])
    print(f"  命中: {total} | 返回: {len(rows)} 条")
    all_stats['total_hits'] = max(all_stats['total_hits'], total)
    
    for row in rows:
        raw = row.get('raw_message', '')
        detail = extract_json(raw)
        
        ip = detail.get('ip', '') or ''
        if not ip:
            # 尝试其他字段
            ip = row.get('sip.attack_ip', '') or row.get('sip.ip', '')
        
        # 也从 raw_message 正则提取IP
        if not ip or is_internal(ip) == 'internal':
            # 查找 raw 中的外网IP
            ips_found = re.findall(r'"ip"\s*:\s*"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"', raw)
            for found_ip in ips_found:
                if is_internal(found_ip) == 'internet':
                    ip = found_ip
                    break
        
        classify = is_internal(ip)
        if classify == 'internet':
            suffer = row.get('sip.suffer_ip', '')
            atk_type = row.get('sip.sub_attack_type_name', '')
            module = row.get('sip.module_type_name', '')
            rel = str(row.get('sip.reliability', ''))
            threat = str(row.get('sip.threat_level', ''))
            status = row.get('sip.status_code', '')
            country = detail.get('attack_country', '') or row.get('sip.attack_country', '')
            risk = row.get('sip.hostRisk', '')
            
            entry = {'ip': ip, 'suffer': suffer, 'type': atk_type, 'module': module,
                     'reliability': rel, 'threat': threat, 'status': status,
                     'country': country, 'risk': risk, 'raw': raw[:200]}
            
            # 去重
            if not any(e['ip'] == ip and e['suffer'] == suffer and e['type'] == atk_type 
                       for e in all_internet):
                all_internet.append(entry)
            
            all_stats['source_ips'][ip] += 1
            all_stats['attack_types'][atk_type] += 1
            all_stats['suffer_ips'][suffer] += 1
            if country and country not in ('未知', '', '-', '0'):
                all_stats['countries'][country] += 1
            all_stats['reliability'][rel] += 1
            all_stats['threat'][threat] += 1
            all_stats['modules'][module] += 1
            code_str = str(status) if not isinstance(status, list) else '+'.join(str(c) for c in status)
            all_stats['http_codes'][code_str] += 1

# 如果上面方法都没找到，用更宽泛的搜索：直接搜 raw_message 含外网IP特征
if not all_internet:
    print("\n[搜索] 尝试更宽泛搜索 - 从 raw_message 提取外网IP...")
    r = search('appname:sip', limit=100)
    rows = r.get('results', {}).get('sheets', {}).get('rows', [])
    
    for row in rows:
        raw = row.get('raw_message', '')
        detail = extract_json(raw)
        
        # 检查所有可能的IP字段
        possible_ips = []
        for key in ['ip', 'src_ip', 'source_ip', 'client_ip', 'remote_addr']:
            v = detail.get(key, '')
            if v and isinstance(v, str) and re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', v):
                possible_ips.append(v)
        
        # 也检查 row 级别的字段
        for key in ['sip.attack_ip', 'sip.ip']:
            v = row.get(key, '')
            if v and isinstance(v, str) and re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', v):
                possible_ips.append(v)
        
        for ip in possible_ips:
            if is_internal(ip) == 'internet':
                suffer = row.get('sip.suffer_ip', '')
                atk_type = row.get('sip.sub_attack_type_name', '')
                module = row.get('sip.module_type_name', '')
                rel = str(row.get('sip.reliability', ''))
                threat = str(row.get('sip.threat_level', ''))
                status = row.get('sip.status_code', '')
                country = detail.get('attack_country', '') or row.get('sip.attack_country', '')
                
                if not any(e['ip'] == ip and e['suffer'] == suffer for e in all_internet):
                    all_internet.append({
                        'ip': ip, 'suffer': suffer, 'type': atk_type, 'module': module,
                        'reliability': rel, 'threat': threat, 'status': status,
                        'country': country
                    })
                all_stats['source_ips'][ip] += 1
                all_stats['attack_types'][atk_type] += 1
                all_stats['suffer_ips'][suffer] += 1
                if country and country not in ('未知', '', '-', '0'):
                    all_stats['countries'][country] += 1

# 输出报告
print(f"\n{'=' * 60}")
print(f"## 📊 分析结果")
print(f"{'=' * 60}")
print(f"  SIP 24h 总告警: {all_stats['total_hits']}")
print(f"  发现互联网攻击记录: {len(all_internet)} 条（采样）")

if all_internet:
    print(f"\n## 🌐 互联网攻击源 IP")
    for ip, cnt in all_stats['source_ips'].most_common(20):
        bar = '█' * min(cnt * 3, 40)
        # 尝试标记IP归属
        print(f"  {cnt:4d} {bar} {ip}")
    
    if all_stats['countries']:
        print(f"\n## 🗺️ 攻击来源国家/地区")
        for c, cnt in all_stats['countries'].most_common(10):
            print(f"  {cnt:4d} — {c}")
    
    if all_stats['attack_types']:
        print(f"\n## ⚔️ 互联网攻击类型")
        for t, cnt in all_stats['attack_types'].most_common(10):
            if t:
                print(f"  {cnt:4d} — {t}")
    
    if all_stats['suffer_ips']:
        print(f"\n## 🎯 被攻击的内网目标")
        for ip, cnt in all_stats['suffer_ips'].most_common(10):
            bar = '█' * min(cnt * 2, 30)
            print(f"  {cnt:4d} {bar} {ip}")
    
    if all_stats['modules']:
        print(f"\n## 📦 攻击模块")
        for m, cnt in all_stats['modules'].most_common():
            if m:
                print(f"  {cnt:4d} — {m}")
    
    if all_stats['http_codes']:
        print(f"\n## 📡 HTTP 响应状态码")
        for code, cnt in all_stats['http_codes'].most_common(5):
            print(f"  {cnt:4d} — {code}")
    
    # 详细记录
    print(f"\n## 📋 互联网攻击详细记录")
    for i, a in enumerate(all_internet[:20], 1):
        rel_label = {'3': '高', '2': '中', '1': '低'}.get(a['reliability'], '?')
        print(f"  [{i:2d}] {a['ip']} → {a['suffer']} | {a['type'] or '?'} | 可信度:{rel_label} | {a['module']}")
    
    print(f"\n{'=' * 60}")
    print("## 💡 总结")
    print(f"{'=' * 60}")
    print(f"\n  24h SIP 态势感知共 {all_stats['total_hits']} 条告警")
    print(f"  采样中发现 {len(all_internet)} 条来自互联网的攻击")
    if all_stats['source_ips']:
        top = all_stats['source_ips'].most_common(1)[0]
        print(f"  主要攻击源: {top[0]} ({top[1]}次)")
    print(f"  主要被攻击目标: {all_stats['suffer_ips'].most_common(3)}")
else:
    print(f"\n  ⚠️ 在 24h 的 {all_stats['total_hits']} 条 SIP 告警中，")
    print(f"     采样未发现明确的互联网攻击源 IP。")
    print(f"     这可能意味着:")
    print(f"     1. 大部分攻击确实来自内网（安全测试/扫描/蜜罐）")
    print(f"     2. 互联网攻击的 sip.ip 字段未正确记录")
    print(f"     3. 20条采样量不足以覆盖互联网攻击")
    print(f"\n  💡 建议：在日志易 Web 界面手动筛选 'attack_country 不为未知' 查看互联网攻击")
