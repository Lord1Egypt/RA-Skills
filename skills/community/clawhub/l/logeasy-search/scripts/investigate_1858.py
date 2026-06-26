#!/usr/bin/env python3
"""排查 10.10.185.8 安全事件"""
import sys, io, json, urllib.request, urllib.parse, base64, collections
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

RIZHIYI = 'http://10.20.51.16'
AUTH = base64.b64encode(b'admin:MIma@sec2025').decode()
headers = {'Authorization': f'Basic {AUTH}', 'Content-Type': 'application/json'}

def search(query, time_range='now-24h,now', index_name='yotta', limit=100):
    params = {'query': query, 'time_range': time_range, 'index_name': index_name, 'limit': limit}
    url = f"{RIZHIYI}/api/v3/search/sheets/?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return {'error': str(e), 'rc': -1}

# 1. 被攻击总览 - 受害者视角
print("=" * 60)
print("🔍 10.10.185.8 安全事件排查报告")
print("=" * 60)
print()

# 搜受害者IP
r = search('sip.suffer_ip:"10.10.185.8"', time_range='now-24h,now', limit=100)
if r.get('rc') != 0:
    print(f"❌ 搜索失败: {json.dumps(r.get('error', {}), ensure_ascii=False)}")
    sys.exit(1)

results = r.get('results', {})
total = results.get('total_hits', 0)
rows = results.get('sheets', {}).get('rows', [])

print(f"## 📊 概览")
print(f"  统计周期: 最近24小时")
print(f"  攻击总数: {total} 条")
print(f"  返回条数: {len(rows)} 条")
print()

# 统计攻击类型
attack_types = collections.Counter()
attackers = collections.Counter()
threat_levels = collections.Counter()
attack_states = collections.Counter()
protocols = collections.Counter()
briefs = collections.Counter()
timeline = collections.Counter()

for row in rows:
    atk_type = row.get('sip.sub_attack_type_name', '未知')
    atk_name = row.get('sip.sub_attack_name', '未知')
    attacker_ip = row.get('sip.ip', row.get('src_ip', '未知'))
    threat = row.get('sip.threat_level', '未知')
    state = row.get('sip.attack_state', '未知')
    brief = row.get('sip.brief', '未知')
    raw = row.get('raw_message', '')
    
    # 组合攻击类型
    full_type = f"{atk_type} - {atk_name}" if atk_type != '未知' else atk_name
    attack_types[full_type] += 1
    attackers[attacker_ip] += 1
    threat_levels[str(threat)] += 1
    attack_states[str(state)] += 1
    briefs[brief] += 1
    
    # 时间线（按小时）
    try:
        # 从 raw_message 提取时间
        time_str = raw.split('|')[0] if '|' in raw else ''
        if time_str:
            hour = time_str.strip()[-8:-6] if len(time_str) >= 8 else '??'
            timeline[hour] += 1
    except:
        pass

# 威胁等级映射
threat_map = {'1': '🔴 高危', '2': '🟠 中危', '3': '🟡 低危', '4': '🔵 信息', '未知': '⚪ 未知'}
state_map = {'1': '已处理', '2': '未处理', '3': '忽略', '未知': '未知'}

print("## 🎯 攻击类型分布 TOP 15")
for atype, cnt in attack_types.most_common(15):
    bar = '█' * min(cnt, 40)
    print(f"  {cnt:4d} {bar} {atype}")
print()

print("## 🌐 攻击源 IP TOP 10")
for ip, cnt in attackers.most_common(10):
    bar = '█' * min(cnt, 30)
    print(f"  {cnt:4d} {bar} {ip}")
print()

print("## ⚠️ 威胁等级分布")
for level, cnt in threat_levels.most_common():
    label = threat_map.get(level, f'等级{level}')
    print(f"  {label}: {cnt} 条")
print()

print("## 📋 处理状态")
for state, cnt in attack_states.most_common():
    label = state_map.get(state, f'状态{state}')
    print(f"  {label}: {cnt} 条")
print()

print("## 📈 时间线（按小时）")
for hour in sorted(timeline.keys()):
    cnt = timeline[hour]
    bar = '█' * min(cnt, 50)
    print(f"  {hour}:00  {cnt:4d} {bar}")
print()

print("## 📝 攻击分类概览")
for brief, cnt in briefs.most_common():
    print(f"  {cnt:4d} - {brief}")
print()

# 3. 高危攻击详情
print("=" * 60)
print("## 🔴 高危攻击详情（threat_level=1）")
print("=" * 60)
high_risk = [r for r in rows if r.get('sip.threat_level') == '1']
print(f"共 {len(high_risk)} 条高危攻击\n")

for i, row in enumerate(high_risk[:10], 1):
    print(f"### [{i}]")
    print(f"  攻击类型: {row.get('sip.sub_attack_type_name', '?')} - {row.get('sip.sub_attack_name', '?')}")
    print(f"  攻击源: {row.get('sip.ip', '?')}")
    print(f"  攻击源风险: {row.get('sip.hostRisk', '?')}")
    print(f"  描述: {row.get('sip.brief', '?')}")
    print(f"  处理状态: {state_map.get(row.get('sip.attack_state', '?'), '?')}")
    # 提取更多详情
    raw = row.get('raw_message', '')
    if raw:
        try:
            # 尝试从 syslog 格式后的 JSON 提取
            json_start = raw.find('{')
            if json_start > 0:
                detail = json.loads(raw[json_start:])
                if 'attack_detail' in detail:
                    print(f"  攻击详情: {str(detail['attack_detail'])[:200]}")
                if 'rule_name' in detail:
                    print(f"  规则名称: {detail['rule_name']}")
                if 'url' in detail and detail['url']:
                    print(f"  请求URL: {detail['url']}")
                if 'request_method' in detail:
                    print(f"  请求方法: {detail['request_method']}")
        except:
            pass
    print()

# 4. 未处理的高危事件
print("=" * 60)
print("## ⚡ 未处理事件（attack_state=2）")
print("=" * 60)
unhandled = [r for r in rows if r.get('sip.attack_state') == '2']
print(f"共 {len(unhandled)} 条未处理事件\n")
# 按威胁等级统计
unhandled_threat = collections.Counter()
for r in unhandled:
    t = r.get('sip.threat_level', '?')
    label = threat_map.get(t, f'等级{t}')
    unhandled_threat[label] += 1
for t, cnt in unhandled_threat.most_common():
    print(f"  {t}: {cnt} 条")
print()

# 5. 结论
print("=" * 60)
print("## 📋 排查结论")
print("=" * 60)
print()
print(f"1. 10.10.185.8 在过去24小时共遭受 {total} 次攻击")
print(f"2. 主要攻击类型: {', '.join([t for t, _ in attack_types.most_common(5)])}")
print(f"3. 主要攻击源: {', '.join([ip for ip, _ in attackers.most_common(5)])}")
print(f"4. 高危攻击: {len(high_risk)} 条，未处理: {len(unhandled)} 条")
print()

# 风险评估
if len(high_risk) > 0:
    print("⚠️ 风险等级: 高")
    print("  建议:")
    print("  - 立即检查 10.10.185.8 上的应用和服务状态")
    print("  - 确认是否存在已知的未修复漏洞")
    print("  - 检查攻击是否成功（查看WAF/IDS日志、应用日志）")
    print("  - 对高频攻击源IP进行封禁（需确认是否为业务IP）")
elif len(unhandled) > 10:
    print("⚠️ 风险等级: 中")
    print("  建议: 尽快处理未处理的安全事件")
else:
    print("✅ 风险等级: 低")
    print("  日常监控即可")
