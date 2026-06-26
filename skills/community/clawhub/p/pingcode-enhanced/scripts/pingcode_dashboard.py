#!/usr/bin/env python3
# Author: geji (built from daily PingCode usage)
# Repo: personal skill workspace

"""
PingCode 全局看板 — 一条命令看全貌
用法:
  python3 scripts/pingcode_dashboard.py               # 所有项目概览
  python3 scripts/pingcode_dashboard.py --project "合规"  # 指定项目
  python3 scripts/pingcode_dashboard.py --name "项目名称"
  python3 scripts/pingcode_dashboard.py --test        # 含测试库统计
"""

import requests, json, os, sys, argparse
from collections import Counter
from datetime import datetime

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

def fetch_all(url, params, headers):
    page = 0
    all_items = []
    while True:
        p = {**params, 'page_size': 100, 'page_index': page}
        r = requests.get(url, params=p, headers=headers)
        if r.status_code != 200:
            break
        vals = r.json().get('values', [])
        if not vals:
            break
        all_items.extend(vals)
        page += 1
    return all_items

def main():
    parser = argparse.ArgumentParser(description='PingCode 全局看板')
    parser.add_argument('--project', help='项目名称筛选')
    parser.add_argument('--name', help='按项目名搜索')
    parser.add_argument('--test', action='store_true', help='含测试库统计')
    args = parser.parse_args()

    token = get_token()
    headers = {'Authorization': f'Bearer {token}'}
    
    name_filter = args.project or args.name
    
    # 1. 项目
    projects = fetch_all(f'{BASE}/v1/agile/projects', {}, headers)
    if name_filter:
        projects = [p for p in projects if name_filter.lower() in p.get('name','').lower()]
    
    print('=' * 50)
    print('  PingCode 概览看板')
    print(f'  {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    print('=' * 50)
    print(f'
📦 项目 ({len(projects)}):
')
    
    for p in projects:
        pid = p['id']
        pname = p.get('name','?')
        
        # 工作项统计 (使用 /v1/project/work_items?project_id=xx)
        items = fetch_all(f'{BASE}/v1/project/work_items', {'project_id': pid}, headers)
        total = len(items)
        open_items = [i for i in items if i.get('state',{}).get('type') not in ('completed','cancelled')]
        bugs = [i for i in items if i.get('type') == 'bug']
        
        print(f'📦 {pname}')
        print(f'   总工作项: {total} | 未完成: {len(open_items)} | Bug: {len(bugs)}')
        
        # 迭代
        sprints = fetch_all(f'{BASE}/v1/agile/projects/{pid}/sprints', {}, headers)
        active = [s for s in sprints if s.get('status') in ('active', 'in_progress')]
        if active:
            for s in active:
                print(f'   🔄 迭代: {s.get("name","?")} ({s.get("start_date","?")[:10]} ~ {s.get("end_date","?")[:10]})')
        
        # 测试库
        if args.test:
            libs = fetch_all(f'{BASE}/v1/testhub/libraries', {}, headers)
            matched_libs = [l for l in libs if pname in l.get('name','')]
            for lib in matched_libs:
                r = requests.get(f'{BASE}/v1/testhub/cases', params={
                    'library_id': lib['id'], 'page_size': 1
                }, headers=headers)
                case_count = r.json().get('total', 0) if r.status_code == 200 else 0
                print(f'   🧪 测试库: {lib.get("name","?")} ({case_count} 用例)')
        
        # 负责人分布
        assignees = Counter()
        for item in open_items:
            a = item.get('assignee',{})
            assignees[a.get('display_name','未指派') if a else '未指派'] += 1
        top = assignees.most_common(3)
        if top:
            print(f'   负责人(Top3): {", ".join(f"{k}({v})" for k,v in top)}')
        print()

if __name__ == '__main__':
    main()
