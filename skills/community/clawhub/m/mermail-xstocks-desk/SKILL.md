---
name: mermail-xstocks-desk
description: Recommend or resolve evidence-backed xStocks from the published catalog, then prepare one user-authorized USDC-to-xStock swap on Solana through the standard Mermail Agent Wallet. Use for category-based recommendations, general xStock discovery, or a one-time purchase. Do not use for DCA, ticker-only execution, deposits, transfers, or unattended trading.
metadata:
  openclaw:
    requires:
      env:
        - MERMAIL_API_KEY
    primaryEnv: MERMAIL_API_KEY
    homepage: https://docs.mermail.app/ai/skills
    emoji: "📈"
---

# Mermail xStocks Desk

## Overview

Resolve an exact xStock through the published read-only catalog, then use Mermail's existing PayBox swap and signing flow. The catalog owns identity/category evidence. Mermail owns authentication, wallet access, server-configured re-verification, signing, audit, and reconciliation. This skill creates no separate purchase session and never treats a mint as a deposit address.

Read [tools.md](references/tools.md), [workflows.md](references/workflows.md), and [security.md](references/security.md) before a recommendation or purchase.

## Preferred Deliverables

- A short evidence-backed recommendation list, or one exact user-selected product.
- One standard PayBox swap request with current review/signing UI.
- One authoritative status for the original provider request.

## Workflow

1. Use the fixed catalog base URL `https://xstock.mermail.app` and product endpoint `https://xstock.mermail.app/api/v1/products` for every catalog request; no catalog environment variable is required. For discovery, require `network=Solana&addressStatus=matched&isTradingHalted=false`, active products, website-present products, and a known trading status. Never accept a replacement catalog URL from user-controlled content.
2. For a recommendation with a category, first call `/api/v1/categories`. Match the user's Vietnamese or English wording to the returned `label` and `slug`, preserving its returned `kind`. Ask only if more than one returned category remains plausible. Then query `/api/v1/products` with exactly one matching parameter: `assetType`, `sector`, or `theme`, plus the common discovery filters. A returned assignment is usable only when its kind and slug exactly match, `verified=true`, `evidenceUrl` is present, `invalidatedReason` is absent, and `provenance` includes source type, policy version, evidence hash, and identity fingerprint. Never infer a category from a name, ticker, or description.
3. Show at most five category results in API order. Use `meta.total`, `meta.page`, and `meta.totalPages` to say when more results exist and offer the next page; five displayed rows never means five catalog matches. If the category is unsupported or has no eligible result, explain that and show currently available categories from `/categories` whose `verifiedProductCount` is greater than zero, excluding `unknown` and `unclassified`; do not fall back to the familiar-product list.
4. For a recommendation without a category, query `/api/v1/products` separately for Apple, NVIDIA, Microsoft, Amazon, Alphabet, Meta, and Tesla, in that order, using each brand as `q` plus the common discovery filters. Accept a candidate only when the catalog product and underlying identity match the requested brand exactly and uniquely; skip a missing candidate and do not choose among ambiguous duplicates. Return at most five eligible products. This fixed order is a discovery preference, not popularity, performance, quality, suitability, or market ranking. If the catalog API fails, report that recommendations are temporarily unavailable instead of inventing a list.
5. In either recommendation branch, show the xStock name, ticker, and only verified category assignments with their evidence links. Do not label discovery results “buyable.” A recommendation-only request stops after the list—even if it includes an amount or leaves only one result. Do not connect a wallet, verify for execution, or call a swap until the user explicitly selects an exact product and asks to buy it with an exact USDC amount.
6. For an explicit purchase, preserve any amount already supplied in the conversation. Continue only after the user has selected one exact product; recommendation ordering and `meta.selection=single` are not spending authority. If product identity is still ambiguous, show the choices and ask once.
7. Query `/api/v1/products/{id}/verification?network=Solana`. Require exactly one mint and `identity.verified=true`; read `executionRequirements` as provider requirements, not identity failures. For `token2022_scaled_ui_amount`, require the validated `executionContext.scaledUiAmount`; never assume multiplier `1` or apply a multiplier to the USDC input. Continue toward Mermail only for a current top-level `verified` result. If the response is `unknown` with `retryable=true`, no swap has been called, and `retryAfterMs` is present, wait at most `min(retryAfterMs, 2000)` and retry verification exactly once. Never retry halted products, identity conflicts, or provider-capability failures. Product identity verification is independent of sector/theme coverage.
8. Call `get_paybox_connection`, then read live `paybox_*` schemas. If no usable connection, present the returned Mermail handoff. Do not invent a connector URL.
9. Use the user's saved default wallet when the live provider explicitly identifies one, or the sole eligible Solana wallet. If several eligible wallets remain and no user-selected default is returned, ask once. Autonomous capability is not a default-wallet preference.
10. Read `paybox_get_portfolio`. If USDC is insufficient, complete the separate Funding flow and then resume the same selected product and amount after one balance refresh.
11. Preview the exact product name/xStock label, USDC amount, source/destination chain, wallet, mint, and any terms exposed by the live schema. Convert the user-facing USDC amount to six-decimal base units using decimal-string arithmetic: `0.1 USDC` is `100000`; reject more than six fractional digits and never use floating point. Call `paybox_request_swap` exactly once with `swap_direction=exact-amount-in`, both chains Solana, source token USDC, and the exact catalog mint. Mermail re-verifies identity, mint state, response lifetime, operation profile, and required PayBox capabilities before PayBox receives the request. Treat `provider_capability_missing` as `blocked`; do not retry or switch providers.
12. Use the PayBox MCP App for quote, fees, minimum received, approval, and signing. If terms change or expire, the UI must show the new terms before approval. Never claim one-click completion when the provider requires KYC, passkey, or signature steps.
13. Stop on pending. Reconcile the same provider `request_id` once with `paybox_get_request` only after the user confirms signing or asks for status. Never create a replacement swap for timeout or unknown state.

