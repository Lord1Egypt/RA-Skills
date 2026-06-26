---
name: telegram-bot-payments
description: Add paywall to OpenClaw Telegram bots. Covers Stripe external link (94% margin), Telegram Stars (65% margin, required for iOS), and TON Wallet Pay (99% margin). Includes webhook server, credits system, and AGENTS.md behavior.
license: MIT
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.2"
  tags: ["telegram", "payments", "stripe", "stars", "openclaw", "monetization"]
allowed-tools: Bash Read Edit Write Grep Glob Agent
user-invocable: true
---

# Telegram Bot Payments — Paywall Implementation

Add paid credits to any OpenClaw Telegram bot. Supports three payment methods with a hybrid approach to maximize developer margin.

## When to Use

- Adding a paywall to an OpenClaw Telegram bot
- Implementing per-image or per-use quota with paid top-ups
- Choosing the right payment method for your user base
- Setting up Stripe, Telegram Stars, or TON payments

---

## Payment Method Decision

| Method | User pays $10 → You receive | When to use |
|--------|------------------------------|-------------|
| **Stripe (external link)** | **~$9.41 (94%)** | Android, Desktop, Web users — best margin |
| **TON Wallet Pay** | **~$9.90 (99%)** | Crypto-savvy users — best margin, zero fees |
| **Telegram Stars** | **~$6.50 (65%)** | iOS users ONLY — legally required for in-app digital goods on iOS |

### Why NOT Stars-only

Stars = two fees back-to-back:
```
User pays $10
  → Apple/Google takes ~30% (mandatory IAP)
  → Telegram takes ~5%
  → You receive ~$6.50
```

For image generation at $0.03–$0.08/image, Stars makes most packages unprofitable.

### The Hybrid Rule

```
User on iOS?   → Stars (no choice — Apple policy)
User on Android/Desktop/Web? → Stripe external link (9x better margin)
```

Telegram does NOT currently ban external payment links. Risk is low-medium.
If enforced in future, fall back to Stars or TON.

---

## Architecture

```
Quota exhausted
    ↓
Agent detects (check_quota.py returns allowed=false)
    ↓
Agent sends payment options message + buttons
    ↓
    ├─ [Pay with Card ⭐] → Stripe Payment Link (external browser)
    ├─ [Pay with Stars ⭐] → Telegram Stars invoice (iOS compliance)
    └─ [Pay with TON 💎] → TON Wallet Pay link (optional)
    ↓
Payment completed → Stripe/Stars webhook fires
    ↓
payment_server.py updates /workspaces/{USER_ID}/usage.json credits
    ↓
User continues generating
```

---

## Implementation: Stripe External Link (Primary Method)

### Step 1: Create Stripe Payment Links

In Stripe Dashboard → Payment Links → Create:

```
Product: "20 Image Credits"   Price: $2.00  → copy link e.g. https://buy.stripe.com/xxx
Product: "50 Image Credits"   Price: $4.00  → copy link e.g. https://buy.stripe.com/yyy
Product: "100 Image Credits"  Price: $7.00  → copy link e.g. https://buy.stripe.com/zzz
```

**Critical:** Add a metadata field `telegram_user_id` — but Payment Links don't support dynamic metadata natively. Two options:

**Option A (Simple) — URL with client_reference_id:**
Stripe Payment Links support `?client_reference_id=USER_ID` as a query param. Append the user's Telegram ID:
```
https://buy.stripe.com/xxx?client_reference_id=697391377
```
The `client_reference_id` appears in the webhook payload.

**Option B (Proper) — Stripe Checkout Session:**
Create a dynamic session per user via API (see `create_checkout.py` below). More control, supports pre-filling email, adding metadata.

---

### Step 2: `payment_server.py` (FastAPI, runs on port 8001)

