# Enable Stripe Payments Within Your Skill

This repository shows how to **gate a skill behind a Stripe payment** before any premium logic runs. A small Python module handles receipts and Stripe lookups. `SKILL.md` tells an agent to **check payment first**, **show a Payment Link when needed**, and **verify checkout by email** against completed Stripe Checkout Sessions.

![In-skill Stripe payment test run](test.png)

## Understanding what ships

The demo includes two parts:

1. **`scripts/check_payment.py`**  
   The module reads a local receipt, returns a Payment Link from the environment, lists completed Checkout Sessions in Stripe, matches the checkout email, compares `amount_total` to `MIN_AMOUNT_CENTS`, and writes a receipt so later sessions skip the paywall.

2. **`SKILL.md`**  
   The file walks the agent through that flow, then points to a placeholder where your real product code would go.

The repo deliberately ships no live product feature. After you verify payment, you add your own APIs, tools, or scripts in that placeholder.

## Walking through payment

1. The agent calls `check_payment_status()`. A valid receipt opens the gate immediately.
2. If there is no receipt, the agent shows `get_payment_link()` so the user can pay in the browser.
3. After payment, the user sends the checkout email. The agent calls `complete_payment_verification(email)`.
4. Stripe returns a completed session for that email with `amount_total` at or above `MIN_AMOUNT_CENTS`. The script saves a receipt at `~/.skill-payment-demo-receipt` for this demo.

## Configuring Stripe

Set **`STRIPE_SECRET_KEY`** wherever the skill runs. It drives server-side Stripe API calls only. Do not commit it.

Set **`STRIPE_PAYMENT_LINK_URL`** to a Stripe Payment Link you created in the Dashboard. If it is unset, `get_payment_link()` returns a short placeholder string so missing setup is obvious.

Install dependencies:

```bash
pip install -r requirements.txt
```

Test the script interactively:

```bash
python scripts/check_payment.py
```

## Hardening before launch

Edit **`MIN_AMOUNT_CENTS`** in `check_payment.py` so it matches your price.

A file in the home directory works for a demo. Production skills may store entitlement elsewhere or tie it to a stable user id.

## Checking eval coverage

`evals/evals.json` holds prompts that expect the agent to run the payment gate before claiming premium access.