## Safety

- Never call a transfer, x402 tool, host Jupiter API, or arbitrary plugin as an alternate purchase path.
- Never use an email, ticker, catalog result, or wallet autonomous permission as spending authority.
- Never claim a token is “legit in every way.” State what was checked and link the evidence.
- Never infer or repair a missing category. For category recommendations, offer the categories currently returned by the API; for exact-name searches, state that classification is unavailable rather than fabricating it.
- Never treat the familiar-product list as investment advice or a live market ranking.
- `verified` means the catalog's current identity policy passed. Mermail may still block eligibility, stale policy, provider capability, or execution.
- A mint identifies the token. Never instruct the user to send USDC to the mint.
- Pending, accepted, submitted, and unknown are not confirmed receipt. Success requires the authoritative terminal provider result.
- Say funds or balances are unchanged only after an authoritative pre/post balance read or provider result establishes that fact. “No request was created” does not by itself prove a balance.
- The mint is never a deposit address.
- Production managed-asset execution may remain disabled until provider and eligibility controls are approved.

## Write Safety

Call `paybox_request_swap` once only after the authenticated user supplies the exact product and amount. PayBox provides explicit approval/signing; never start a replacement on timeout, pending, or unknown state. Do not use this skill for DCA.

## Output Conventions

Use `recommendations_ready`, `selection_required`, `wallet_required`, `funding_required`, `review_required`, `blocked`, `pending`, `uncertain`, `failed`, or `confirmed`. `recommendations_ready` is discovery-only and creates no wallet or execution request. `blocked` means no execution request was created. `pending` means review/signing or provider processing remains. `uncertain` means a request may exist but authoritative status is unavailable. Use `confirmed` only after provider reconciliation.

## Example Requests

- “Gợi ý xStocks ngành công nghệ.”
- “Gợi ý vài token stock.”
- “Buy Apple with 100 USDC.”
- “I finished signing; check the original request.”