```python
"""
Unified payment webhook server.
Handles: Stripe webhooks + Telegram Stars pre_checkout_query + successful_payment
Run: uvicorn payment_server:app --host 0.0.0.0 --port 8001
"""
import json
import os
import pathlib
import httpx
from fastapi import FastAPI, Request, HTTPException
import stripe

app = FastAPI()
WORKSPACES = pathlib.Path(os.environ.get("WORKSPACES_DIR", "/workspaces"))
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")

CREDIT_PACKAGES = {
    "price_20":  {"credits": 20,  "price_id": "price_xxx"},  # replace with real Stripe price IDs
    "price_50":  {"credits": 50,  "price_id": "price_yyy"},
    "price_100": {"credits": 100, "price_id": "price_zzz"},
}


def add_credits(user_id: str, credits: int):
    """Add credits to user's usage.json."""
    usage_file = WORKSPACES / user_id / "usage.json"
    if usage_file.exists():
        usage = json.loads(usage_file.read_text())
    else:
        usage = {"daily_count": 0, "credits": 0, "tier": "free"}
    usage["credits"] = usage.get("credits", 0) + credits
    usage_file.write_text(json.dumps(usage, indent=2))
    return usage["credits"]


def notify_user(user_id: str, credits_added: int, total_credits: int):
    """Send Telegram message to user after successful payment."""
    httpx.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": user_id,
            "text": f"✅ 充值成功！\n\n+{credits_added} 张图片额度\n剩余总额度：{total_credits} 张\n\n直接告诉我你想要什么吧 👇",
        },
        timeout=10,
    )


# ── Stripe Webhook ──────────────────────────────────────────────────────────

@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")

    try:
        event = stripe.Webhook.construct_event(payload, sig, STRIPE_WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session.get("client_reference_id") or session.get("metadata", {}).get("telegram_user_id")
        credits = int(session.get("metadata", {}).get("credits", 0))

        if user_id and credits:
            total = add_credits(user_id, credits)
            notify_user(user_id, credits, total)

    return {"ok": True}


# ── Telegram Stars Webhook ───────────────────────────────────────────────────

@app.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()

    # Must answer pre_checkout_query within 10 seconds
    pq = data.get("pre_checkout_query")
    if pq:
        httpx.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/answerPreCheckoutQuery",
            json={"pre_checkout_query_id": pq["id"], "ok": True},
            timeout=8,
        )
        return {"ok": True}

    msg = data.get("message", {})
    payment = msg.get("successful_payment")
    if payment:
        # payload format: "credits_20_697391377"
        parts = payment.get("invoice_payload", "").split("_")
        if len(parts) == 3 and parts[0] == "credits":
            credits = int(parts[1])
            user_id = parts[2]
            total = add_credits(user_id, credits)
            notify_user(user_id, credits, total)

    return {"ok": True}
```

---

### Step 3: `buy_credits.py` (agent calls this to send payment options)

```python
#!/usr/bin/env python3
"""
Send payment options to user when quota is exhausted.
Usage: python3 buy_credits.py <user_id> [stars|stripe|both]
"""
import sys
import os
import httpx

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
USER_ID = sys.argv[1]
MODE = sys.argv[2] if len(sys.argv) > 2 else "both"

# Replace these with your actual Stripe Payment Links
STRIPE_LINKS = {
    "20":  "https://buy.stripe.com/xxx?client_reference_id=" + USER_ID,
    "50":  "https://buy.stripe.com/yyy?client_reference_id=" + USER_ID,
    "100": "https://buy.stripe.com/zzz?client_reference_id=" + USER_ID,
}

# Stars packages (currency XTR, 1 star ≈ $0.013 received by developer)
STARS_PACKAGES = {
    "20":  {"stars": 200, "credits": 20},   # ~$2.60 retail → ~$1.69 to you
    "50":  {"stars": 450, "credits": 50},   # ~$5.85 retail → ~$3.80 to you
    "100": {"stars": 800, "credits": 100},  # ~$10.40 retail → ~$6.76 to you
}

if MODE in ("stripe", "both"):
    # Send external link buttons
    httpx.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": USER_ID,
            "text": "今天的免费额度用完了！\n\n💳 用银行卡充值（推荐）：",
            "reply_markup": {
                "inline_keyboard": [
                    [{"text": "20张 $2.00", "url": STRIPE_LINKS["20"]},
                     {"text": "50张 $4.00", "url": STRIPE_LINKS["50"]}],
                    [{"text": "100张 $7.00 🔥", "url": STRIPE_LINKS["100"]}],
                ]
            },
        },
        timeout=10,
    )

if MODE in ("stars", "both"):
    # Send Stars invoice for the most popular package
    httpx.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendInvoice",
        json={
            "chat_id": USER_ID,
            "title": "50张图片额度",
            "description": "购买50张图片生成额度，不过期",
            "payload": f"credits_50_{USER_ID}",
            "currency": "XTR",
            "prices": [{"label": "50张图片", "amount": STARS_PACKAGES["50"]["stars"]}],
        },
        timeout=10,
    )

print("PAYMENT_OPTIONS_SENT")
```

---

### Step 4: `entrypoint.sh` additions

