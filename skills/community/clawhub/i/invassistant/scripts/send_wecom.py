# -*- coding: utf-8 -*-
"""
InvAssistant — 企业微信推送脚本
推送投资信号检查结果到企业微信群。

用法:
  python send_wecom.py                        # 推送最新检查结果
  python send_wecom.py --webhook <url>        # 使用自定义 webhook
  python send_wecom.py --test                 # 发送测试消息

环境变量:
  WECOM_WEBHOOK_URL — 企业微信 Webhook 地址（优先级高于配置文件）

配置指南:
  1. 企业微信群 → 群设置 → 群机器人 → 添加自定义机器人
  2. 复制 Webhook URL 到配置文件或环境变量
  3. 企微 Markdown 消息限制: 4096 字节
"""
import json
import urllib.request
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_FILE = PROJECT_DIR / "invassistant-config.json"


def load_config():
    """加载配置文件。"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_webhook_url(args_webhook=None):
    """获取 Webhook URL，优先级：命令行参数 > 环境变量 > 配置文件。"""
    if args_webhook:
        return args_webhook

    env_url = os.environ.get("WECOM_WEBHOOK_URL")
    if env_url:
        return env_url

    config = load_config()
    url = config.get("adapters", {}).get("wechatwork", {}).get("webhook_url", "")
    if url:
        return url

    print("[错误] 未配置企微 Webhook URL")
    print("  方式 1: 设置环境变量 WECOM_WEBHOOK_URL")
    print("  方式 2: 在 invassistant-config.json 中配置 adapters.wechatwork.webhook_url")
    print("  方式 3: 使用 --webhook 参数")
    sys.exit(1)


def send_markdown(webhook_url, content):
    """推送 Markdown 消息到企微。"""
    # 企微限制 4096 字节
    content_bytes = content.encode("utf-8")
    if len(content_bytes) > 4000:
        content = content[:2000] + "\n\n... (内容已截断，完整版请查看 JSON 文件)"

    payload = {"msgtype": "markdown", "markdown": {"content": content}}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    print(f"  消息长度: {len(content)} 字符 / {len(data)} 字节")

    req = urllib.request.Request(
        webhook_url, data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print(f"  errcode: {result.get('errcode')}, errmsg: {result.get('errmsg')}")
        return result


def push_signal(report_text, webhook_url=None):
    """推送信号报告（供 portfolio_checker.py 调用）。"""
    url = webhook_url or get_webhook_url()
    print("\n📤 推送到企业微信...")
    send_markdown(url, report_text)
    print("  推送完成!")


def find_latest_result():
    """查找最新的检查结果 JSON 文件。"""
    output_dir = PROJECT_DIR / "output"
    if not output_dir.exists():
        return None
    files = sorted(output_dir.glob("portfolio_*.json"), reverse=True)
    return files[0] if files else None


def format_json_to_markdown(json_path):
    """将 JSON 检查结果格式化为企微 Markdown。"""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    timestamp = data.get("timestamp", "未知")
    market_detail = data.get("market_detail", "")
    results = data.get("results", {})

    lines = [
        f"**📊 持仓信号检查 | {timestamp}**",
        f"市场环境: {market_detail}",
        ""
    ]

    for sym, info in results.items():
        strategy = info.get("strategy", "")
        price = info.get("price", 0)

        if strategy == "redline":
            rl = info.get("redline", {})
            rl1 = "✅" if rl.get("red_line_1", {}).get("passed") else "❌"
            rl2 = "✅" if rl.get("red_line_2", {}).get("passed") else "❌"
            rl3 = "✅" if rl.get("red_line_3", {}).get("passed") else "❌"
            action = rl.get("action", "")
            lines.append(f"**{sym}** ${price:.2f} | {rl1}{rl2}{rl3} | {action}")
        elif strategy == "pullback":
            pb = info.get("pullback", {})
            detail = pb.get("detail", "")
            signal = "⚠️" if pb.get("signal") else "—"
            lines.append(f"**{sym}** ${price:.2f} | {detail} {signal}")
        elif strategy == "hold":
            lines.append(f"**{sym}** ${price:.2f} | HOLD")
        elif strategy == "satellite":
            lines.append(f"**{sym}** ${price:.2f} | 卫星不动")

    has_signal = data.get("has_signal", False)
    lines.append(f"\n👉 **{'存在信号' if has_signal else '今天不交易'}**")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="InvAssistant 企微推送")
    parser.add_argument("--webhook", help="企微 Webhook URL")
    parser.add_argument("--test", action="store_true", help="发送测试消息")
    parser.add_argument("--file", help="指定 JSON 结果文件路径")
    args = parser.parse_args()

    webhook_url = get_webhook_url(args.webhook)

    print(f"{'='*55}")
    print(f"  InvAssistant — 企微推送")
    print(f"{'='*55}")

    if args.test:
        test_msg = f"**📊 InvAssistant 测试消息**\n\n连接成功! {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        send_markdown(webhook_url, test_msg)
        return

    # 查找结果文件
    if args.file:
        json_path = Path(args.file)
    else:
        json_path = find_latest_result()

    if json_path is None or not json_path.exists():
        print("[错误] 未找到检查结果文件")
        print("  请先运行: python scripts/portfolio_checker.py")
        sys.exit(1)

    print(f"\n[文件] {json_path.name}")
    content = format_json_to_markdown(json_path)
    send_markdown(webhook_url, content)
    print(f"\n{'='*55}")
    print("  推送完成!")
    print(f"{'='*55}")


if __name__ == "__main__":
    main()
