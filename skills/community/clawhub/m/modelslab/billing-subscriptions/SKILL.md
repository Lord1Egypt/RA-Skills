---
name: modelslab-billing-subscriptions
description: Manage ModelsLab billing, wallet balance, payment methods, subscriptions, invoices, and coupons programmatically via the Agent Control Plane API.
---

# ModelsLab Billing & Subscriptions

Manage billing, wallet funding, payment methods, subscriptions, and coupons via the Agent Control Plane API.

## When to Use This Skill

- Check wallet balance and fund it
- Set up auto-recharge for wallets
- Manage payment methods (add, set default, remove)
- Create payment links for human-assisted checkout
- Confirm Stripe Checkout sessions (wallet funding or subscriptions)
- View and download invoices
- Create, upgrade, pause, or resume subscriptions
- Validate and redeem coupons
- Update billing information (address, tax ID)

## Authentication

All billing endpoints require a bearer token.

```
Base URL: https://modelslab.com/api/agents/v1
Authorization: Bearer <agent_access_token>
```

Get a token via the `modelslab-account-management` skill or `POST /auth/login`.

## Helper

```python
import requests

BASE = "https://modelslab.com/api/agents/v1"

def headers(token):
    return {"Authorization": f"Bearer {token}"}
```

## Billing Overview

```python
def get_billing_overview(token):
    """Get billing overview — balance, active subscriptions, recent charges."""
    resp = requests.get(f"{BASE}/billing/overview", headers=headers(token))
    return resp.json()["data"]

# Usage
overview = get_billing_overview(token)
print(f"Wallet balance: ${overview.get('wallet_balance', 0)}")
```

## Three Payment Paths

ModelsLab supports three ways for agents to handle payments:

| Path | Best For | Flow |
|------|----------|------|
| **Headless** | Autonomous agents with card data | `GET /billing/stripe-config` -> tokenize via Stripe API -> pass `payment_method_id` to fund/subscribe |
| **Setup Intent** | Save a card for reuse without immediate charge | `POST /billing/setup-intent` -> confirm with Stripe -> reuse `payment_method_id` for future fund/subscribe |
| **Human-Assisted** | Agents that cannot handle card data directly | `POST /billing/payment-link` -> forward URL to human -> human pays on Stripe Checkout -> poll `confirm-checkout` |

## Stripe Config

Fetch the Stripe publishable key dynamically instead of hardcoding it. Useful for agents that need to tokenize cards client-side.

```python
def get_stripe_config(token):
    """Get the Stripe publishable key for client-side card tokenization.

    Returns:
        publishable_key: Stripe publishable key (pk_...)
        instructions: Usage guidance from the API
    """
    resp = requests.get(f"{BASE}/billing/stripe-config", headers=headers(token))
    return resp.json()["data"]

# Usage
config = get_stripe_config(token)
stripe_pk = config["publishable_key"]  # e.g., "pk_live_..."
```

> **Tip:** The publishable key is safe to embed in agent code — it can only create tokens, never charge directly. You can either fetch it dynamically via this endpoint or use the hardcoded key below.

## Headless Card Tokenization (Recommended)

Agents create PaymentMethods directly via the Stripe API using the ModelsLab publishable key. Card data goes to Stripe only — ModelsLab never sees raw card numbers.

Fetch the Stripe publishable key dynamically via `GET /billing/stripe-config`. This ensures your agent always uses the current key without redeploying when it rotates.

```python
import requests

# Fetch publishable key from API
config_resp = requests.get(
    f"{BASE}/billing/stripe-config",
    headers={"Authorization": f"Bearer {TOKEN}"}
)
STRIPE_PK = config_resp.json()["publishable_key"]

def create_payment_method(card_number, exp_month, exp_year, cvc):
    """Create a Stripe PaymentMethod directly — card data never touches ModelsLab.

    Args:
        card_number: Card number (e.g., "4242424242424242")
        exp_month: Expiry month (e.g., 12)
        exp_year: Expiry year (e.g., 2027)
        cvc: CVC code (e.g., "123")

    Returns:
        Stripe PaymentMethod ID (pm_...) for use with ModelsLab endpoints.
    """
    resp = requests.post(
        "https://api.stripe.com/v1/payment_methods",
        auth=(STRIPE_PK, ""),
        data={
            "type": "card",
            "card[number]": card_number,
            "card[exp_month]": exp_month,
            "card[exp_year]": exp_year,
            "card[cvc]": cvc,
        }
    )
    return resp.json()["id"]  # e.g., "pm_1Xyz..."

# Usage — complete headless payment flow:
pm_id = create_payment_method("4242424242424242", 12, 2027, "123")
fund_wallet(token, 25, payment_method_id=pm_id)  # or create_subscription(...)
```

