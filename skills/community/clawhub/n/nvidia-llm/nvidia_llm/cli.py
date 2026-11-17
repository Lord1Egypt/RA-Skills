#!/usr/bin/env python3
"""
nvidia-llm CLI — 命令行
用法:
    nvidia-llm chat "你好"
    nvidia-llm chat "写爬虫" --scene code
    nvidia-llm stream "讲故事" --scene creative
    nvidia-llm status                    # 模型健康状态
    nvidia-llm models
    nvidia-llm models --tag code
    nvidia-llm subscribe                 # 微信扫码订阅
    nvidia-llm subscribe --plan yearly   # 选择年卡
    nvidia-llm activate <激活码>         # 激活VIP
    nvidia-llm invite <邀请码>           # 使用邀请码
    nvidia-llm invite                    # 显示我的邀请码
    nvidia-llm me                        # 我的会员状态
"""

import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="nvidia-llm CLI")
    sub = parser.add_subparsers(dest="cmd")

    # chat
    p_chat = sub.add_parser("chat", help="对话")
    p_chat.add_argument("prompt")
    p_chat.add_argument("--system", "-s", default=None)
    p_chat.add_argument("--scene", "-c", default="default",
        choices=["default","code","fast","reasoning","creative","chinese",
                 "multimodal","edge","finance","medical","translate"])
    p_chat.add_argument("--model", "-m", default=None)

    # stream
    p_stream = sub.add_parser("stream", help="流式对话")
    p_stream.add_argument("prompt")
    p_stream.add_argument("--system", "-s", default=None)
    p_stream.add_argument("--scene", "-c", default="default")

    # status (模型健康)
    sub.add_parser("status", help="模型健康状态")

    # models
    p_models = sub.add_parser("models", help="列出模型")
    p_models.add_argument("--tag", "-t", default=None)

    # test
    p_test = sub.add_parser("test", help="连通性测试")
    p_test.add_argument("--model", "-m", default="ultra")

    # ── 订阅相关 ──
    p_sub = sub.add_parser("subscribe", help="微信扫码订阅VIP")
    p_sub.add_argument("--plan", "-p", default="",
        choices=["", "monthly", "yearly", "lifetime"],
        help="选择套餐: monthly(¥19/月) yearly(¥99/年) lifetime(¥299/永久)")

    p_act = sub.add_parser("activate", help="激活VIP")
    p_act.add_argument("code", help="订阅激活码")

    p_inv = sub.add_parser("invite", help="邀请码")
    p_inv.add_argument("code", nargs="?", default="", help="使用别人的邀请码 (不填则显示自己的)")

    sub.add_parser("me", help="我的会员状态")

    args = parser.parse_args()

    if args.cmd == "chat":
        from .core import AutoRouter
        router = AutoRouter(scene=args.scene)
        if args.model:
            result = router._call_model(args.model, [{"role":"user","content":args.prompt}])
            if "error" in result:
                print(f"❌ {result['error']}")
            else:
                print(result.get("content", ""))
        else:
            result = router.chat(args.prompt, system=args.system)
            if result.get("access_denied"):
                print(result["content"])
            else:
                print(f"[{result['model_alias']}] {result['latency']:.2f}s")
                print(result["content"])

    elif args.cmd == "stream":
        from .core import AutoRouter
        router = AutoRouter(scene=args.scene)
        for chunk in router.stream(args.prompt, system=args.system):
            if chunk["type"] == "meta":
                print(chunk["text"], end="", flush=True)
            elif chunk["type"] == "content":
                print(chunk["text"], end="", flush=True)
        print()

    elif args.cmd == "status":
        from .core import status as _status
        s = _status()
        print(f"{'Model':<20} {'State':<10} {'P50(ms)':<10} {'P95(ms)':<10} {'Fails':<6}")
        print("-" * 60)
        for alias, info in s.items():
            p50 = f"{info['latency_p50']*1000:.0f}" if info['latency_p50'] else "-"
            p95 = f"{info['latency_p95']*1000:.0f}" if info['latency_p95'] else "-"
            print(f"{alias:<20} {info['state']:<10} {p50:<10} {p95:<10} {info['fail_count']:<6}")

    elif args.cmd == "models":
        from .core import models as _models
        m = _models(args.tag)
        for alias, mid in m.items():
            print(f"{alias:<20} {mid}")

    elif args.cmd == "test":
        from .core import AutoRouter
        router = AutoRouter()
        result = router._call_model(args.model, [{"role":"user","content":"你好"}], max_tokens=32)
        if "error" in result:
            print(f"❌ {args.model}: {result['error']}")
        else:
            print(f"✅ {args.model}: {result['content'][:80]} ({result['latency']:.2f}s)")

    # ── 订阅 ──
    elif args.cmd == "subscribe":
        from .core import subscribe
        print(subscribe(args.plan))

    elif args.cmd == "activate":
        from .core import activate
        activate(args.code)

    elif args.cmd == "invite":
        if args.code:
            from .core import invite
            invite(args.code)
        else:
            from .core import my_invite_code, subscribe
            code = my_invite_code()
            print()
            print(f"  你的邀请码: {code}")
            print()
            print("  分享给朋友:")
            print(f"    nvidia-llm invite {code}")
            print()
            print("  邀请奖励:")
            print("    邀请 1 人 → 双方各得 30 天 VIP")
            print("    邀请 3 人 → 免费 90 天")
            print("    邀请12人 → 全年免费")

    elif args.cmd == "me":
        from .core import subscription_status
        print(subscription_status())

    else:
        parser.print_help()


if __name__ == "__main__":
    main()