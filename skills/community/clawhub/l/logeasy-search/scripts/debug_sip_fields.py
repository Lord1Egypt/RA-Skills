#!/usr/bin/env python3
import sys, io, json, urllib.request, urllib.parse, base64
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
AUTH = base64.b64encode(b'admin:MIma@sec2025').decode()
params = {'query': 'appname:sip', 'time_range': 'now-24h,now', 'index_name': 'yotta', 'limit': 100}
url = f'http://10.20.51.16/api/v3/search/sheets/?{urllib.parse.urlencode(params)}'
req = urllib.request.Request(url, headers={'Authorization': f'Basic {AUTH}'})
with urllib.request.urlopen(req, timeout=120) as resp:
    r = json.loads(resp.read().decode('utf-8'))
sheets = r.get('results', {}).get('sheets', {})
rows = sheets.get('rows', [])
total = r['results']['total_hits']
print(f'total_hits: {total}, rows returned: {len(rows)}')

all_keys = set()
for row in rows:
    all_keys.update(row.keys())
sip_keys = sorted(k for k in all_keys if k.startswith('sip.'))
print(f'\nsip.* fields ({len(sip_keys)}):')
for k in sip_keys:
    print(f'  {k}')

# show sip.ip, sip.hostRisk, sip.suffer_ip for first 5 rows
print('\n--- Key fields in first 5 rows ---')
key_fields = ['sip.ip', 'sip.hostRisk', 'sip.suffer_ip', 'sip.sub_attack_type_name',
              'sip.sub_attack_name', 'sip.threat_level', 'sip.module_type_name',
              'sip.reliability', 'sip.attack_state', 'sip.status_code', 'sip.suggest']
for i, row in enumerate(rows[:5]):
    print(f'\nRow {i}:')
    for k in key_fields:
        v = row.get(k, '')
        if v is not None and str(v) not in ('', '0', 'None'):
            sv = str(v)[:150]
            print(f'  {k}: {sv}')

# collect unique sip.ip values
ip_vals = {}
risk_vals = {}
internal_prefixes = ('10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.', '172.21.',
                     '172.22.', '172.23.', '172.24.', '172.25.', '172.26.', '172.27.',
                     '172.28.', '172.29.', '172.30.', '172.31.', '192.168.', '127.', '0.')
def is_internal(ip):
    if not ip or ip in ('-', '未知', ''): return True
    return any(ip.startswith(p) for p in internal_prefixes)

for row in rows:
    ip = row.get('sip.ip', '')
    risk = row.get('sip.hostRisk', '')
    if ip and ip not in ('-', '', '未知', '0'):
        ip_vals[ip] = ip_vals.get(ip, 0) + 1
    if risk and risk not in ('', '未知'):
        risk_vals[risk] = risk_vals.get(risk, 0) + 1

print(f'\n--- sip.ip distribution ({len(ip_vals)} unique) ---')
internet = {ip: cnt for ip, cnt in ip_vals.items() if not is_internal(ip)}
internal = {ip: cnt for ip, cnt in ip_vals.items() if is_internal(ip)}
print(f'Internet IPs: {len(internet)} types, {sum(internet.values())} total')
print(f'Internal IPs: {len(internal)} types, {sum(internal.values())} total')
if internet:
    print('\nInternet TOP 10:')
    for ip, cnt in sorted(internet.items(), key=lambda x: -x[1])[:10]:
        print(f'  {cnt:3d} {ip}')
