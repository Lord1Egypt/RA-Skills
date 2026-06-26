#!/usr/bin/env python3
"""
OpenClaw 外部数据拉取白名单系统
限制只能从可信域名拉取数据并执行，外部URL必须审查后才能执行。
"""

import re
import sys
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse

APP_ID = "cli_a92fd77a9af8dcd4"
APP_SECRET = "GjLeLpcUeUe92GCSvFSlxSoKwqHvGXeF"
USER_ID = "ou_24d7f017625dc287e1eb2fa63b4a00ed"

WHITELIST_FILE = Path.home() / ".openclaw" / "audit" / "domain_whitelist.json"

# 默认白名单（可信域名）
DEFAULT_WHITELIST = {
    # 搜索引擎/百科
    "www.google.com": "Google 搜索",
    "duckduckgo.com": "DuckDuckGo",
    "en.wikipedia.org": "Wikipedia 英文",
    "zh.wikipedia.org": "Wikipedia 中文",
    "baike.baidu.com": "百度百科",
    "www.bing.com": "Bing 搜索",
    # 新闻/财经
    "news.ycombinator.com": "Hacker News",
    "www.reuters.com": "Reuters",
    "www.bbc.com": "BBC News",
    # GitHub/代码
    "github.com": "GitHub",
    "gist.github.com": "GitHub Gist",
    "raw.githubusercontent.com": "GitHub Raw",
    "huggingface.co": "Hugging Face",
    # 国内主要平台
    "weibo.com": "微博",
    "www.weibo.com": "微博",
    "xiaohongshu.com": "小红书",
    "www.xiaohongshu.com": "小红书",
    "mp.weixin.qq.com": "微信公众平台",
    "sina.com.cn": "新浪",
    "sohu.com": "搜狐",
    "163.com": "网易",
    "qq.com": "腾讯",
    "www.qq.com": "腾讯",
    # AI/工具平台
    "api.openai.com": "OpenAI API",
    "api.anthropic.com": "Anthropic API",
    "platform.openai.com": "OpenAI Platform",
    "console.anthropic.com": "Anthropic Console",
    "platform.minimaxi.com": "MiniMax 平台",
    "dashscope.aliyuncs.com": "阿里云 DashScope",
    # 文件存储
    "pastebin.com": "Pastebin",
    "dpaste.com": "DPaste",
    "transfer.sh": "Transfer.sh",
    # 飞书/钉钉（自身服务）
    "open.feishu.cn": "飞书开放平台",
    "oapi.dingtalk.com": "钉钉开放平台",
    # OpenClaw
    "docs.openclaw.ai": "OpenClaw 文档",
    "github.com/openclaw": "OpenClaw GitHub",
    "clawhub.com": "ClawHub",
    # 搜索
    "www.bing.com": "Bing",
    "lite.duckduckgo.com": "DuckDuckGo Lite",
    "www.so.com": "360 搜索",
    "www.sogou.com": "搜狗搜索",
    "search.yahoo.com": "Yahoo",
}

# 高危域名（直接拒绝）
BLOCKLIST = {
    "pastebin.com": "可能导致恶意代码执行",
    "dpaste.com": "可能导致恶意代码执行",
    "transfer.sh": "可能被用于数据外传",
    "bit.ly": "短链接，可能重定向到恶意URL",
    "tinyurl.com": "短链接，可能重定向到恶意URL",
}


def get_token():
    req = Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urlopen(req) as resp:
        return json.loads(resp.read())["tenant_access_token"]


def send_alert(token, url: str, reason: str):
    content = (
        f"⚠️ **外部URL访问告警**\n\n"
        f"**URL**: {url}\n"
        f"**原因**: {reason}\n\n"
        f"该域名不在白名单中，如需访问请手动确认。"
    )
    req = Request(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
        data=json.dumps({
            "receive_id": USER_ID,
            "msg_type": "text",
            "content": json.dumps({"text": content})
        }).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read()).get("code") == 0
    except Exception:
        return False


