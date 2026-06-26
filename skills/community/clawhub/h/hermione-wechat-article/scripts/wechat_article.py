#!/usr/bin/env python3
"""
微信公众号文章抓取工具
用法: python wechat_article.py "公众号名称" [文章数]
"""

import requests
import json
import sys
import re
import time
import os
from urllib.parse import urlparse, parse_qs

# Cookie 文件路径
COOKIE_FILE = os.path.expanduser("~/.openclaw/skills/wechat-article/scripts/wechat_cookie.env")

def load_cookie():
    """加载 Cookie"""
    cookie_str = """ua_id=4mddjU5uFGX8YHjeAAAAAOMDvaonFUznOnd6P3pOdc8=; wxuin=72383668830005; mm_lang=zh_CN; pac_uid=0_xBBm9AMJTX4Tx; omgid=0_xBBm9AMJTX4Tx; _qimei_uuid42=1a305171e0510052c8de00f4e90b24d90c08ea4687; _qimei_fingerprint=2290dcf391b9ca981dc3afd04525d36d; _qimei_q36=; _qimei_h38=2db824f9c8de00f4e90b24d90200000311a305; _clck=1xzda43|1|g44|0; uuid=1eaa808f508fafc0d230661fc2037bf3; rand_info=CAESIHUHHNWBXly7ao9EfgfSwfUNJIO746Chf9qTtU7ylMfA; slave_bizuin=3957958460; data_bizuin=3957958460; bizuin=3957958460; data_ticket=VyL1SvQ/ksJw7A5NdcuT06ISrTSKHmS/Od2qu8rR7017KE0bwAswRpfDemdBVbjO; slave_sid=VExZNkZvVkxTQUJFSUVpb1pKZUxPUVBzSXpRZkw3U0l0ZUk5R1ZVUE83Z1RTSmlQQWhsaGo5OTUzZTdUdV9CWVlxOE9aVEEyb2JnbUhyb19aRlE5bElVWkhDUE01TGU1T0NDM05uSkdKWk1zeVV5R2pGN3pwZGtyM1ZMZnZ3TmttUm4zUkZPUEFPdEg2TkdL; slave_user=gh_7d44b8b99b3a; xid=c1afa806da5f16018cf4e35f0170ca92; _clsk=1kqk3ua|1772776804862|14|1|mp.weixin.qq.com/weheat-agent/payload/record; rewardsn=; wxtokenkey=777"""
    return cookie_str

def get_token(cookie):
    """获取 token"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Cookie": cookie,
        "Referer": "https://mp.weixin.qq.com/"
    }
    r = requests.get("https://mp.weixin.qq.com/", headers=headers, allow_redirects=True)
    parsed = urlparse(r.url)
    params = parse_qs(parsed.query)
    return params.get('token', [None])[0]

def search_fakeid(cookie, token, name):
    """搜索公众号 fakeid"""
    url = "https://mp.weixin.qq.com/cgi-bin/searchbiz"
    params = {
        "action": "search_biz",
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "random": str(time.time()),
        "query": name
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Cookie": cookie,
        "Referer": "https://mp.weixin.qq.com/"
    }
    r = requests.get(url, params=params, headers=headers)
    data = r.json()
    
    if data.get("base_resp", {}).get("ret") == 0 and data.get("list"):
        return data["list"][0]["fakeid"], data["list"][0]["nickname"]
    return None, None

def get_article_list(cookie, token, fakeid, count=10):
    """获取公众号文章列表"""
    url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
    params = {
        "action": "list_ex",
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "random": str(time.time()),
        "fakeid": fakeid,
        "type": "9",
        "count": count,
        "begin": "0"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Cookie": cookie,
        "Referer": "https://mp.weixin.qq.com/"
    }
    r = requests.get(url, params=params, headers=headers)
    data = r.json()
    
    if data.get("base_resp", {}).get("ret") == 0:
        return data.get("app_msg_list", [])
    return []

def main():
    if len(sys.argv) < 2:
        print("用法: python wechat_article.py \"公众号名称\" [文章数]")
        print("示例: python wechat_article.py \"分析派迈缇\" 10")
        sys.exit(1)
    
    name = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    print(f"🔍 搜索公众号: {name}")
    
    cookie = load_cookie()
    
    # 获取 token
    print("🔑 获取 token...")
    token = get_token(cookie)
    if not token:
        print("❌ 获取 token 失败，Cookie 可能已失效")
        print("请重新获取 Cookie 并更新脚本")
        sys.exit(1)
    print(f"✅ Token 获取成功")
    
    # 搜索公众号
    print(f"🔍 搜索公众号...")
    fakeid, nickname = search_fakeid(cookie, token, name)
    if not fakeid:
        print(f"❌ 未找到公众号: {name}")
        sys.exit(1)
    print(f"✅ 找到公众号: {nickname}")
    
    # 获取文章列表
    print(f"📄 获取文章列表 (前{count}篇)...")
    articles = get_article_list(cookie, token, fakeid, count)
    
    if not articles:
        print("⚠️  没有找到文章")
        sys.exit(1)
    
    print(f"\n✅ 获取到 {len(articles)} 篇文章:\n")
    
    for i, art in enumerate(articles, 1):
        print(f"{i}. {art.get('title', '无标题')}")
        print(f"   链接: {art.get('link', '无链接')}")
        print()
    
    return articles

if __name__ == "__main__":
    main()