## Setup Intent Flow

Use a SetupIntent to save a card for future use without an immediate charge. The confirmed PaymentMethod can then be reused for wallet funding or subscriptions.

```python
def create_setup_intent(token):
    """Create a Stripe SetupIntent to save a card for future use.

    Returns:
        client_secret: Use with Stripe.js or Stripe API to confirm the SetupIntent
        setup_intent_id: The SetupIntent ID (seti_...)
    """
    resp = requests.post(f"{BASE}/billing/setup-intent", headers=headers(token))
    return resp.json()["data"]

# Usage — save a card for reuse
setup = create_setup_intent(token)
client_secret = setup["client_secret"]

# Confirm the SetupIntent via Stripe API with card details
stripe_pk = get_stripe_config(token)["publishable_key"]
confirm_resp = requests.post(
    f"https://api.stripe.com/v1/setup_intents/{setup['setup_intent_id']}/confirm",
    auth=(stripe_pk, ""),
    data={
        "payment_method_data[type]": "card",
        "payment_method_data[card][number]": "4242424242424242",
        "payment_method_data[card][exp_month]": 12,
        "payment_method_data[card][exp_year]": 2027,
        "payment_method_data[card][cvc]": "123",
    }
)
pm_id = confirm_resp.json()["payment_method"]  # e.g., "pm_..."

# Now attach and reuse the payment method
add_payment_method(token, pm_id, make_default=True)
fund_wallet(token, 50, payment_method_id=pm_id)
```

## Human-Assisted Payment (Payment Links)

For agents that cannot handle card data directly (e.g., chatbots, voice assistants), create a Stripe-hosted payment URL and forward it to a human user. ModelsLab controls the `success_url` — agents cannot override it.

```python
def create_payment_link(token, purpose, amount=None, plan_id=None):
    """Create a Stripe-hosted payment URL for a human to complete.

    Args:
        purpose: "fund" for wallet funding, "subscribe" for subscription
        amount: Required if purpose is "fund" — amount in USD (min $10)
        plan_id: Required if purpose is "subscribe" — plan ID from list_plans()

    Returns:
        payment_url: Stripe Checkout URL to forward to the human
        session_id: Checkout session ID (cs_...) for confirming later
        purpose: Echoed back
        amount: Echoed back (for fund)
        expires_at: When the payment link expires
        instructions: Guidance for the agent

    Note:
        success_url is NOT accepted — ModelsLab controls redirects.
        After payment, the human sees ModelsLab's success page with the session_id
        to copy back to the agent.
    """
    payload = {"purpose": purpose}
    if amount is not None:
        payload["amount"] = amount
    if plan_id is not None:
        payload["plan_id"] = plan_id

    resp = requests.post(
        f"{BASE}/billing/payment-link",
        headers=headers(token),
        json=payload
    )
    return resp.json()["data"]

# Usage — wallet funding via human
link = create_payment_link(token, purpose="fund", amount=50)
print(f"Please complete payment at: {link['payment_url']}")
print(f"Session ID: {link['session_id']} (expires {link['expires_at']})")

# Usage — subscription via human
plans = list_plans(token)
chosen_plan = plans["subscription_plans"][0]
link = create_payment_link(token, purpose="subscribe", plan_id=chosen_plan["id"])
print(f"Please subscribe at: {link['payment_url']}")
```

### Confirming Checkout Sessions

After the human completes payment on the Stripe Checkout page, confirm the session to finalize the transaction. Use the `session_id` from `create_payment_link()` or from the human after they see the success page.

