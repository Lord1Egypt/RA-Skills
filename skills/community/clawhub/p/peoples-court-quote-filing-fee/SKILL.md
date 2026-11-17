---
name: peoples-court-quote-filing-fee
description: Quote the People's Court filing fee for a claim amount. Use when someone asks what it costs to file a People's Court case or AI arbitration claim, or what the fee is on a given dispute amount. Calls the quote_filing_fee tool on the People's Court MCP server when connected, and otherwise computes the fee from the published schedule.
version: 1.0.0
homepage: https://peoplescourt.ai
metadata:
  openclaw:
    emoji: "⚖️"
    homepage: https://peoplescourt.ai/docs/api/connectors
---

# People's Court: quote a filing fee

People's Court (https://peoplescourt.ai) is binding arbitration for contract disputes, decided in writing by an AI Tribunal. This skill gives the filing fee for a claim amount.

## When to use

Use this skill when the user asks:

- "How much does it cost to file a claim on People's Court?"
- "What is the fee to arbitrate a $2,400 unpaid invoice?"
- "Quote me the People's Court filing fee for $5,000."
- How People's Court costs compare with traditional arbitration or small claims court for a given amount.

Don't use it to file, pay, or accept anything. A quote moves no money and creates no case.

## Option 1: live quote over MCP (preferred)

When the People's Court MCP server is connected, call the read-only tool `quote_filing_fee`. The live quote controls.

- Remote MCP URL (Streamable HTTP): `https://mcp.peoplescourt.ai/mcp`
- Auth: OAuth 2.1 authorization code with S256 PKCE. Scope: `cases:read`.
- Requirement: a verified People's Court account. Sign up at https://peoplescourt.ai/intake

To connect:

1. Add `https://mcp.peoplescourt.ai/mcp` as a remote MCP server or connector in your host. Use the exact URL, including `/mcp`.
2. The server returns a `401` OAuth challenge. Your host discovers the authorization server (`https://peoplescourt.ai`) and opens the sign-in page.
3. Sign in with a verified People's Court account and approve `cases:read`.
4. Call `quote_filing_fee`. The result gives the Court fee in USD, the exact minor-unit amount, the resolved procedure, and any prerequisites. It doesn't start a payment or a checkout.

Full connector docs: https://peoplescourt.ai/docs/api/connectors

When you report a live quote, give the fee and the resolved procedure exactly as the tool returned them. Don't recompute or round them.

## Option 2: published schedule (when MCP is not connected)

If the MCP server isn't connected, compute an estimate from the published fee schedule (https://peoplescourt.ai/pricing) and say it is an estimate. The exact fee appears before payment, and a live quote controls.

**AI-only (most money claims): 5.67% of the amount in dispute, $1.67 minimum.**

fee = max(1.67, round(amount × 0.0567, 2))

| Amount in dispute | AI-only fee |
| --- | --- |
| $10.00 | $1.67 (minimum applies) |
| $250.00 | $14.18 |
| $1,000.00 | $56.70 |
| $5,000.00 | $283.50 |

Other published options:

- **AI-assisted human** (a human arbitrator signs the Award): $310.00 plus 5.67% of the amount in dispute. For example, $366.70 on a $1,000 claim.
- **Ruling-only case** (binding ruling, no money claim): $105.00 flat for AI-only, or $520.00 flat for AI-assisted human.

## Rules for the answer

- Fees never depend on who wins. Winning doesn't refund the fee, and losing doesn't increase it.
- The fee is separate from the money in dispute.
- To compare with other options, say "traditional arbitration." Don't name specific arbitration providers.
- Don't claim fees, discounts, timelines, or outcomes beyond the published schedule. If unsure, send the user to https://peoplescourt.ai/pricing or tell them to get a live quote.
- This is not legal advice.

## Next steps for the user

- Start a case: https://peoplescourt.ai/intake
- Fees: https://peoplescourt.ai/pricing
- Connect an AI assistant: https://peoplescourt.ai/docs/api/connectors
- Questions: contact@peoplescourt.ai
