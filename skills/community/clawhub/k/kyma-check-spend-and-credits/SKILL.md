---
name: check-spend-and-credits
description: Report the Kyma API account balance, this connection's spend cap, amount spent, remaining budget and reset date, plus recent credit ledger entries, and hand back the top-up link when the balance is low. Use when the user asks about their balance, credits, budget, spend cap, what a call cost, why a request was refused for funds, or before running anything that is billed such as send_message.
---

# Check spend and credits on Kyma API

Everything here is read-only. No tool in this skill moves money or creates a key.

## When to use

- "What's my balance?" / "How many credits do I have left?"
- "How much has this connection spent?" / "When does my cap reset?"
- "What did that call cost?"
- Immediately before any billed action, so the user sees the budget before the charge.

## Steps

1. Call `get_credits` for the account balance in USD.
2. Call `get_spend` for this connection's own limits: the cap, spent so far, remaining, and the reset date. This is a per-connection budget separate from the account balance — a connection can be capped out while the account still has credits, and vice versa.
3. If the user asked what something cost, or the numbers look wrong, call `get_transactions` for the recent ledger rows and read the amounts and types back. Each row is one credit movement; usage rows are charges, top-up rows are additions.
4. If the balance or the remaining cap will not cover what the user is about to do, call `get_topup_link` and give them the link. It returns the billing page, never a checkout — the user completes payment themselves.

## Reporting

- Lead with the two numbers that matter: account balance, and remaining on this connection's cap with its reset date.
- Give amounts in USD with enough decimal places to be honest about sub-cent costs.
- When the remaining cap is the binding constraint, say so explicitly, and mention the cap is adjustable from $1 to $500 at https://kymaapi.com/integrations.
- Never present a remembered or estimated balance. If a tool call failed, say the balance is unknown.

## Before a billed action

Run this check first, state the balance and remaining cap, then ask for the go-ahead. Do not chain straight from a balance check into `send_message`.
