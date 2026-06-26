# -*- coding: utf-8 -*-
"""
InvAssistant — 飞书推送脚本
通过飞书群机器人 Webhook 推送投资信号检查结果。

用法:
  python send_feishu.py                       # 推送最新检查结果
  python send_feishu.py --webhook <url>       # 自定义 webhook
  python send_feishu.py --test                # 发送测试消息

环境变量:
  FEISHU_WEBHOOK_URL — 飞书 Webhook URL
  FEISHU_SECRET      — 签名密钥（可选）

配置指南:
  1. 飞书群 → 设置 → 群机器人 → 添加机器人 → 自定义机器人
  2. 安全设置:
     - 签名校验: 记下 Secret → FEISHU_SECRET（推荐）
     - 自定义关键词: 设 "信号" "持仓" "检查" 等
     - IP 白名单: 填服务器 IP
  3. 复制 Webhook URL 到环境变量或配置文件
  4. 限制: 每分钟 5 条, 每小时 100 条
"""
import json
import urllib.request
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
    env_url = os.environ.get("FEISHU_WEBHOOK_URL")
    if env_url:
        return env_url
    url = load_config().get("adapters", {}).get("feishu", {}).get("webhook_url", "")
    if url:
        return url
    print("[错误] 未配置飞书 Webhook URL")
    print("  设置环境变量 FEISHU_WEBHOOK_URL 或在 invassistant-config.json 中配置")
    sys.exit(1)


def get_secret():
    s = os.environ.get("FEISHU_SECRET")
    if s:
        return s
    return load_config().get("adapters", {}).get("feishu", {}).get("secret", "")


def gen_sign(secret):
    """生成飞书签名。"""
    if not secret:
        return None, None
    timestamp = str(int(time.time()))
    hmac_code = hmac.new(
        f"{timestamp}\n{secret}".encode("utf-8"),
        digestmod=hashlib.sha256
    ).digest()
    return timestamp, base64.b64encode(hmac_code).decode("utf-8")


def md_to_post_content(md_text):
    """将 Markdown 转为飞书 post 富文本格式。"""
    lines = md_text.split("\n")
    content_lines = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith("# "):
            content_lines.append([{"tag": "text", "text": s.lstrip("# ").strip(), "style": ["bold"]}])
        elif s.startswith("## "):
            content_lines.append([{"tag": "text", "text": f"\n📌 {s.lstrip('# ').strip()}", "style": ["bold"]}])
        elif s.startswith("### "):
            content_lines.append([{"tag": "text", "text": f"  {s.lstrip('# ').strip()}", "style": ["bold"]}])
        elif s.startswith("> "):
            content_lines.append([{"tag": "text", "text": f"💡 {s[2:].strip()}"}])
        elif s.startswith("---"):
            content_lines.append([{"tag": "text", "text": "─" * 20}])
        else:
            content_lines.append([{"tag": "text", "text": s}])
    return content_lines


def send_post(webhook_url, title, md_content, secret=""):
    """推送富文本消息到飞书。"""
    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": md_to_post_content(md_content)
                }
            }
        }
    }
    if secret:
        ts, sign = gen_sign(secret)
        if ts:
            payload["timestamp"] = ts
            payload["sign"] = sign

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    print(f"  长度: {len(md_content)} 字符")
    req = urllib.request.Request(
        webhook_url, data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print(f"  code: {result.get('code', result.get('StatusCode', -1))}")
        return result


def send_card(webhook_url, title, summary, secret=""):
    """推送飞书交互卡片。"""
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": title},
                "template": "blue"
            },
            "elements": [
                {"tag": "markdown", "content": summary[:2000]}
            ]
        }
    }
    if secret:
        ts, sign = gen_sign(secret)
        if ts:
            payload["timestamp"] = ts
            payload["sign"] = sign

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        webhook_url, data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print(f"  [卡片] code: {result.get('code', -1)}")
        return result


def push_signal(report_text, webhook_url=None, secret=None):
    """推送信号报告（供 portfolio_checker.py 调用）。"""
    url = webhook_url or get_webhook_url()
    sec = secret or get_secret()
    print("\n📤 推送到飞书...")
    title = f"📊 持仓信号检查 | {datetime.now().strftime('%Y-%m-%d')}"
    send_post(url, title, report_text, sec)
    print("  推送完成!")


def find_latest_result():
    output_dir = PROJECT_DIR / "output"
    if not output_dir.exists():
        return None
    files = sorted(output_dir.glob("portfolio_*.json"), reverse=True)
    return files[0] if files else None


def format_json_to_markdown(json_path):
    """将 JSON 检查结果格式化为飞书消息。"""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    timestamp = data.get("timestamp", "未知")
    market_detail = data.get("market_detail", "")
    results = data.get("results", {})

    lines = [
        f"时间: {timestamp}",
        f"市场环境: {market_detail}",
        "",
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
            lines.append(f"{sym} ${price:.2f} | {rl1}{rl2}{rl3} | {action}")
        elif strategy == "pullback":
            pb = info.get("pullback", {})
            detail = pb.get("detail", "")
            signal = "⚠️可小加" if pb.get("signal") else "HOLD"
            lines.append(f"{sym} ${price:.2f} | {detail} → {signal}")
        elif strategy == "hold":
            lines.append(f"{sym} ${price:.2f} | HOLD")
        elif strategy == "satellite":
            lines.append(f"{sym} ${price:.2f} | 卫星不动")

    has_signal = data.get("has_signal", False)
    lines.append(f"\n{'存在信号，需关注' if has_signal else '今天不交易'}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="InvAssistant 飞书推送")
    parser.add_argument("--webhook", help="飞书 Webhook URL")
    parser.add_argument("--test", action="store_true", help="发送测试消息")
    parser.add_argument("--card", action="store_true", help="使用交互卡片模式")
    parser.add_argument("--file", help="指定 JSON 结果文件路径")
    args = parser.parse_args()

    webhook_url = get_webhook_url(args.webhook)
    secret = get_secret()

    print(f"{'='*55}")
    print(f"  InvAssistant — 飞书推送")
    print(f"  签名: {'是' if secret else '否'} | 模式: {'卡片' if args.card else '富文本'}")
    print(f"{'='*55}")

    if args.test:
        title = "📊 InvAssistant 测试"
        content = f"连接成功! {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        if args.card:
            send_card(webhook_url, title, content, secret)
        else:
            send_post(webhook_url, title, content, secret)
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
    title = f"📊 持仓信号检查 | {datetime.now().strftime('%Y-%m-%d')}"
    content = format_json_to_markdown(json_path)

    if args.card:
        send_card(webhook_url, title, content, secret)
    else:
        send_post(webhook_url, title, content, secret)

    print(f"\n{'='*55}")
    print("  推送完成!")
    print(f"{'='*55}")


if __name__ == "__main__":
    main()
