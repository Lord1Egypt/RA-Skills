---
name: looloo-trading
description: Use this skill when the user wants a LooLoo trade quote or a website confirmation link for a buy or sell.
---

# LooLoo Trading

Phase 1 trading is quote-first and wallet-confirmed.

## Use this skill for

- quoting a buy or sell on the LooLoo internal market
- creating a confirmation link that sends the user back to `looloo.lol`

## Workflow

1. Call `quote_trade` with `tokenAddress`, `side`, and either `amountETH` or `amountToken`.
2. Show the quote summary and confirm the side and size with the user.
3. Call `create_trade_intent` only after the user explicitly wants to continue.
4. Return the `confirmUrl` and explain that the final wallet signature happens on the LooLoo website.

## Notes

- Phase 1 does not support unattended execution.
- The plugin does not hold keys or sign transactions.
- If the API rejects an intent, surface the policy error directly because it usually comes from the user's risk settings.
