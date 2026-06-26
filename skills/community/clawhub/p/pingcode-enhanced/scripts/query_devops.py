#!/usr/bin/env python3
# Author: geji (built from daily PingCode usage)
# Repo: personal skill workspace

"""
DevOps 集成 — 代码仓库、提交、PR、构建、部署查询
用法:
  python3 scripts/query_devops.py --repos          # 查看代码仓库
  python3 scripts/query_devops.py --commits        # 最近提交
  python3 scripts/query_devops.py --pr             # 最近 PR
  python3 scripts/query_devops.py --builds         # 最近构建
  python3 scripts/query_devops.py --deploys        # 最近部署
  python3 scripts/query_devops.py --limit 10       # 控制显示条数
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
        p = {**params, 'page_size': 50, 'page_index': page}
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
    parser = argparse.ArgumentParser(description='PingCode DevOps 信息查询')
    parser.add_argument('--repos', action='store_true', help='查看代码仓库')
    parser.add_argument('--commits', action='store_true', help='最近提交')
    parser.add_argument('--pr', action='store_true', help='最近 Pull Request')
    parser.add_argument('--builds', action='store_true', help='最近构建')
    parser.add_argument('--deploys', action='store_true', help='最近部署')
    parser.add_argument('--limit', type=int, default=10, help='显示条数')
    args = parser.parse_args()

    token = get_token()
    headers = {'Authorization': f'Bearer {token}'}

    if not any([args.repos, args.commits, args.pr, args.builds, args.deploys]):
        args.repos = True

    if args.repos:
        repos = fetch_all(f'{BASE}/v1/code/repositories', {}, headers)
        print(f'📦 代码仓库 ({len(repos)}):' if repos else '📦 代码仓库: 暂无数据')
        for r in repos[:args.limit]:
            print(f'   {r.get("id","?")}  {r.get("name","?")} ({r.get("type","?")})')
        if repos:
            print()

    if args.commits:
        commits = fetch_all(f'{BASE}/v1/code/commits', {}, headers)
        if commits:
            print(f'📝 最近提交 ({len(commits)}):')
            for c in commits[:args.limit]:
                author = c.get('author',{})
                msg = c.get('message','')[:80]
                date = c.get('created_at','?')[:16]
                repo = c.get('repository',{}).get('name','?')
                print(f'   [{date}] [{repo}] {author.get("display_name","?")}: {msg}')
        else:
            print('📝 最近提交: 暂无数据')
        print()

    if args.pr:
        prs = fetch_all(f'{BASE}/v1/code/pull_requests', {}, headers)
        if prs:
            print(f'🔄 Pull Requests ({len(prs)}):')
            for pr in prs[:args.limit]:
                author = pr.get('author',{})
                status = pr.get('state','?')
                title = pr.get('title','?')
                repo = pr.get('repository',{}).get('name','?')
                print(f'   [{status}] [{repo}] {title} — {author.get("display_name","?")}')
        else:
            print('🔄 Pull Requests: 暂无数据')
        print()

    if args.builds:
        builds = fetch_all(f'{BASE}/v1/build/build_records', {}, headers)
        if builds:
            print(f'🏗️ 构建记录 ({len(builds)}):')
            for b in builds[:args.limit]:
                status = b.get('status','?')
                name = b.get('name','?')
                date = b.get('created_at','?')[:16]
                print(f'   [{status}] {name} ({date})')
        else:
            print('🏗️ 构建记录: 暂无数据')
        print()

    if args.deploys:
        deploys = fetch_all(f'{BASE}/v1/release/deployments', {}, headers)
        if deploys:
            print(f'🚀 部署记录 ({len(deploys)}):')
            for d in deploys[:args.limit]:
                status = d.get('status','?')
                env = d.get('environment',{}).get('name','?')
                name = d.get('name','?')
                date = d.get('created_at','?')[:16]
                print(f'   [{status}] [{env}] {name} ({date})')
        else:
            print('🚀 部署记录: 暂无数据')

if __name__ == '__main__':
    main()