```bash
# Install dependencies
pip3 install fastapi uvicorn stripe httpx

# Start payment server in background
uvicorn payment_server:app --host 0.0.0.0 --port 8001 &

# Register Telegram webhook for Stars payments
python3 - << 'EOF'
import httpx, os
token = os.environ["TELEGRAM_BOT_TOKEN"]
# Replace with your server's public IP/domain
server = os.environ.get("SERVER_PUBLIC_URL", "https://your-server.com")
httpx.post(
    f"https://api.telegram.org/bot{token}/setWebhook",
    json={"url": f"{server}/webhook/telegram"}
)
print("Telegram webhook set")
EOF
```

### Step 5: `AGENTS.md` payment behavior

```markdown
## 付费引导（额度用完时）

当 check_quota.py 输出 `allowed=false` 时：
1. 如果本次请求已生成图片，先发出图片
2. 运行：exec python3 /workspaces-shared/skills/payments/buy_credits.py {PEER_ID} both
3. 不要多说，让按钮说话

严格禁止：
- 不要解释定价逻辑
- 不要提到 Stripe、Stars 是什么
- 不要说「我无法生成了」——说「今天的免费额度用完了」

文字聊天、问题回答即使额度=0也继续正常进行。只有生成图片时才触发付费引导。
```

---

## Stripe Setup Checklist

```
□ Stripe 账号创建并验证身份（需要护照/ID）
□ 创建三个 Payment Links（20/50/100张）
□ 每个 Product 的 metadata 里加 credits 字段（如 credits=20）
□ Webhook endpoint 添加：https://your-server/webhook/stripe
□ 选择监听事件：checkout.session.completed
□ 复制 Webhook Signing Secret → 填入 STRIPE_WEBHOOK_SECRET env var
□ 测试：用 Stripe test card 4242 4242 4242 4242 付款，确认 credits 更新
```

---

## Pricing Strategy

Goal: cover API cost + profit. Using Seedream ($0.03/image):

| Package | Price | Stripe到手 | 成本(Seedream) | 利润 | 利润率 |
|---------|-------|------------|----------------|------|--------|
| 20张    | $2.00 | $1.41      | $0.60          | $0.81 | 57% |
| 50张    | $4.00 | $3.41      | $1.50          | $1.91 | 56% |
| 100张   | $7.00 | $6.41      | $3.00          | $3.41 | 53% |

Using NB2 ($0.08/image) — not recommended for paid packages, only free tier:

| Package | Price | Stripe到手 | 成本(NB2) | 利润 | 利润率 |
|---------|-------|------------|-----------|------|--------|
| 20张    | $2.00 | $1.41      | $1.60     | **-$0.19** | **亏损** |
| 50张    | $4.00 | $3.41      | $4.00     | **-$0.59** | **亏损** |

**结论：付费包只用 Seedream。NB2 限制在免费试用。**

---

## Soft Paywall UX Rules

From `bot-ux-checklist.md`:

```
✅ 先出图，再提示额度用完（软 paywall）
✅ 渐进式提示：「还剩2张」→「最后1张」→「用完了，充值继续」
✅ 即使额度=0，文字对话继续正常进行
✅ 付款成功后立即发确认消息（payment_server 里已实现）
❌ 不要在生成前弹付款提示
❌ 不要重复推送付款按钮
```

---

## Known Issues / Gotchas

1. **Stripe Payment Links 无法动态注入 metadata** — 用 `client_reference_id` 传 user ID。如果需要 credits 数量，在 Stripe Dashboard 的 Product metadata 里提前设好，webhook 里从 `line_items` 读取。

2. **Telegram webhook 和 OpenClaw 不能共用同一个 port** — OpenClaw 用 8815，payment server 用 8001，分开。

3. **setWebhook 会覆盖 OpenClaw 的 Telegram 轮询** — 如果 OpenClaw 用 long-polling（默认），设了 webhook 后 OpenClaw 会收不到消息。解决：OpenClaw 配置 webhook 模式，或者 payment server 用独立 bot token（推荐创建一个独立的 @YourBotPaymentBot 专门处理支付回调）。

4. **中国用户** — Stripe 支持中国发行的 Visa/Mastercard，但不支持支付宝/微信支付（需要 Stripe China 账号）。如果主要是中国用户：考虑用 TON 或接入 Creem（支持更多支付方式）。

5. **Stars 21天 hold** — 提现要等21天，且只能提 TON。Stars 做为 iOS 合规保底，不作为主要收入。

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
