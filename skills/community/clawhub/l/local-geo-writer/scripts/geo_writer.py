#!/usr/bin/env python3
"""
GEO文章生成器 - SaaS版 v3.0
调用后端API按次计费，无需自备API Key
新用户注册送5次免费额度
"""
import os
import sys
import json
import argparse
from coze_workload_identity import requests

# ========== API配置 ==========
SKILL_ID = os.environ.get("SKILL_ID", "7663702611819855908")

API_BASE = os.environ.get(
    f"COZE_GEO_API_URL_{SKILL_ID}",
    os.environ.get("GEO_API_URL", "http://47.109.39.255:8765/api/v4")
)
USER_KEY = (
    os.environ.get(f"COZE_GEO_USER_KEY_{SKILL_ID}")
    or os.environ.get("GEO_USER_KEY", "")
)


def api_call(endpoint, data=None, method="POST", headers=None):
    """统一API调用"""
    url = f"{API_BASE.rstrip('/')}/{endpoint}"
    h = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    if USER_KEY:
        h["X-User-Key"] = USER_KEY
    try:
        if method == "GET":
            resp = requests.get(url, headers=h, params=data or {}, timeout=30)
        else:
            resp = requests.post(url, headers=h, json=data or {}, timeout=60)
        if resp.status_code >= 400:
            try:
                err = resp.json()
                msg = err.get("detail", str(err))
            except:
                msg = resp.text
            print(f"❌ API错误 ({resp.status_code}): {msg}", file=sys.stderr)
            if resp.status_code == 402:
                print("\n💡 余额不足！充值请联系微信 17392371127", file=sys.stderr)
            sys.exit(1)
        return resp.json()
    except Exception as e:
        print(f"❌ 网络错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


def cmd_register(args):
    """注册账号，送5次免费"""
    result = api_call("register", {"username": args.username})
    print()
    print("=" * 50)
    print("  🎉 注册成功！赠送5次免费调用")
    print("=" * 50)
    print(f"  用户名：{result.get('username')}")
    print(f"  用户密钥：{result.get('user_key')}")
    print(f"  剩余次数：{result.get('credits')} 次")
    print()
    print("  ⚠️  请保存好用户密钥，设置为环境变量：")
    print(f"  export GEO_USER_KEY={result.get('user_key')}")
    print("=" * 50)
    print()


def cmd_info(args):
    """查看用户信息"""
    if not USER_KEY:
        print("❌ 请先设置 GEO_USER_KEY 环境变量", file=sys.stderr)
        sys.exit(1)
    result = api_call("user/info", method="GET")
    plan_map = {"free": "免费版", "basic": "基础版", "pro": "专业版", "monthly": "月度会员", "yearly": "年度会员"}
    print()
    print("📊 账户信息")
    print("-" * 30)
    print(f"  用户名：{result.get('username')}")
    print(f"  套餐：{plan_map.get(result.get('plan', 'free'), result.get('plan', '免费版'))}")
    print(f"  剩余积分：{result.get('credits', 0)} 点")
    print(f"  累计调用：{result.get('total_used', 0)} 次")
    if result.get('expire_at'):
        print(f"  到期时间：{result.get('expire_at')}")
    print()
    print("💡 充值/升级：联系微信 17392371127（郭总）")
    print()


def cmd_generate(args):
    """生成GEO文章"""
    if not USER_KEY:
        print("❌ 请先设置 GEO_USER_KEY 环境变量（注册后获取）", file=sys.stderr)
        print("   注册命令：geo_writer.py register --username 你的名字", file=sys.stderr)
        sys.exit(1)
    
    print(f"🔍 正在生成GEO文章：{args.keyword}...", file=sys.stderr)
    
    result = api_call("geo-writer", {
        "keyword": args.keyword,
        "industry": args.industry or "general",
        "article_type": args.type or "guide",
        "word_count": args.words or 1500,
    })
    
    article = result.get("article", "")
    remaining = result.get("remaining_credits", 0)
    
    # 输出到stdout
    print(article)
    print(file=sys.stderr)
    print(f"✅ 生成完成！剩余积分：{remaining} 点", file=sys.stderr)
    print(f"📝 字数：约{result.get('word_count', 0)}字", file=sys.stderr)
    
    # 保存到文件
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(article)
        print(f"💾 已保存到：{args.output}", file=sys.stderr)
    
    print(file=sys.stderr)
    print("💼 企业级GEO全案服务 | 微信 17392371127", file=sys.stderr)


def cmd_services(args):
    """查看所有服务"""
    result = api_call("services", method="GET")
    services = result.get("services", {})
    pricing = result.get("pricing", {})
    
    print()
    print("📋 全部AI服务")
    print("-" * 50)
    for key, s in services.items():
        print(f"  • {s['name']} — {s['cost_per_call']}点/次")
        print(f"    {s['description']}")
    print()
    print("💳 套餐价格")
    print("-" * 50)
    for key, p in pricing.get("plans", {}).items():
        print(f"  • {p['name']}：¥{p['price']} — {p['desc']}")
    print()
    print(f"  免费额度：{pricing.get('free_quota', 5)}次/新用户")
    print()
    print("💰 充值微信：17392371127（郭总）")
    print()


def main():
    parser = argparse.ArgumentParser(description="GEO文章生成器 - SaaS版")
    sub = parser.add_subparsers(dest="command")
    
    # 注册
    r = sub.add_parser("register", help="注册账号，送5次免费")
    r.add_argument("--username", required=True, help="用户名")
    
    # 用户信息
    sub.add_parser("info", help="查看账户信息")
    
    # 服务列表
    sub.add_parser("services", help="查看全部服务和价格")
    
    # 生成文章
    g = sub.add_parser("generate", help="生成GEO文章")
    g.add_argument("--keyword", required=True, help="核心关键词")
    g.add_argument("--industry", default="", help="行业")
    g.add_argument("--type", default="guide", help="文章类型: guide/howto/review/comparison/news")
    g.add_argument("--words", type=int, default=1500, help="目标字数")
    g.add_argument("--output", "-o", default="", help="保存到文件")
    
    args = parser.parse_args()
    
    if args.command == "register":
        cmd_register(args)
    elif args.command == "info":
        cmd_info(args)
    elif args.command == "services":
        cmd_services(args)
    elif args.command == "generate":
        cmd_generate(args)
    else:
        parser.print_help()
        print()
        print("💡 新用户先注册：geo_writer.py register --username 你的名字", file=sys.stderr)


if __name__ == "__main__":
    main()
