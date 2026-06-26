#!/usr/bin/env python3
# Author: geji (built from daily PingCode usage)
# Repo: personal skill workspace

"""
PingCode 测试执行情况查询工具
用法：
  python3 scripts/query_test_runs.py                           # 列出最近的执行用例
  python3 scripts/query_test_runs.py --library_name "项目名称"  # 按测试库筛选
  python3 scripts/query_test_runs.py --days 7                  # 最近7天
  python3 scripts/query_test_runs.py --detail                  # 显示详细结果
"""

import requests, json, os, sys, argparse
from collections import Counter
from datetime import datetime, timedelta

BASE = 'https://open.pingcode.com'

def get_token():
    cid = os.environ.get('PINGCODE_CLIENT_ID')
    secret = os.environ.get('PINGCODE_CLIENT_SECRET')
    if not cid or not secret:
        print("❌ 请设置环境变量 PINGCODE_CLIENT_ID 和 PINGCODE_CLIENT_SECRET")
        sys.exit(1)
    r = requests.get(f'{BASE}/v1/auth/token', params={
        'grant_type': 'client_credentials', 'client_id': cid, 'client_secret': secret
    })
    return r.json().get('access_token')

def get_libraries(token):
    headers = {'Authorization': f'Bearer {token}'}
    page = 0
    all_libs = []
    while True:
        r = requests.get(f'{BASE}/v1/testhub/libraries', params={'page_size': 100, 'page_index': page}, headers=headers)
        vals = r.json().get('values', [])
        if not vals:
            break
        all_libs.extend(vals)
        page += 1
    return all_libs

def get_test_runs(token, library_id=None, days=30):
    headers = {'Authorization': f'Bearer {token}'}
    page = 0
    all_runs = []
    since = (datetime.now() - timedelta(days=days)).isoformat()
    
    params = {'page_size': 100, 'page_index': page}
    if library_id:
        params['library_id'] = library_id
    
    while True:
        r = requests.get(f'{BASE}/v1/testhub/test_runs', params=params, headers=headers)
        if r.status_code != 200:
            print(f'⚠️ 查询测试运行失败: {r.status_code} {r.text[:200]}')
            break
        vals = r.json().get('values', [])
        if not vals:
            break
        all_runs.extend(vals)
        page += 1
        params['page_index'] = page
    return all_runs

def main():
    parser = argparse.ArgumentParser(description='PingCode 测试执行查询')
    parser.add_argument('--library_name', help='测试库名称筛选')
    parser.add_argument('--days', type=int, default=30, help='查询最近N天')
    parser.add_argument('--detail', action='store_true', help='显示详细执行结果')
    args = parser.parse_args()
    
    token = get_token()
    headers = {'Authorization': f'Bearer {token}'}
    
    # Find library
    library_id = None
    if args.library_name:
        libs = get_libraries(token)
        matched = [l for l in libs if args.library_name.lower() in l.get('name','').lower()]
        if matched:
            library_id = matched[0]['id']
            print(f'📦 测试库: {matched[0]["name"]} ({library_id})')
        else:
            print(f'❌ 未找到包含 "{args.library_name}" 的测试库')
            return
    
    # Get test runs
    runs = get_test_runs(token, library_id, args.days)
    print(f'📊 共查询到 {len(runs)} 条执行用例（最近 {args.days} 天）
')
    
    if not runs:
        return
    
    # Stats
    result_counts = Counter()
    status_counts = Counter()
    assignee_counts = Counter()
    plan_counts = Counter()
    
    for run in runs:
        result = run.get('result',{})
        result_counts[result.get('name','?') if isinstance(result, dict) else '?'] += 1
        status_counts[run.get('status',{}).get('name','?')] += 1
        assignee = run.get('assignee',{})
        assignee_counts[assignee.get('display_name','未指派') if assignee else '未指派'] += 1
        plan = run.get('plan',{})
        plan_counts[plan.get('name','?') if plan else '?'] += 1
    
    print('📋 执行结果分布:')
    for k, v in result_counts.most_common():
        print(f'   {k}: {v}')
    print()
    
    print('👤 执行人分布:')
    for k, v in assignee_counts.most_common(10):
        print(f'   {k}: {v}')
    print()
    
    if args.detail and runs:
        print('📝 最近执行:')
        for run in runs[:20]:
            case = run.get('case',{})
            plan = run.get('plan',{})
            result = run.get('result',{})
            assignee = run.get('assignee',{})
            a_name = assignee.get('display_name','?') if assignee else '?'
            r_name = result.get('name','?') if isinstance(result, dict) else '?'
            p_name = plan.get('name','?') if plan else '?'
            title = case.get('title','?') if case else '?'
            print(f'   [{r_name}] {title}')
            print(f'     计划: {p_name} | 执行人: {a_name}')

if __name__ == '__main__':
    main()
