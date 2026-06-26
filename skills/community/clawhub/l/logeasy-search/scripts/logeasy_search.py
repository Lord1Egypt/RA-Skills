#!/usr/bin/env python3
"""日志易搜索脚本 - 正确API格式
用法:
  python logeasy_search.py "查询" [--time 1h] [--limit 5] [--index yotta] [--raw]
"""
import sys, os, io, json, urllib.request, urllib.parse, base64

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

RIZHIYI = os.environ.get('LOGEASE_BASE_URL', 'http://10.20.51.16')
AUTH_USER = 'admin'
AUTH_PASS = 'MIma@sec2025'
AUTH = base64.b64encode(f'{AUTH_USER}:{AUTH_PASS}'.encode()).decode()

headers = {
    'Authorization': f'Basic {AUTH}',
    'Content-Type': 'application/json',
}

def search(query, time_range='now-1h,now', index_name='yotta', limit=100, raw=False):
    params = {
        'query': query,
        'time_range': time_range,
        'index_name': index_name,
        'limit': limit,
    }
    url = f"{RIZHIYI}/api/v3/search/sheets/?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if raw:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result

    # 解析结果
    if result.get('rc') != 0:
        err = result.get('error', {})
        print(f"搜索失败: {err.get('message', json.dumps(err, ensure_ascii=False))}", file=sys.stderr)
        return result

    results = result.get('results', {})
    total_hits = results.get('total_hits', 0)
    sheets = results.get('sheets', {})
    rows = sheets.get('rows', [])
    starttime = results.get('starttime', 0)
    endtime = results.get('endtime', 0)

    # 时间戳转可读
    def fmt_ts(ts):
        from datetime import datetime
        if ts > 0:
            return datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M:%S')
        return 'N/A'

    print(f"## 搜索结果: {total_hits} 条 (返回 {len(rows)} 条)")
    print(f"   时间范围: {fmt_ts(starttime)} ~ {fmt_ts(endtime)}")
    print()

    if not rows:
        print("(无匹配日志)")
        return result

    for i, row in enumerate(rows, 1):
        print(f"### [{i}]")
        # 提取关键字段
        important_fields = ['appname', 'logtype', 'level', 'severity', 'client_ip', 'src_ip', 'dst_ip',
                          'hostname', 'host', 'sip.suffer_ip', 'sip.ip',
                          'sip.sub_attack_name', 'sip.sub_attack_type_name',
                          'sip.attack_state', 'sip.threat_level', 'sip.brief',
                          'raw_message']
        for field in important_fields:
            if field in row and row[field]:
                val = str(row[field])
                if len(val) > 300:
                    val = val[:300] + '...'
                # 显示更友好的字段名
                display = field.replace('sip.', 'SIP ')
                print(f"  {display}: {val}")
        # 如果没有匹配到重要字段，显示所有字段
        if not any(row.get(f) for f in important_fields):
            for k, v in row.items():
                val = str(v)
                if len(val) > 200:
                    val = val[:200] + '...'
                print(f"  {k}: {val}")
        print()

    return result

def parse_time(time_str):
    """将 1h/24h/7d/30m 转为 time_range 格式"""
    unit = time_str[-1]
    val = time_str[:-1]
    return f"now-{val}{unit},now"

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='日志易搜索')
    parser.add_argument('query', help='搜索查询')
    parser.add_argument('--time', '-t', default='1h', help='时间范围 (如 1h/24h/7d/30m)')
    parser.add_argument('--limit', '-l', type=int, default=100, help='返回条数 (API最大100)')
    parser.add_argument('--index', '-i', default='yotta', help='索引名称')
    parser.add_argument('--raw', action='store_true', help='输出原始JSON')
    args = parser.parse_args()

    time_range = parse_time(args.time)
    search(args.query, time_range=time_range, index_name=args.index, limit=args.limit, raw=args.raw)
