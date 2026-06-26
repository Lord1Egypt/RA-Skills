---
name: in-skill-stripe-payments-demo
description: >
  Stripe in-skill payments demo: gate premium behavior behind a one-time checkout, verify
  via Stripe API and local receipt. Use when demonstrating or implementing paid skills,
  in-skill payment, Stripe payment gate, or verify payment before premium features. Trigger
  for: "in-skill Stripe payments", "paid skill", "skill payment demo", "Stripe checkout
  gate", "verify payment before premium".
---

# Skill payments demo (placeholder)

This repository is a **minimal template** for **gating a skill behind a one-time Stripe payment**. The “premium” behavior is intentionally a placeholder: after payment verification, your product code would run here.

## What ships in this demo

- `scripts/check_payment.py` — Stripe Checkout Session lookup by **customer email**, minimum amount check (`MIN_AMOUNT_CENTS` in code), optional Payment Link URL from the environment, and a **local receipt cache** on disk (see below).
- `requirements.txt` — pins **`stripe>=7.0.0`** (Stripe’s Python SDK). Install before importing `check_payment`.
- This `SKILL.md` — agent instructions: **always verify payment first**, then proceed to placeholder premium steps.

## Environment variables (sensitive — host / deployment only)

These are read by `scripts/check_payment.py` via `os.environ`. **Do not ask end users for `STRIPE_SECRET_KEY`.** Configure them in the environment where the agent or skill host runs (or a local `.env` for development — see `.env.example`; never commit secrets).

| Variable | Required? | Purpose |
|----------|-----------|---------|
| `STRIPE_SECRET_KEY` | **Yes** | Stripe secret API key (`sk_test_...` or `sk_live_...`). Without it, verification against Stripe fails. |
| `STRIPE_PAYMENT_LINK_URL` | No | Full URL of a [Stripe Payment Link](https://stripe.com/docs/payment-links). If unset, `get_payment_link()` returns an obvious placeholder string. |

## Dependencies and install

1. Use **Python 3** with `pip` available.
2. From this skill’s repository root, install the declared dependency:

```bash
pip install -r requirements.txt
```

That installs `stripe>=7.0.0`. Calls to Stripe’s API require **outbound network** access from the runtime.

## Local disk: receipt cache

After a successful `complete_payment_verification`, the script **writes** a small JSON file (with a checksum) to:

`~/.skill-payment-demo-receipt`

On later runs, `check_payment_status()` **reads** that file to skip re-querying Stripe when the receipt is still valid. Users and publishers should treat this path as **agent-local state** (not shared across machines). Production skills may replace this with different storage or user binding.

---

## Step 1 — Payment gate (mandatory first)

The agent **must** run the payment check before any premium behavior.

### 1a. Import and check existing receipt

```python
import sys
sys.path.insert(0, "<SKILL_DIR>/scripts")
from check_payment import (
    check_payment_status,
    get_payment_link,
    complete_payment_verification,
)

if check_payment_status():
    print("Payment verified — premium section allowed.")
else:
    print("Payment required for premium features.")
```

Replace `<SKILL_DIR>` with this skill’s directory on disk.

If `check_payment_status()` is `True`, skip to **Step 2**.

### 1b. Not paid — show Payment Link

```python
link = get_payment_link()
print("Complete the one-time payment to unlock premium features:")
print(f"  → {link}")
print()
print("After paying, reply with the email address you used at checkout.")
```

Stop and wait for the user’s email.

### 1c. Verify by email

```python
email = "<user's email>"
if complete_payment_verification(email):
    print("Payment verified.")
else:
    print("No matching completed payment for that email. Check the address and try again.")
    # Do not run premium logic
```

If verification fails, do not proceed. If `STRIPE_SECRET_KEY` is missing or misconfigured, treat it as a server-side error (do not ask the user for the secret).

---

## Step 2 — Placeholder premium behavior

After payment is verified (receipt or successful `complete_payment_verification`), respond with a short confirmation, for example:

> Premium area unlocked (demo). Replace this section in `SKILL.md` with your real skill: API calls, tools, or scripts.

There is **no** streaming or external data feed in this repo by design.

---

## Error handling

- **Not paid / verification failed**: Show the link again; do not run premium logic.
- **Stripe errors**: Say verification is temporarily unavailable; retry later.
- **CLI test**: `python scripts/check_payment.py` (requires `STRIPE_SECRET_KEY`; optional `STRIPE_PAYMENT_LINK_URL`).

## Security notes for publishers

- Never commit `STRIPE_SECRET_KEY` or live customer data; use environment variables and a `.gitignore` for local secrets.
- Adjust `MIN_AMOUNT_CENTS` in `check_payment.py` to match your Payment Link price.
- The receipt cache path and behavior are documented under **Local disk: receipt cache** above.
