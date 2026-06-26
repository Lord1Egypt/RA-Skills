#!/usr/bin/env python3
# Author: geji (built from daily PingCode usage)
# Repo: personal skill workspace

"""
活动记录 & 评论 & 关注人 — 工作项目的动态查询
用法:
  python3 scripts/query_activities.py --work_item_id xxx            # 查看某个工作项的动态
  python3 scripts/query_activities.py --work_item_id xxx --comments # 查看评论
  python3 scripts/query_activities.py --work_item_id xxx --hours    # 查看工时
  python3 scripts/query_activities.py --work_item_id xxx --followers # 关注人
  python3 scripts/query_activities.py --work_item_id xxx --relations # 关联项
"""

import requests, json, os, sys, argparse
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

def main():
    parser = argparse.ArgumentParser(description='PingCode 动态/评论/工时查询')
    parser.add_argument('--work_item_id', required=True, help='工作项 ID')
    parser.add_argument('--comments', action='store_true', help='查看评论')
    parser.add_argument('--hours', action='store_true', help='查看工时')
    parser.add_argument('--followers', action='store_true', help='查看关注人')
    parser.add_argument('--relations', action='store_true', help='查看关联项')
    parser.add_argument('--limit', type=int, default=20, help='显示条数')
    args = parser.parse_args()

    token = get_token()
    headers = {'Authorization': f'Bearer {token}'}
    
    wid = args.work_item_id
    print(f'📝 工作项 {wid} 的活动记录
')
    
    # 动态
    if not args.comments and not args.hours and not args.followers and not args.relations:
        args.comments = True  # default: show activities
    
    # 动态/活动记录
    r = requests.get(f'{BASE}/v1/activities', params={
        'principal_type': 'work_item', 'principal_id': wid, 'page_size': args.limit
    }, headers=headers)
    if r.status_code == 200:
        activities = r.json().get('values', [])
        print(f'🔄 动态 ({len(activities)}):')
        for a in activities[:args.limit]:
            user = a.get('user',{})
            action = a.get('action','?')
            created = a.get('created_at','?')[:16]
            print(f'   [{created}] {user.get("display_name","?")} {action}')
            detail = a.get('detail','')
            if detail:
                print(f'       {str(detail)[:100]}')
    
    # 评论
    if args.comments:
        r = requests.get(f'{BASE}/v1/comments', params={
            'principal_type': 'work_item', 'principal_id': wid, 'page_size': args.limit
        }, headers=headers)
        if r.status_code == 200:
            comments = r.json().get('values', [])
            print(f'
💬 评论 ({len(comments)}):')
            for c in comments[:args.limit]:
                user = c.get('user',{})
                created = c.get('created_at','?')[:16]
                content = c.get('content','')[:200]
                print(f'   [{created}] {user.get("display_name","?")}: {content}')
    
    # 工时
    if args.hours:
        r = requests.get(f'{BASE}/v1/work_hours', params={
            'principal_type': 'work_item', 'principal_id': wid, 'page_size': args.limit
        }, headers=headers)
        if r.status_code == 200:
            hours = r.json().get('values', [])
            print(f'
⏱️ 工时 ({len(hours)}):')
            total = 0
            for h in hours[:args.limit]:
                user = h.get('user',{})
                spent = h.get('spent_hours', 0)
                desc = h.get('description','')
                total += spent
                print(f'   {user.get("display_name","?")} {spent}h — {desc}')
            if total:
                print(f'   合计: {total}h')
    
    # 关注人
    if args.followers:
        r = requests.get(f'{BASE}/v1/followers', params={
            'principal_type': 'work_item', 'principal_id': wid, 'page_size': args.limit
        }, headers=headers)
        if r.status_code == 200:
            followers = r.json().get('values', [])
            print(f'
👁️ 关注人 ({len(followers)}):')
            for f in followers:
                user = f.get('user',{})
                print(f'   {user.get("display_name","?")}')
    
    # 关联项
    if args.relations:
        r = requests.get(f'{BASE}/v1/relationships', params={
            'principal_type': 'work_item', 'principal_id': wid, 'page_size': args.limit
        }, headers=headers)
        if r.status_code == 200:
            relations = r.json().get('values', [])
            print(f'
🔗 关联 ({len(relations)}):')
            for r in relations[:args.limit]:
                target = r.get('target',{})
                relation_type = r.get('type','?')
                print(f'   [{relation_type}] {target.get("title","?")} ({target.get("type","?")})')

if __name__ == '__main__':
    main()
