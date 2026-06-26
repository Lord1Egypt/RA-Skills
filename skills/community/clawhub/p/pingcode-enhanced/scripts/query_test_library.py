#!/usr/bin/env python3
# Author: geji (built from daily PingCode usage)
# Repo: personal skill workspace

"""
PingCode 测试库查询工具
用法：
  python3 scripts/query_test_library.py                       # 列出所有测试库
  python3 scripts/query_test_library.py --library_name "合规"  # 按名称查找测试库
  python3 scripts/query_test_library.py --library_id xxx      # 按ID查询
  python3 scripts/query_test_library.py --library_name "合规" --detail  # 查看用例详情
"""

import requests, json, os, sys, argparse
from collections import Counter

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
    data = r.json()
    return data.get('access_token')

def get_libraries(token, name_filter=None):
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
    if name_filter:
        return [lib for lib in all_libs if name_filter.lower() in lib.get('name','').lower()]
    return all_libs

def get_cases(token, library_id):
    headers = {'Authorization': f'Bearer {token}'}
    page = 0
    all_cases = []
    while True:
        r = requests.get(f'{BASE}/v1/testhub/cases', params={
            'library_id': library_id, 'page_size': 100, 'page_index': page
        }, headers=headers)
        vals = r.json().get('values', [])
        if not vals:
            break
        all_cases.extend(vals)
        page += 1
    return all_cases

def get_suites(token, library_id):
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get(f'{BASE}/v1/testhub/libraries/{library_id}/suites', params={'page_size': 50}, headers=headers)
    return r.json().get('values', [])

def main():
    parser = argparse.ArgumentParser(description='PingCode 测试库查询工具')
    parser.add_argument('--library_name', help='测试库名称（模糊匹配）')
    parser.add_argument('--library_id', help='测试库 ID')
    parser.add_argument('--detail', action='store_true', help='显示用例详情')
    args = parser.parse_args()

    token = get_token()
    headers = {'Authorization': f'Bearer {token}'}

    if args.library_id:
        # 直接按ID查询
        r = requests.get(f'{BASE}/v1/testhub/libraries/{args.library_id}', headers=headers)
        if r.status_code == 200:
            lib = r.json()
            print(f'📦 {lib["id"]}  {lib.get("name","?")}')
            if args.detail:
                cases = get_cases(token, args.library_id)
                suites = get_suites(token, args.library_id)
                print_suite_stats(cases, suites)
        else:
            print(f'❌ 查询失败: {r.text[:200]}')
    elif args.library_name:
        libs = get_libraries(token, args.library_name)
        if not libs:
            print(f'❌ 未找到包含 "{args.library_name}" 的测试库')
            return
        for lib in libs:
            print(f'📦 {lib["id"]}  {lib.get("name","?")}')
            if args.detail:
                cases = get_cases(token, lib['id'])
                suites = get_suites(token, lib['id'])
                print_suite_stats(cases, suites)
            print()
    else:
        # 列出全部
        libs = get_libraries(token)
        print(f'📊 共 {len(libs)} 个测试库
')
        for lib in libs:
            print(f'📦 {lib["id"]}  {lib.get("name","?")}')
        print()

def print_suite_stats(cases, suites):
    if not cases:
        print(f'   用例总数: 0')
        return
    
    # Build suite name map
    suite_map = {s['id']: s['name'] for s in suites}
    
    suite_counts = Counter()
    state_counts = Counter()
    
    for c in cases:
        suite = c.get('suite',{})
        sname = suite_map.get(suite.get('id',''), suite.get('name','未分类')) if suite else '未分类'
        suite_counts[sname] += 1
        state = c.get('state',{})
        state_counts[state.get('name','?') if isinstance(state, dict) else '?'] += 1
    
    print(f'   用例总数: {len(cases)}')
    print(f'   状态分布: {dict(state_counts.most_common())}')
    print(f'   模块分布:')
    for name, count in suite_counts.most_common(10):
        print(f'     {name}: {count}')
    if len(suite_counts) > 10:
        print(f'     ... 还有 {len(suite_counts)-10} 个模块')

if __name__ == '__main__':
    main()
