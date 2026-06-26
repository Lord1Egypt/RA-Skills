# ipeaky Paid Tier 💎

> **Status: Scaffold** — This is the foundation for ipeaky's paid tier. The gating logic and billing integration are stubs ready for customization.

## Concept

ipeaky is free and open-source for core key management (store, list, test, delete). The paid tier adds premium capabilities for power users and teams:

### Free Tier (current)
- ✅ Secure key storage via macOS popup
- ✅ Store keys in OpenClaw native config
- ✅ Test keys against provider APIs
- ✅ List and delete keys
- ✅ Multi-key paste (v4)
- ✅ Key monitoring & health checks

### Paid Tier (coming)
- 🔐 **Team key sharing** — Share keys across team members with role-based access
- 🔄 **Key rotation reminders** — Automated alerts when keys are approaching expiry
- 📊 **Usage analytics** — Track which skills use which keys and how often
- 🔔 **Breach monitoring** — Get notified if a key appears in public leak databases
- 🌐 **Cross-platform support** — Linux and Windows secure input (beyond macOS osascript)
- 📦 **Key backup & sync** — Encrypted backup to cloud storage, sync across machines
- 🏢 **Org-level policies** — Enforce key naming conventions, required rotations, audit logs

## How Billing Works

ipeaky uses **Stripe** for payment processing. The flow:

1. **Setup**: Run `bash paid_tier/stripe-setup.sh` to store your Stripe API key via ipeaky itself (dogfooding!)
2. **Checkout**: `bash paid_tier/stripe-checkout.sh --price price_XXXXX --mode subscription` creates a Stripe Checkout session
3. **Verification**: After payment, the checkout session ID is stored locally and verified against Stripe's API
4. **Activation**: Paid features unlock based on active subscription status

### Pricing (planned)

| Plan | Price | Features |
|------|-------|----------|
| **Free** | $0/mo | Core key management |
| **Pro** | $9/mo | + rotation reminders, cross-platform, usage analytics |
| **Team** | $29/mo | + team sharing, org policies, breach monitoring, backup & sync |

## Setup

### 1. Store your Stripe key

```bash
bash paid_tier/stripe-setup.sh
```

This uses ipeaky's own secure storage to save your Stripe secret key. Keys never touch chat or logs.

### 2. Create a product in Stripe

Go to [Stripe Dashboard → Products](https://dashboard.stripe.com/products) and create your subscription product with a price.

### 3. Create checkout sessions

```bash
# Subscription checkout
bash paid_tier/stripe-checkout.sh --price price_1ABC123 --mode subscription

# One-time payment
bash paid_tier/stripe-checkout.sh --price price_1ABC123 --mode payment
```

### 4. Verify payment (TODO)

```bash
# Future: verify subscription status
bash paid_tier/stripe-verify.sh --session cs_XXXXX
```

## Architecture

```
paid_tier/
├── stripe-setup.sh       # Store Stripe key via ipeaky (dogfooding)
├── stripe-checkout.sh    # Create Stripe Checkout sessions
├── README-paid.md        # This file
└── (future)
    ├── stripe-verify.sh  # Verify payment / subscription status
    ├── stripe-webhook.sh # Handle Stripe webhook events
    └── gate.sh           # Feature gating logic (check subscription)
```

## Development

This scaffold is intentionally minimal. To build out the paid tier:

1. **Create your Stripe product** — Set up pricing in the Stripe Dashboard
2. **Wire up verification** — Add `stripe-verify.sh` to check subscription status
3. **Add feature gates** — Import `gate.sh` in premium scripts to check access
4. **Set up webhooks** — Handle subscription lifecycle events (created, cancelled, failed)
5. **Add a landing page** — Point users to ipeaky-site with upgrade CTAs

## Security Notes

- Stripe keys are stored via ipeaky's secure flow (macOS popup → config.patch)
- Keys never appear in chat, shell history, or process lists
- The checkout script reads keys from OpenClaw config, not environment variables
- All scripts use `set -euo pipefail` (strict mode)
- No `eval` usage anywhere
