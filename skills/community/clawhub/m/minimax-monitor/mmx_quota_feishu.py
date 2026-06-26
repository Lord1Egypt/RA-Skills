#!/usr/bin/env python3
"""
查询 MiniMax 套餐配额并推送飞书（可选）
用法: python3 mmx_quota_feishu.py [api_key]

飞书推送需要配置环境变量（见 .env.example）：
  MINIMAX_API_KEY / FEISHU_APP_ID / FEISHU_APP_SECRET / FEISHU_CHAT_ID
若未配置飞书相关变量，脚本会直接在终端输出配额。
"""
import os
import sys
import json
import time
import requests

# ── MiniMax API ──────────────────────────────────────────────────────────
API_KEY = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("MINIMAX_API_KEY", "")

def get_quota(api_key):
    """通过 MiniMax 官网接口获取配额，跟 mmx-monitor-server.js 逻辑一致"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    # 跟前端一样，先试 www.minimaxi.com 的 token_plan 接口
    urls = [
        "https://www.minimaxi.com/v1/token_plan/remains",
        "https://api.minimaxi.com/v1/token_plan/remains",
    ]
    for url in urls:
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.ok and r.text:
                try:
                    return r.json()
                except Exception:
                    return r.text
        except Exception:
            continue
    return None

# ── 飞书发送 ─────────────────────────────────────────────────────────────
FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")
FEISHU_CHAT_ID = os.environ.get("FEISHU_CHAT_ID", "")

def get_token():
    res = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET},
        timeout=10,
    ).json()
    return res.get("tenant_access_token")

def send_card(token, chat_id, content_blocks):
    """发送飞书富文本卡片"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "receive_id": chat_id,
        "msg_type": "interactive",
        "content": json.dumps({"config": {"wide_screen_mode": True}, "elements": content_blocks}),
    }
    params = {"receive_id_type": "chat_id"}
    resp = requests.post(url, headers=headers, json=payload, params=params)
    return resp.ok

def format_quota(resp):
    blocks = []
    if not resp or resp.get("ok") != True or not resp.get("data"):
        return [{"tag": "markdown", "content": "❌ 获取配额失败，请检查 API Key"}]

    data = resp["data"]
    models = data.get("models", [])
    total_used = data.get("totalUsed", 0)
    total_limit = data.get("totalLimit", 0)
    reset_sec = data.get("resetSeconds", 0)

    # v1.2.0: 官方只返"剩余百分比"，server 把 used 推导成已用%，total 恒 100。
    # 文案适配：直接展示"已用 X%" / "剩余 Y%"，不再打印"0/100"这种基数。
    pct_used = round(total_used / total_limit * 100) if total_limit else 0
    pct_remain = 100 - pct_used
    blocks.append({"tag": "markdown", "content": f"**📊 MiniMax 套餐配额**  更新: {time.strftime('%H:%M:%S')}"})
    blocks.append({"tag": "markdown", "content": f"**5小时配额** 已用 `{pct_used}%`  剩余 `{pct_remain}%`"})
    if reset_sec:
        h, m = reset_sec // 3600, (reset_sec % 3600) // 60
        blocks.append({"tag": "markdown", "content": f"⏱️ 重置倒计时: **{h}小时{m}分钟**"})

    blocks.append({"tag": "hr"})
    blocks.append({"tag": "markdown", "content": "**模型明细**"})

    for m in models:
        name = m.get("name", "-")
        used = m.get("used", 0)         # 已用百分比
        window = m.get("window", "-")
        remain = 100 - used
        color = "🔴" if used >= 95 else "🟡" if used >= 75 else "🟢"
        display_window = "5小时" if window == "4小时" else window
        blocks.append({"tag": "markdown", "content": f"{color} **{name}** ({display_window})\n　已用 `{used}%`  剩余 `{remain}%`"})

    has_weekly = any(not m.get("weekly_unlimited", False) for m in models)
    if has_weekly:
        blocks.append({"tag": "hr"})
        blocks.append({"tag": "markdown", "content": "**本周配额**"})
        for m in models:
            if m.get("weekly_unlimited", False):
                blocks.append({"tag": "markdown", "content": f"　{m['name']}: 无周限"})
            else:
                w_used = m.get("weekly_used", 0)
                w_remain = 100 - w_used
                blocks.append({"tag": "markdown", "content": f"　{m['name']}: 已用 `{w_used}%`  剩余 `{w_remain}%`"})
    else:
        blocks.append({"tag": "hr"})
        blocks.append({"tag": "markdown", "content": "**本周配额**: 无周限"})

    return blocks

def main():
    if not API_KEY:
        print("[Error] 需要 API Key，请传入或设置 MINIMAX_API_KEY")
        sys.exit(1)

    resp = get_quota(API_KEY)
    blocks = format_quota(resp)

    feishu_configured = FEISHU_APP_ID and FEISHU_APP_SECRET and FEISHU_CHAT_ID
    if not feishu_configured:
        # 降级：终端输出
        print("\n📊 MiniMax 套餐配额（未配置飞书，直接输出）")
        print("=" * 40)
        for b in blocks:
            if b.get('tag') == 'markdown':
                print(b['content'])
        return

    token = get_token()
    if not token:
        print("[Error] 飞书 token 获取失败")
        sys.exit(1)

    ok = send_card(token, FEISHU_CHAT_ID, blocks)
    print("[OK] 配额已推送到飞书" if ok else "[Error] 发送失败")

if __name__ == "__main__":
    main()