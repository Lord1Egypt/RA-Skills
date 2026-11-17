#!/usr/bin/env python3
"""
贷款资质预审 - SaaS版
调用后端API按次计费，新用户注册送5次免费
"""
import os
import sys
import json
import argparse
from coze_workload_identity import requests

API_BASE = os.environ.get(f"COZE_LOAN_CHECK_API_URL_{SKILL_ID}", os.environ.get("LOAN_CHECK_API_URL", "http://47.109.39.255:8765/api/v4")
USER_KEY = os.environ.get("LOAN_CHECK_USER_KEY", "")


def api_call(endpoint, data=None, method="POST"):
    url = f"{API_BASE.rstrip('/')}/{endpoint}"
    h = {"Content-Type": "application/json"}
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
    result = api_call("register", {"username": args.username})
    print()
    print("=" * 50)
    print("  🎉 注册成功！赠送5次免费调用")
    print("=" * 50)
    print(f"  用户名：{result.get('username')}")
    print(f"  用户密钥：{result.get('user_key')}")
    print(f"  剩余积分：{result.get('credits')} 点")
    print()
    print(f"  ⚠️  请设置环境变量：")
    print(f"  export LOAN_CHECK_USER_KEY={result.get('user_key')}")
    print("=" * 50)
    print()


def cmd_info(args):
    if not USER_KEY:
        print("❌ 请先设置 LOAN_CHECK_USER_KEY 环境变量", file=sys.stderr)
        sys.exit(1)
    result = api_call("user/info", method="GET")
    plan_map = {"free": "免费版", "basic": "基础版", "pro": "专业版", "monthly": "月度会员", "yearly": "年度会员"}
    print()
    print(f"📊 贷款资质预审 账户")
    print("-" * 30)
    print(f"  套餐：{plan_map.get(result.get('plan', 'free'), result.get('plan', '免费版'))}")
    print(f"  剩余积分：{result.get('credits', 0)} 点")
    print(f"  累计调用：{result.get('total_used', 0)} 次")
    if result.get('expire_at'):
        print(f"  到期时间：{result.get('expire_at')}")
    print()
    print("💰 充值微信：17392371127（郭总）")
    print()


def cmd_check(args):
    if not USER_KEY:
        print("❌ 请先设置 LOAN_CHECK_USER_KEY 环境变量", file=sys.stderr)
        print("   注册命令：脚本 register --username 你的名字", file=sys.stderr)
        sys.exit(1)
    print(f"🚀 贷款资质预审中...", file=sys.stderr)
    data = {}
    data['age'] = args.age
    data['income'] = args.income
    if args.credit: data['credit'] = args.credit
    if args.loan_type: data['loan_type'] = args.loan_type
    data['loan_amount'] = args.loan_amount if args.loan_amount else 10
    if args.city: data['city'] = args.city
    result = api_call("loan-check", data)
    remaining = result.get("remaining_credits", 0)
    # 输出完整结果
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(file=sys.stderr)
    print(f"✅ 完成！剩余积分：{remaining} 点", file=sys.stderr)
    print(file=sys.stderr)
    print("💼 企业定制/助贷全案 | 微信 17392371127", file=sys.stderr)


def cmd_services(args):
    result = api_call("services", method="GET")
    services = result.get("services", {})
    pricing = result.get("pricing", {})
    print()
    print("📋 全部AI服务")
    print("-" * 50)
    for key, s in services.items():
        print(f"  • {s['name']} — {s['cost_per_call']}点/次")
    print()
    print("💳 套餐价格")
    print("-" * 50)
    for key, p in pricing.get("plans", {}).items():
        print(f"  • {p['name']}：¥{p['price']} — {p['desc']}")
    print()
    print("💰 充值微信：17392371127（郭总）")
    print()


def main():
    parser = argparse.ArgumentParser(description="贷款资质预审 - SaaS版，1点/次")
    sub = parser.add_subparsers(dest="command")
    r = sub.add_parser("register", help="注册账号，送5次免费")
    r.add_argument("--username", required=True, help="用户名")
    sub.add_parser("info", help="查看账户信息")
    sub.add_parser("services", help="查看全部服务和套餐")
    g = sub.add_parser("check", help="贷款资质预审")
    g.add_argument("--age", required=True, help="年龄")
    g.add_argument("--income", required=True, help="月收入（元）")
    g.add_argument("--credit", default="fair", help="征信: excellent/good/fair/poor")
    g.add_argument("--loan-type", default="consumer", help="贷款类型: consumer/business/mortgage/car")
    g.add_argument("--loan-amount", type=int, default=10, help="期望金额（万）")
    g.add_argument("--city", default="", help="所在城市")
    args = parser.parse_args()
    if args.command == "register":
        cmd_register(args)
    elif args.command == "info":
        cmd_info(args)
    elif args.command == "services":
        cmd_services(args)
    elif args.command == "check":
        cmd_check(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