```python
def confirm_wallet_checkout(token, session_id):
    """Confirm a Stripe Checkout session for wallet funding.

    Call this after the human completes payment on the Stripe Checkout page.

    Args:
        session_id: The Checkout session ID (cs_...) from create_payment_link()
    """
    resp = requests.post(
        f"{BASE}/wallet/confirm-checkout",
        headers=headers(token),
        json={"session_id": session_id}
    )
    return resp.json()["data"]

def confirm_subscription_checkout(token, session_id):
    """Confirm a Stripe Checkout session for subscription.

    Call this after the human completes payment on the Stripe Checkout page.

    Args:
        session_id: The Checkout session ID (cs_...) from create_payment_link()
    """
    resp = requests.post(
        f"{BASE}/subscriptions/confirm-checkout",
        headers=headers(token),
        json={"session_id": session_id}
    )
    return resp.json()["data"]

# Usage — complete human-assisted wallet funding flow
link = create_payment_link(token, purpose="fund", amount=50)
print(f"Pay here: {link['payment_url']}")
# ... human pays ...
session_id = link["session_id"]  # or human copies it from success page
result = confirm_wallet_checkout(token, session_id)
print(f"Wallet funded! New balance: ${result.get('balance')}")

# Usage — complete human-assisted subscription flow
link = create_payment_link(token, purpose="subscribe", plan_id=42)
print(f"Subscribe here: {link['payment_url']}")
# ... human pays ...
result = confirm_subscription_checkout(token, link["session_id"])
print(f"Subscription active! Status: {result.get('status')}")
```

## Payment Methods

### List Payment Methods

```python
def list_payment_methods(token):
    """List all saved payment methods."""
    resp = requests.get(f"{BASE}/billing/payment-methods", headers=headers(token))
    return resp.json()["data"]
```

### Add Payment Method

```python
def add_payment_method(token, payment_method_id, make_default=True):
    """Add a Stripe payment method.

    Args:
        payment_method_id: Stripe PaymentMethod ID (pm_...)
        make_default: Set as default payment method
    """
    resp = requests.post(
        f"{BASE}/billing/payment-methods",
        headers=headers(token),
        json={
            "payment_method_id": payment_method_id,
            "make_default": make_default
        }
    )
    return resp.json()["data"]
```

### Set Default & Remove

```python
def set_default_payment_method(token, payment_method_id):
    """Set a payment method as the default."""
    requests.put(
        f"{BASE}/billing/payment-methods/{payment_method_id}/default",
        headers=headers(token)
    )

def remove_payment_method(token, payment_method_id):
    """Remove a payment method."""
    requests.delete(
        f"{BASE}/billing/payment-methods/{payment_method_id}",
        headers=headers(token)
    )
```

## Billing Info

```python
def get_billing_info(token):
    """Get billing name, address, and tax ID."""
    resp = requests.get(f"{BASE}/billing/info", headers=headers(token))
    return resp.json()["data"]

def update_billing_info(token, **kwargs):
    """Update billing information.

    Kwargs: name, email, tax_id, tax_id_type,
            address_line1, address_line2, address_city,
            address_state, address_postal_code, address_country
    """
    resp = requests.put(
        f"{BASE}/billing/info",
        headers=headers(token),
        json=kwargs
    )
    return resp.json()["data"]

# Usage
update_billing_info(
    token,
    name="Acme Corp",
    email="billing@acme.com",
    tax_id="EU123456789",
    tax_id_type="eu_vat",
    address_line1="123 AI Street",
    address_city="San Francisco",
    address_state="CA",
    address_postal_code="94105",
    address_country="US"
)
```

## Invoices

```python
def list_invoices(token):
    """List all invoices."""
    resp = requests.get(f"{BASE}/billing/invoices", headers=headers(token))
    return resp.json()["data"]

def get_invoice(token, invoice_id):
    """Get invoice details."""
    resp = requests.get(
        f"{BASE}/billing/invoices/{invoice_id}",
        headers=headers(token)
    )
    return resp.json()["data"]

def get_invoice_pdf(token, invoice_id):
    """Get invoice PDF download URL."""
    resp = requests.get(
        f"{BASE}/billing/invoices/{invoice_id}/pdf",
        headers=headers(token)
    )
    return resp.json()["data"]
```

