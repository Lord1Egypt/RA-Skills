# -*- coding: utf-8 -*-
"""
InvAssistant — 钉钉推送脚本
通过钉钉群机器人 Webhook 推送投资信号检查结果。

用法:
  python send_dingtalk.py                     # 推送最新检查结果
  python send_dingtalk.py --webhook <url>     # 自定义 webhook
  python send_dingtalk.py --test              # 发送测试消息

环境变量:
  DINGTALK_WEBHOOK_URL — 钉钉 Webhook URL
  DINGTALK_SECRET      — 加签密钥（可选）

配置指南:
  1. 钉钉群 → 群设置 → 智能群助手 → 添加机器人 → 自定义
  2. 安全设置选一种:
     - 自定义关键词: 设 "信号" "持仓" "检查" 等
     - 加签: 记下 Secret 配到 DINGTALK_SECRET 或 invassistant-config.json
     - IP 白名单: 填服务器 IP
  3. 复制 Webhook URL 到环境变量或配置文件
  4. 限制: 每分钟最多 20 条消息
"""
import json
import urllib.request
import urllib.parse
import os
import sys
import time
import hmac
import hashlib
import base64
import argparse
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_FILE = PROJECT_DIR / "invassistant-config.json"


def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_webhook_url(args_webhook=None):
    if args_webhook:
        return args_webhook
    env_url = os.environ.get("DINGTALK_WEBHOOK_URL")
    if env_url:
        return env_url
    url = load_config().get("adapters", {}).get("dingtalk", {}).get("webhook_url", "")
    if url:
        return url
    print("[错误] 未配置钉钉 Webhook URL")
    print("  设置环境变量 DINGTALK_WEBHOOK_URL 或在 invassistant-config.json 中配置")
    sys.exit(1)


def get_secret():
    secret = os.environ.get("DINGTALK_SECRET")
    if secret:
        return secret
    return load_config().get("adapters", {}).get("dingtalk", {}).get("secret", "")


def sign_url(webhook_url, secret):
    """对 Webhook URL 进行加签。"""
    if not secret:
        return webhook_url
    timestamp = str(round(time.time() * 1000))
    string_to_sign = f"{timestamp}\n{secret}"
    hmac_code = hmac.new(
        secret.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        digestmod=hashlib.sha256
    ).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return f"{webhook_url}&timestamp={timestamp}&sign={sign}"


def send_markdown(webhook_url, title, content):
    """推送 Markdown 消息到钉钉。"""
    payload = {
        "msgtype": "markdown",
        "markdown": {"title": title, "text": content}
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    print(f"  长度: {len(content)} 字符")
    req = urllib.request.Request(
        webhook_url, data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print(f"  errcode: {result.get('errcode')}, errmsg: {result.get('errmsg')}")
        return result


def push_signal(report_text, webhook_url=None, secret=None):
    """推送信号报告（供 portfolio_checker.py 调用）。"""
    url = webhook_url or get_webhook_url()
    sec = secret or get_secret()
    signed_url = sign_url(url, sec)
    print("\n📤 推送到钉钉...")
    title = f"持仓信号检查 | {datetime.now().strftime('%Y-%m-%d')}"
    send_markdown(signed_url, title, report_text)
    print("  推送完成!")


def find_latest_result():
    output_dir = PROJECT_DIR / "output"
    if not output_dir.exists():
        return None
    files = sorted(output_dir.glob("portfolio_*.json"), reverse=True)
    return files[0] if files else None


def format_json_to_markdown(json_path):
    """将 JSON 检查结果格式化为钉钉 Markdown。"""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    timestamp = data.get("timestamp", "未知")
    market_detail = data.get("market_detail", "")
    results = data.get("results", {})

    lines = [
        f"## 📊 持仓信号检查",
        f"**时间**: {timestamp}",
        f"**市场环境**: {market_detail}",
        "",
        "---",
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
            lines.append(f"**{sym}** ${price:.2f}")
            lines.append(f"> 情绪{rl1} 技术{rl2} 市场{rl3} | {action}")
            lines.append("")
        elif strategy == "pullback":
            pb = info.get("pullback", {})
            detail = pb.get("detail", "")
            signal = "⚠️可小加" if pb.get("signal") else "HOLD"
            lines.append(f"**{sym}** ${price:.2f} | {detail} → {signal}")
            lines.append("")
        elif strategy == "hold":
            lines.append(f"**{sym}** ${price:.2f} | HOLD")
            lines.append("")
        elif strategy == "satellite":
            lines.append(f"**{sym}** ${price:.2f} | 卫星不动")
            lines.append("")

    has_signal = data.get("has_signal", False)
    lines.append(f"---")
    lines.append(f"### 👉 {'存在信号，需关注' if has_signal else '今天不交易'}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="InvAssistant 钉钉推送")
    parser.add_argument("--webhook", help="钉钉 Webhook URL")
    parser.add_argument("--test", action="store_true", help="发送测试消息")
    parser.add_argument("--file", help="指定 JSON 结果文件路径")
    args = parser.parse_args()

    webhook_url = get_webhook_url(args.webhook)
    secret = get_secret()
    signed_url = sign_url(webhook_url, secret)

    print(f"{'='*55}")
    print(f"  InvAssistant — 钉钉推送")
    print(f"  加签: {'是' if secret else '否'}")
    print(f"{'='*55}")

    if args.test:
        title = "InvAssistant 测试"
        content = f"## 📊 InvAssistant 测试消息\n\n连接成功! {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        send_markdown(signed_url, title, content)
        return

    if args.file:
        json_path = Path(args.file)
    else:
        json_path = find_latest_result()

    if json_path is None or not json_path.exists():
        print("[错误] 未找到检查结果文件")
        print("  请先运行: python scripts/portfolio_checker.py")
        sys.exit(1)

    print(f"\n[文件] {json_path.name}")
    title = f"持仓信号检查 | {datetime.now().strftime('%Y-%m-%d')}"
    content = format_json_to_markdown(json_path)
    send_markdown(signed_url, title, content)
    print(f"\n{'='*55}")
    print("  推送完成!")
    print(f"{'='*55}")


if __name__ == "__main__":
    main()
