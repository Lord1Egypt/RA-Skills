#!/usr/bin/env python3
# Author: geji (built from daily PingCode usage)
# Repo: personal skill workspace

"""
组织架构 — 用户、部门、团队、角色查询
用法:
  python3 scripts/query_users.py                              # 列出所有用户
  python3 scripts/query_users.py --search "张三"            # 按姓名搜索
  python3 scripts/query_users.py --departments                 # 查看部门
  python3 scripts/query_users.py --groups                      # 查看团队
  python3 scripts/query_users.py --roles                       # 查看角色
  python3 scripts/query_users.py --detail                      # 详细信息
"""

import requests, json, os, sys, argparse

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
    parser = argparse.ArgumentParser(description='PingCode 组织架构查询')
    parser.add_argument('--search', help='按姓名搜索用户')
    parser.add_argument('--departments', action='store_true', help='查看部门')
    parser.add_argument('--groups', action='store_true', help='查看团队')
    parser.add_argument('--roles', action='store_true', help='查看角色')
    parser.add_argument('--detail', action='store_true', help='详细信息')
    parser.add_argument('--user_id', help='指定用户 ID')
    args = parser.parse_args()

    token = get_token()
    headers = {'Authorization': f'Bearer {token}'}

    if args.departments:
        depts = fetch_all(f'{BASE}/v1/directory/departments', {}, headers)
        print(f'🏢 部门 ({len(depts)}):
')
        for d in depts:
            parent = d.get('parent',{})
            parent_name = parent.get('name','') if parent else ''
            parent_str = f' → {parent_name}' if parent_name else ''
            print(f'   {d["id"]}  {d.get("name","?")}{parent_str}')
    
    elif args.groups:
        groups = fetch_all(f'{BASE}/v1/directory/groups', {}, headers)
        print(f'👥 团队 ({len(groups)}):
')
        for g in groups:
            print(f'   {g["id"]}  {g.get("name","?")}')
    
    elif args.roles:
        roles = fetch_all(f'{BASE}/v1/directory/roles', {}, headers)
        print(f'🎭 角色 ({len(roles)}):
')
        for r in roles:
            print(f'   {r["id"]}  {r.get("name","?")}')
    
    elif args.user_id:
        r = requests.get(f'{BASE}/v1/directory/users', params={'page_size': 100}, headers=headers)
        users = r.json().get('values', [])
        matched = [u for u in users if u.get('id') == args.user_id]
        if matched:
            u = matched[0]
            print(f'👤 {u.get("display_name","?")} ({u.get("name","?")})')
            print(f'   ID: {u["id"]}')
            print(f'   邮箱: {u.get("email","?")}')
            print(f'   手机: {u.get("phone","?")}')
            print(f'   职位: {u.get("job",{}).get("name","?") if u.get("job") else "?"}')
    else:
        users = fetch_all(f'{BASE}/v1/directory/users', {}, headers)
        
        if args.search:
            matched = [u for u in users if args.search.lower() in u.get('display_name','').lower()
                       or args.search.lower() in u.get('name','').lower()]
            print(f'🔍 搜索 "{args.search}" — 找到 {len(matched)} 人
')
            users = matched
        
        if not args.detail:
            print(f'👤 用户列表 ({len(users)}):
')
            for u in users:
                print(f'   {u["id"]}  {u.get("display_name","?")} ({u.get("name","?")})')
        else:
            for u in users:
                print(f'👤 {u.get("display_name","?")} ({u.get("name","?")})')
                print(f'   ID: {u["id"]} | 邮箱: {u.get("email","?")} | 手机: {u.get("phone","?")}')
                print(f'   职位: {u.get("job",{}).get("name","?") if u.get("job") else "?"}')

if __name__ == '__main__':
    main()