## Wallet

### Wallet Balance

```python
def get_wallet_balance(token):
    """Quick wallet balance check."""
    resp = requests.get(f"{BASE}/wallet/balance", headers=headers(token))
    return resp.json()["data"]

# Usage
balance = get_wallet_balance(token)
print(f"Balance: ${balance['balance']} {balance['currency']}")
```

### Wallet Transactions

```python
def get_wallet_transactions(token, type=None, limit=50, offset=0):
    """Get wallet transaction ledger (deposits, charges, refunds).

    Args:
        type: Filter by "credit" or "debit" (optional)
        limit: Max items 1-200 (default 50)
        offset: Pagination offset (default 0)
    """
    params = {"limit": limit, "offset": offset}
    if type: params["type"] = type

    resp = requests.get(
        f"{BASE}/wallet/transactions",
        headers=headers(token),
        params=params
    )
    return resp.json()["data"]

# Usage
txns = get_wallet_transactions(token, type="debit", limit=20)
for txn in txns["items"]:
    print(f"{txn['created_at']}: {txn['type']} ${txn['amount']} — {txn['usecase']}")
print(f"Wallet balance: ${txns['wallet']['balance']}")
```

### Fund Wallet

```python
def fund_wallet(token, amount, payment_method_id=None, idempotency_key=None):
    """Add funds to wallet.

    Args:
        amount: Amount in USD (min $10)
        payment_method_id: Stripe PM ID from create_payment_method() (recommended)
        idempotency_key: Prevent duplicate charges on retries (optional)
    """
    payload = {"amount": amount}
    if payment_method_id:
        payload["payment_method_id"] = payment_method_id

    h = headers(token)
    if idempotency_key:
        h["Idempotency-Key"] = idempotency_key

    resp = requests.post(f"{BASE}/wallet/fund", headers=h, json=payload)
    return resp.json()["data"]

# Usage — headless payment flow
pm_id = create_payment_method("4242424242424242", 12, 2027, "123")
fund_wallet(token, 50, payment_method_id=pm_id, idempotency_key="fund-50-20260220")
```

### Check Payment Status

```python
def get_payment_status(token, payment_intent_id):
    """Check the status of a Stripe PaymentIntent."""
    resp = requests.get(
        f"{BASE}/payments/{payment_intent_id}/status",
        headers=headers(token)
    )
    return resp.json()["data"]

# Usage
status = get_payment_status(token, "pi_xxx")
print(f"Payment status: {status['status']}")
```

### Auto-Recharge

```python
def enable_auto_funding(token, auto_charge_amount, charge_threshold):
    """Enable automatic wallet recharge.

    Args:
        auto_charge_amount: Amount to charge (min $5)
        charge_threshold: Balance threshold to trigger charge (min $1)
    """
    resp = requests.put(
        f"{BASE}/wallet/auto-funding",
        headers=headers(token),
        json={
            "auto_charge_amount": auto_charge_amount,
            "charge_threshold": charge_threshold
        }
    )
    return resp.json()["data"]

def disable_auto_funding(token):
    """Disable automatic wallet recharge."""
    requests.delete(f"{BASE}/wallet/auto-funding", headers=headers(token))

# Usage — auto-charge $25 when balance drops below $5
enable_auto_funding(token, auto_charge_amount=25, charge_threshold=5)
```

### Withdraw

```python
def withdraw(token, amount):
    """Withdraw from wallet balance."""
    resp = requests.post(
        f"{BASE}/wallet/withdraw",
        headers=headers(token),
        json={"amount": amount}
    )
    return resp.json()["data"]
```

### Coupons

