#!/usr/bin/env python3
# Author: geji (built from daily PingCode usage)
# Repo: personal skill workspace

"""
项目管理 — 项目、迭代、发布
用法:
  python3 scripts/query_projects.py                              # 列出所有项目
  python3 scripts/query_projects.py --name "合规"                # 按名称搜索
  python3 scripts/query_projects.py --project_id xxx             # 查看单个项目详情
  python3 scripts/query_projects.py --sprints                     # 查看所有迭代
  python3 scripts/query_projects.py --releases                    # 查看所有发布
  python3 scripts/query_projects.py --project_id xxx --sprints    # 查看指定项目的迭代
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
    return r.json().get('access_token')

def fetch_all(url, params, headers):
    page = 0
    all_items = []
    while True:
        p = {**params, 'page_size': 100, 'page_index': page}
        r = requests.get(url, params=p, headers=headers)
        if r.status_code != 200:
            print(f'⚠️ 查询失败 {url}: {r.status_code} {r.text[:200]}')
            break
        vals = r.json().get('values', [])
        if not vals:
            break
        all_items.extend(vals)
        page += 1
    return all_items

def main():
    parser = argparse.ArgumentParser(description='PingCode 项目查询工具')
    parser.add_argument('--name', help='项目名称（模糊匹配）')
    parser.add_argument('--project_id', help='项目 ID')
    parser.add_argument('--sprints', action='store_true', help='查看迭代')
    parser.add_argument('--releases', action='store_true', help='查看发布')
    parser.add_argument('--members', action='store_true', help='查看成员')
    parser.add_argument('--detail', action='store_true', help='详细信息')
    parser.add_argument('--all_projects_sprints', action='store_true', help='所有项目的迭代')
    args = parser.parse_args()

    token = get_token()
    headers = {'Authorization': f'Bearer {token}'}

    if args.project_id:
        pid = args.project_id
        # 项目详情
        r = requests.get(f'{BASE}/v1/agile/projects/{pid}', headers=headers)
        if r.status_code == 200:
            p = r.json()
            print(f'📦 {p["id"]}  {p.get("name","?")}')
            print(f'   描述: {p.get("description","")}')
            print(f'   创建时间: {p.get("created_at","?")}')
        else:
            print(f'❌ 查询项目失败: {r.text[:200]}')
            return
        
        # 迭代
        if args.sprints or args.detail:
            sprints = fetch_all(f'{BASE}/v1/agile/projects/{pid}/sprints', {}, headers)
            print(f'
📋 迭代 ({len(sprints)}):')
            for s in sprints:
                status = s.get('status', '?')
                name = s.get('name', '?')
                start = s.get('start_date', '?')
                end = s.get('end_date', '?')
                print(f'   [{status}] {name} ({start} ~ {end})')
        
        # 发布
        if args.releases or args.detail:
            releases = fetch_all(f'{BASE}/v1/agile/projects/{pid}/releases', {}, headers)
            print(f'
🚀 发布 ({len(releases)}):')
            for r in releases:
                name = r.get('name', '?')
                status = r.get('status', '?')
                print(f'   [{status}] {name}')
        
        # 成员
        if args.members or args.detail:
            members = fetch_all(f'{BASE}/v1/agile/projects/{pid}/members', {}, headers)
            print(f'
👥 成员 ({len(members)}):')
            for m in members:
                user = m.get('user', {})
                role = m.get('role', {})
                print(f'   {user.get("display_name","?")} — {role.get("name","?")}')
    
    elif args.sprints and args.all_projects_sprints:
        # 所有项目的迭代
        projects = fetch_all(f'{BASE}/v1/agile/projects', {}, headers)
        for p in projects:
            pid = p['id']
            pname = p.get('name','?')
            sprints = fetch_all(f'{BASE}/v1/agile/projects/{pid}/sprints', {}, headers)
            active = [s for s in sprints if s.get('status') in ('active', 'in_progress')]
            if active:
                print(f'📦 {pname}')
                for s in active:
                    print(f'   🔄 {s.get("name","?")} ({s.get("start_date","?")} ~ {s.get("end_date","?")})')
    
    elif args.name:
        # 按名称查询
        projects = fetch_all(f'{BASE}/v1/agile/projects', {}, headers)
        matched = [p for p in projects if args.name.lower() in p.get('name','').lower()]
        print(f'找到 {len(matched)} 个匹配的项目:
')
        for p in matched:
            print(f'📦 {p["id"]}  {p.get("name","?")}')
            if args.detail:
                print(f'   创建时间: {p.get("created_at","?")}')
            print()
    
    else:
        # 列出全部
        projects = fetch_all(f'{BASE}/v1/agile/projects', {}, headers)
        print(f'📊 共 {len(projects)} 个项目
')
        for p in projects:
            print(f'📦 {p["id"]}  {p.get("name","?")}')

if __name__ == '__main__':
    main()