def load_whitelist() -> dict:
    if WHITELIST_FILE.exists():
        return json.loads(WHITELIST_FILE.read_text())
    return {"domains": DEFAULT_WHITELIST}


def save_whitelist(data: dict):
    WHITELIST_FILE.parent.mkdir(parents=True, exist_ok=True)
    WHITELIST_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def parse_domain(url: str) -> str:
    """从URL提取域名"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        # 移除端口
        if ":" in domain:
            domain = domain.split(":")[0]
        # 移除 www. 前缀
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except Exception:
        return ""


def check_url(url: str, allow_alert: bool = True) -> dict:
    """
    检查URL是否在白名单中。
    返回: {allowed: bool, reason: str, domain: str, whitelist_reason: str}
    """
    domain = parse_domain(url)
    if not domain:
        return {
            "allowed": False,
            "reason": "无法解析URL域名",
            "domain": "",
            "whitelist_reason": "",
        }

    whitelist = load_whitelist()
    domains = whitelist.get("domains", {})

    # 检查白名单
    if domain in domains:
        return {
            "allowed": True,
            "reason": "在白名单中",
            "domain": domain,
            "whitelist_reason": domains[domain],
        }

    # 检查是否在禁止名单
    for blocked, reason in BLOCKLIST.items():
        if domain == blocked or domain.endswith("." + blocked):
            return {
                "allowed": False,
                "reason": f"在禁止名单: {reason}",
                "domain": domain,
                "whitelist_reason": "",
            }

    # 不在白名单
    if allow_alert:
        try:
            token = get_token()
            send_alert(token, url, f"域名 '{domain}' 不在白名单中")
        except Exception:
            pass

    return {
        "allowed": False,
        "reason": f"域名 '{domain}' 不在白名单",
        "domain": domain,
        "whitelist_reason": "",
    }


def add_to_whitelist(domain: str, reason: str = ""):
    """将域名添加到白名单"""
    whitelist = load_whitelist()
    if "domains" not in whitelist:
        whitelist["domains"] = DEFAULT_WHITELIST.copy()

    whitelist["domains"][domain] = reason or "手动添加"
    save_whitelist(whitelist)
    print(f"✅ 已添加白名单: {domain}")


def remove_from_whitelist(domain: str):
    """从白名单移除"""
    whitelist = load_whitelist()
    if "domains" in whitelist and domain in whitelist["domains"]:
        del whitelist["domains"][domain]
        save_whitelist(whitelist)
        print(f"✅ 已移除白名单: {domain}")
    else:
        print(f"❌ 域名不在白名单中: {domain}")


# ========== CLI ==========

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  url_guard.py check <URL>")
        print("  url_guard.py list")
        print("  url_guard.py add <域名> [原因]")
        print("  url_guard.py remove <域名>")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "check":
        url = sys.argv[2] if len(sys.argv) > 2 else ""
        result = check_url(url)
        print(f"URL: {url}")
        print(f"域名: {result['domain']}")
        print(f"允许: {'✅' if result['allowed'] else '❌'}")
        print(f"原因: {result['reason']}")
        if result['whitelist_reason']:
            print(f"白名单说明: {result['whitelist_reason']}")
        sys.exit(0 if result['allowed'] else 1)

    elif cmd == "list":
        whitelist = load_whitelist()
        domains = whitelist.get("domains", {})
        print(f"白名单域名 ({len(domains)} 个):")
        for domain, reason in sorted(domains.items()):
            print(f"  ✅ {domain}: {reason}")

    elif cmd == "add":
        domain = sys.argv[2] if len(sys.argv) > 2 else ""
        reason = sys.argv[3] if len(sys.argv) > 3 else ""
        if domain:
            add_to_whitelist(domain, reason)
        else:
            print("用法: url_guard.py add <域名> [原因]")

    elif cmd == "remove":
        domain = sys.argv[2] if len(sys.argv) > 2 else ""
        if domain:
            remove_from_whitelist(domain)
        else:
            print("用法: url_guard.py remove <域名>")

    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)