```python
def validate_coupon(token, coupon_code, purchase_amount=None):
    """Validate a coupon code before redeeming (GET request)."""
    params = {"coupon_code": coupon_code}
    if purchase_amount:
        params["purchase_amount"] = purchase_amount

    resp = requests.get(
        f"{BASE}/wallet/coupons/validate",
        headers=headers(token),
        params=params
    )
    return resp.json()["data"]

def redeem_coupon(token, coupon_code, payment_method_id=None, purchase_amount=None):
    """Redeem a coupon code."""
    payload = {"coupon_code": coupon_code}
    if payment_method_id:
        payload["payment_method_id"] = payment_method_id
    if purchase_amount:
        payload["purchase_amount"] = purchase_amount

    resp = requests.post(
        f"{BASE}/wallet/coupons/redeem",
        headers=headers(token),
        json=payload
    )
    return resp.json()["data"]

# Usage
info = validate_coupon(token, "WELCOME50")
if not info.get("error"):
    redeem_coupon(token, "WELCOME50")
```

## Subscriptions

### Discover Available Plans

Before creating a subscription, discover available plans and pay-as-you-go options:

```python
def list_plans(token):
    """List all available subscription plans and pay-as-you-go options.

    Returns:
        subscription_plans: Array of plans with id, name, price, features
        pay_as_you_go: Info about wallet-based billing (min $10 topup, auto-payments)
    """
    resp = requests.get(f"{BASE}/subscriptions/plans", headers=headers(token))
    return resp.json()["data"]

# Usage
plans_data = list_plans(token)

# Show subscription plans
for plan in plans_data["subscription_plans"]:
    print(f"{plan['name']} - ${plan['price']}/{plan['period']} (ID: {plan['id']})")
    print(f"  Features: {', '.join(plan['features'])}")

# Show pay-as-you-go option
payg = plans_data["pay_as_you_go"]
if payg["available"]:
    print(f"\nPay-as-you-go: min ${payg['minimum_topup_usd']} topup")
    print(f"Auto-payments: {payg['auto_payments']['supported']}")
```

### List Subscriptions

```python
def list_subscriptions(token):
    """List all active subscriptions."""
    resp = requests.get(f"{BASE}/subscriptions", headers=headers(token))
    return resp.json()["data"]
```

### Create Subscription

```python
def create_subscription(token, plan_id, success_url=None):
    """Start a new subscription. Returns a Stripe checkout URL.

    Use list_plans() first to discover valid plan IDs.

    Args:
        plan_id: The plan ID from list_plans() response
        success_url: Redirect after successful checkout
    """
    payload = {"plan_id": plan_id}
    if success_url: payload["success_url"] = success_url

    resp = requests.post(
        f"{BASE}/subscriptions",
        headers=headers(token),
        json=payload
    )
    return resp.json()["data"]

# Usage — discover plans, then subscribe
plans = list_plans(token)
chosen_plan = plans["subscription_plans"][0]  # Pick a plan
result = create_subscription(token, chosen_plan["id"])
print(f"Checkout URL: {result['checkout_url']}")
```

### Create Subscription (Headless — Recommended)

Subscribe headlessly with a `payment_method_id` from the Stripe API. No Checkout redirect needed.

```python
def create_subscription_headless(token, plan_id, payment_method_id, idempotency_key=None):
    """Create a subscription headlessly with a Stripe PaymentMethod.

    No browser redirect — fully headless.
    Use list_plans() first to discover valid plan IDs.
    Use create_payment_method() to get a pm_id from Stripe.

    Args:
        plan_id: The plan ID from list_plans() response
        payment_method_id: Stripe PM ID from create_payment_method()
        idempotency_key: Prevent duplicate subscriptions on retries (optional)
    """
    h = headers(token)
    if idempotency_key:
        h["Idempotency-Key"] = idempotency_key

    resp = requests.post(
        f"{BASE}/subscriptions",
        headers=h,
        json={
            "plan_id": plan_id,
            "payment_method_id": payment_method_id
        }
    )
    return resp.json()["data"]

# Usage — full headless flow
pm_id = create_payment_method("4242424242424242", 12, 2027, "123")
plans = list_plans(token)
chosen_plan = plans["subscription_plans"][0]
result = create_subscription_headless(token, chosen_plan["id"], pm_id)
print(f"Status: {result['status']}")
```

### Check Subscription Status

```python
def get_subscription_status(token, subscription_id):
    """Check the current status of a subscription."""
    resp = requests.get(
        f"{BASE}/subscriptions/{subscription_id}/status",
        headers=headers(token)
    )
    return resp.json()["data"]
```

