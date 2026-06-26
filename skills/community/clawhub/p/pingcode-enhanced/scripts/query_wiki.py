#!/usr/bin/env python3
# Author: geji (built from daily PingCode usage)
# Repo: personal skill workspace

"""
知识管理 — 知识库、页面查询
用法:
  python3 scripts/query_wiki.py                               # 列出所有知识库空间
  python3 scripts/query_wiki.py --space_id xxx                # 查看空间下的页面
  python3 scripts/query_wiki.py --space_id xxx --content      # 查看页面内容
  python3 scripts/query_wiki.py --search "项目名称"         # 按标题搜索页面
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
            break
        vals = r.json().get('values', [])
        if not vals:
            break
        all_items.extend(vals)
        page += 1
    return all_items

def main():
    parser = argparse.ArgumentParser(description='PingCode 知识管理查询')
    parser.add_argument('--space_id', help='知识库空间 ID')
    parser.add_argument('--search', help='搜索页面')
    parser.add_argument('--content', action='store_true', help='查看页面正文')
    parser.add_argument('--page_id', help='查看指定页面')
    args = parser.parse_args()

    token = get_token()
    headers = {'Authorization': f'Bearer {token}'}

    if args.page_id:
        r = requests.get(f'{BASE}/v1/wiki/pages/{args.page_id}', headers=headers)
        if r.status_code == 200:
            page = r.json()
            print(f'📄 {page.get("title","?")}')
            print(f'   空间: {page.get("space",{}).get("name","?")}')
            print(f'   最后更新: {page.get("updated_at","?")}')
            if args.content:
                r2 = requests.get(f'{BASE}/v1/wiki/pages/{args.page_id}/content', headers=headers)
                if r2.status_code == 200:
                    content = r2.json().get('content','')
                    print(f'
📝 正文内容:
{content[:2000]}')
        else:
            print(f'❌ 查询失败: {r.text[:200]}')
        return

    if args.space_id:
        r = requests.get(f'{BASE}/v1/wiki/spaces/{args.space_id}', headers=headers)
        if r.status_code == 200:
            space = r.json()
            print(f'📚 知识库: {space.get("name","?")}')
            print(f'   描述: {space.get("description","")}')
        
        pages = fetch_all(f'{BASE}/v1/wiki/spaces/{args.space_id}/pages', {}, headers)
        print(f'
📄 页面 ({len(pages)}):')
        
        if args.search:
            pages = [p for p in pages if args.search.lower() in p.get('title','').lower()]
            print(f'🔍 搜索 "{args.search}" — 找到 {len(pages)} 个页面
')
        
        for p in pages:
            print(f'   {p["id"]}  {p.get("title","?")} (更新: {p.get("updated_at","?")[:10]})')
    
    else:
        spaces = fetch_all(f'{BASE}/v1/wiki/spaces', {}, headers)
        if not spaces:
            print("⚠️ 此应用没有知识库权限。PingCode 无需额外授权，可以直接访问。")
            print("   可能是知识库功能未开启，或者你还没有创建任何空间。")
            print(f'   API 响应: {r.text[:200]}' if 'r' in dir() else '')
            return
        
        print(f'📚 知识库空间 ({len(spaces)}):
')
        for s in spaces:
            print(f'   {s["id"]}  {s.get("name","?")}')

if __name__ == '__main__':
    main()
