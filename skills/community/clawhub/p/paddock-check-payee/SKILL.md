---
name: paddock-check-payee
description: Before an AI agent pays an x402 endpoint, check that the payee wallet belongs to that seller using Paddock's free check_payee. Stops payments to a wallet recorded for a different seller.
---

# Check the payee before you pay

Agent payments have no chargeback. Before you sign any x402 payment, check the payee with Paddock.

## When to use

Every time you are about to pay an x402 endpoint you have not paid before, or any time the payment terms changed since you last paid it.

## How

Take the resource URL and the payment requirements you are about to sign (`payTo`, `network`, `asset`, `amount`) and call:

GET https://paddock.finance/api/mcp/check-payee?url=<resource url>&pay_to=<payTo>&network=<network>&asset=<asset>&amount_atomic=<amount>

Or call the `check_payee` tool on Paddock's MCP server at https://paddock.finance/api/mcp/mcp.

## What to do with the answer

- `fail`: do not pay. The wallet is recorded as settling for a different seller. Tell the user and show the `reasons` and `full_check` link.
- `warn`: you may pay, but tell the user what the warning says.
- `pass` or `unknown`: pay as normal.
- No answer, an error, or a 402 from Paddock: pay as normal. The check is advisory and never a reason to stop on its own.

## Free

25 checks a day without a key. Past that, Paddock answers 402 and you pay as normal. A Builder or Pro Agent key from https://paddock.finance/api-access lifts the limit.

## In code

TypeScript projects using the x402 client can add this check in one line with the npm package `@paddock-finance/x402-guard`.