### Update (Upgrade/Downgrade)

```python
def update_subscription(token, subscription_id, new_plan_id):
    """Change a subscription to a different plan."""
    resp = requests.put(
        f"{BASE}/subscriptions/{subscription_id}",
        headers=headers(token),
        json={"new_plan_id": new_plan_id}
    )
    return resp.json()["data"]
```

### Pause & Resume

```python
def pause_subscription(token, subscription_id):
    """Pause a subscription."""
    resp = requests.post(
        f"{BASE}/subscriptions/{subscription_id}/pause",
        headers=headers(token)
    )
    return resp.json()["data"]

def resume_subscription(token, subscription_id):
    """Resume a paused subscription."""
    resp = requests.post(
        f"{BASE}/subscriptions/{subscription_id}/resume",
        headers=headers(token)
    )
    return resp.json()["data"]
```

### Other Subscription Actions

```python
def reset_subscription_cycle(token, subscription_id):
    """Reset the current billing cycle."""
    requests.post(
        f"{BASE}/subscriptions/{subscription_id}/reset-cycle",
        headers=headers(token)
    )

def charge_subscription_amount(token, amount):
    """Charge a custom amount ($5-$10,000)."""
    resp = requests.post(
        f"{BASE}/subscriptions/charge-amount",
        headers=headers(token),
        json={"amount": amount}
    )
    return resp.json()["data"]

def fix_payment(token, subscription_id):
    """Fix a failed subscription payment."""
    requests.post(
        f"{BASE}/subscriptions/{subscription_id}/fix-payment",
        headers=headers(token)
    )
```

## Common Workflow: Ensure Funded Account

```python
def ensure_account_funded(token, min_balance=10, top_up_amount=50):
    """Check wallet balance and fund if low."""
    overview = get_billing_overview(token)
    balance = overview.get("wallet_balance", 0)

    if balance < min_balance:
        print(f"Balance ${balance} below ${min_balance}, funding ${top_up_amount}...")
        fund_wallet(token, top_up_amount)
        print("Wallet funded!")
    else:
        print(f"Balance OK: ${balance}")

# Usage
ensure_account_funded(token, min_balance=5, top_up_amount=25)
```

## Common Workflow: Human-Assisted Funding with Polling

```python
import time

def fund_via_human(token, amount, poll_interval=5, max_wait=300):
    """Create a payment link and poll until the human completes it.

    Args:
        amount: Amount in USD
        poll_interval: Seconds between balance checks
        max_wait: Maximum seconds to wait before giving up
    """
    # Get initial balance
    initial = get_wallet_balance(token)["balance"]

    # Create payment link
    link = create_payment_link(token, purpose="fund", amount=amount)
    print(f"Please fund your wallet at: {link['payment_url']}")
    print(f"Waiting for payment (expires {link['expires_at']})...")

    # Poll for confirmation
    elapsed = 0
    while elapsed < max_wait:
        time.sleep(poll_interval)
        elapsed += poll_interval
        try:
            result = confirm_wallet_checkout(token, link["session_id"])
            print(f"Payment confirmed! New balance: ${result.get('balance')}")
            return result
        except Exception:
            # Session not yet completed, keep polling
            pass

    print("Payment not completed within timeout.")
    return None

# Usage
fund_via_human(token, amount=50, max_wait=600)
```

## MCP Server Access

These same capabilities are available via the Agent Control Plane MCP server:
- **URL**: `https://modelslab.com/mcp/agents`
- **Tools**: `agent-billing`, `agent-wallet`, `agent-subscriptions` (use `list-plans` action to discover plans)

See: https://docs.modelslab.com/mcp-web-api/agent-control-plane

