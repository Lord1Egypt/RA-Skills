#!/usr/bin/env python3
# Author: geji (built from daily PingCode usage)
# Repo: personal skill workspace

"""
工作项高级查询 (替代 get_project_workitems.py)
用法:
  python3 scripts/query_workitems.py --project_name "项目名称"                    # 统计
  python3 scripts/query_workitems.py --project_name "项目名称" --status "doing"   # 进行中
  python3 scripts/query_workitems.py --project_name "项目名称" --assignee "张三" # 按负责人
  python3 scripts/query_workitems.py --project_name "项目名称" --type bug          # 仅查看 bug
  python3 scripts/query_workitems.py --project_name "项目名称" --recent 7          # 最近7天变更
  python3 scripts/query_workitems.py --all_projects                                 # 全部项目汇总
  python3 scripts/query_workitems.py --all_projects --unfinished                    # 全部未完成
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

def get_projects(headers, name_filter=None):
    projects = fetch_all(f'{BASE}/v1/agile/projects', {}, headers)
    if name_filter:
        return [p for p in projects if name_filter.lower() in p.get('name','').lower()]
    return projects

def main():
    parser = argparse.ArgumentParser(description='PingCode 工作项高级查询')
    parser.add_argument('--project_name', help='项目名称')
    parser.add_argument('--project_id', help='项目 ID')
    parser.add_argument('--all_projects', action='store_true', help='所有项目')
    parser.add_argument('--status', choices=['doing','done','all'], default='all', help='状态筛选')
    parser.add_argument('--type', help='类型筛选 (bug/story/task)')
    parser.add_argument('--unfinished', action='store_true', help='仅未完成')
    parser.add_argument('--assignee', help='负责人筛选')
    parser.add_argument('--recent', type=int, help='最近N天变更')
    parser.add_argument('--limit', type=int, default=10, help='显示条数')
    args = parser.parse_args()

    token = get_token()
    headers = {'Authorization': f'Bearer {token}'}

    if args.project_name or args.project_id:
        pid = args.project_id
        pname = args.project_name or '?'
        if not pid:
            projects = get_projects(headers, args.project_name)
            if not projects:
                print(f'❌ 未找到项目: {args.project_name}')
                return
            pid = projects[0]['id']
            pname = projects[0].get('name','?')
        
        items = fetch_all(f'{BASE}/v1/agile/projects/{pid}/work_items', {}, headers)
        print(f'📊 {pname} — 共 {len(items)} 项
')
        
    elif args.all_projects:
        projects = get_projects(headers)
        all_items = []
        for p in projects:
            items = fetch_all(f'{BASE}/v1/agile/projects/{p["id"]}/work_items', {}, headers)
            for item in items:
                item['_project_name'] = p.get('name','?')
            all_items.extend(items)
        items = all_items
        print(f'📊 全部项目 — 共 {len(items)} 项
')
    else:
        print('❌ 请指定 --project_name 或 --all_projects')
        return

    # 筛选
    if args.unfinished:
        items = [i for i in items if i.get('state',{}).get('type') not in ('completed','cancelled')]
        print(f'🔍 未完成项: {len(items)}
')
    
    if args.type:
        items = [i for i in items if i.get('type','').lower() == args.type.lower()]
        print(f'🔍 类型={args.type}: {len(items)}
')
    
    if args.assignee:
        items = [i for i in items if args.assignee.lower() in 
                 (i.get('assignee',{}) or {}).get('display_name','').lower()]
        print(f'🔍 负责人={args.assignee}: {len(items)}
')
    
    if args.recent:
        cutoff = datetime.now() - timedelta(days=args.recent)
        items = [i for i in items if i.get('updated_at','')[:10] >= cutoff.strftime('%Y-%m-%d')]
        print(f'🔍 最近{args.recent}天变更: {len(items)}
')

    # 统计
    status_count = Counter()
    type_count = Counter()
    assignee_count = Counter()
    
    for item in items:
        status_count[item.get('state',{}).get('name','?')] += 1
        type_count[item.get('type','?')] += 1
        a = item.get('assignee',{})
        assignee_count[a.get('display_name','未指派') if a else '未指派'] += 1
    
    print('📋 按状态:')
    for k, v in status_count.most_common():
        print(f'   {k}: {v}')
    print()
    
    print('📋 按类型:')
    for k, v in type_count.most_common():
        print(f'   {k}: {v}')
    print()
    
    print('👤 按负责人:')
    for k, v in assignee_count.most_common(10):
        print(f'   {k}: {v}')
    print()
    
    # 列表
    if args.limit and items and args.type or args.assignee or args.unfinished or args.recent:
        print(f'📝 项目列表 (前{args.limit}项):')
        for item in items[:args.limit]:
            title = item.get('title','?')
            state = item.get('state',{}).get('name','?')
            itype = item.get('type','?')
            a = item.get('assignee',{})
            aname = a.get('display_name','?') if a else '?'
            pname = item.get('_project_name','')
            prefix = f'[{pname}] ' if pname else ''
            print(f'   [{itype}] [{state}] {prefix}{title} → {aname}')

if __name__ == '__main__':
    main()