## API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/billing/overview` | Billing overview |
| GET | `/billing/stripe-config` | Get Stripe publishable key |
| POST | `/billing/setup-intent` | Create SetupIntent for card saving |
| POST | `/billing/payment-link` | Create Stripe Checkout payment URL |
| GET | `/billing/payment-methods` | List payment methods |
| POST | `/billing/payment-methods` | Add payment method |
| PUT | `/billing/payment-methods/{id}/default` | Set default |
| DELETE | `/billing/payment-methods/{id}` | Remove payment method |
| GET | `/billing/info` | Get billing info |
| PUT | `/billing/info` | Update billing info |
| GET | `/billing/invoices` | List invoices |
| GET | `/billing/invoices/{id}` | Invoice details |
| GET | `/billing/invoices/{id}/pdf` | Invoice PDF URL |
| GET | `/wallet/balance` | Quick wallet balance check |
| GET | `/wallet/transactions` | Wallet transaction ledger |
| POST | `/wallet/fund` | Fund wallet (with payment_method_id) |
| POST | `/wallet/confirm-checkout` | Confirm Checkout wallet funding |
| PUT | `/wallet/auto-funding` | Enable auto-recharge |
| DELETE | `/wallet/auto-funding` | Disable auto-recharge |
| POST | `/wallet/withdraw` | Withdraw balance |
| GET | `/wallet/coupons/validate` | Validate coupon |
| POST | `/wallet/coupons/redeem` | Redeem coupon |
| GET | `/payments/{id}/status` | Check payment intent status |
| GET | `/subscriptions/plans` | List available plans + pay-as-you-go |
| GET | `/subscriptions` | List subscriptions (addon, enterprise, normal) |
| POST | `/subscriptions` | Create subscription (headless with pm_id, or Checkout) |
| POST | `/subscriptions/confirm-checkout` | Confirm Checkout subscription |
| GET | `/subscriptions/{id}/status` | Check subscription status |
| PUT | `/subscriptions/{id}` | Update subscription |
| POST | `/subscriptions/{id}/pause` | Pause |
| POST | `/subscriptions/{id}/resume` | Resume |
| POST | `/subscriptions/{id}/reset-cycle` | Reset cycle |
| POST | `/subscriptions/charge-amount` | Charge amount |
| POST | `/subscriptions/{id}/fix-payment` | Fix payment |

## Best Practices

### 1. Choose the Right Payment Path
```python
# Headless — agent has card data, fully autonomous
pm_id = create_payment_method("4242424242424242", 12, 2027, "123")
fund_wallet(token, 50, payment_method_id=pm_id)

# Setup Intent — save card first, charge later
setup = create_setup_intent(token)
# ... confirm with Stripe API ...
add_payment_method(token, pm_id, make_default=True)

# Human-Assisted — agent cannot handle cards
link = create_payment_link(token, purpose="fund", amount=50)
# Forward link['payment_url'] to human, then confirm_wallet_checkout()
```

### 2. Use Idempotency Keys for Billing
```python
# Prevent duplicate charges on retries
fund_wallet(token, 50, payment_method_id=pm_id, idempotency_key="fund-50-unique-key")
```

### 3. Set Up Auto-Recharge
```python
# Avoid running out of credits during generation
enable_auto_funding(token, auto_charge_amount=25, charge_threshold=5)
```

### 4. Check Balance Before Large Jobs
```python
balance = get_wallet_balance(token)
if balance["balance"] < estimated_cost:
    fund_wallet(token, estimated_cost * 1.2)  # 20% buffer
```

### 5. Validate Coupons Before Redeeming
```python
info = validate_coupon(token, code)
# Check discount amount, expiry, etc. before committing
```

### 6. Handle Card Failures Gracefully
```python
result = fund_wallet(token, 50, payment_method_id=pm_id)
# Check for errors
if result.get("error"):
    if result["error"]["code"] == "payment_declined":
        print(f"Card declined: {result['error']['details']['decline_code']}")
    # Try a different card or ask user
```

## Resources

- **API Documentation**: https://docs.modelslab.com/agents-api/billing-and-wallet
- **MCP Server**: https://docs.modelslab.com/mcp-web-api/agent-control-plane
- **Pricing**: https://modelslab.com/pricing
- **Dashboard**: https://modelslab.com/dashboard

## Related Skills

- `modelslab-account-management` - Account setup and API keys
- `modelslab-model-discovery` - Check usage and find models
- `modelslab-webhooks` - Per-request webhook URLs for async results
