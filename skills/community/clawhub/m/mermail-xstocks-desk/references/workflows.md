# Workflows

## Exact request: “Buy Apple with 100 USDC”

1. Search the published catalog using the explicit text. If the complete result is uniquely selectable, preserve that product and `100 USDC`; otherwise ask the user to choose from a short list.
2. Verify the chosen product on Solana and preserve its exact mint/evidence. Require the snapshot-backed identity result and read live RPC dependency checks separately. Before any swap exists, a retryable dependency error may be checked once after at most two seconds; all other failures stop immediately.
3. Probe PayBox. Use a provider-declared user default or the sole eligible wallet; ask only when multiple choices remain. Never infer default from autonomous permission.
4. Read portfolio. If funding is needed, open the returned Funding handoff, retain the product/amount in conversation state, then refresh balance once.
5. Show the exact proposed pair and amount. Convert USDC to base units using decimal strings (`0.1` → `100000`) without applying the xStock display multiplier, then call `paybox_request_swap` once as Solana exact-in. Let its MCP App show current quote, fee, minimum received, approval, and signing.
6. Stop on pending. After the user finishes or asks for status, call `paybox_get_request` once using the same request ID.

## Recommendation with category: “Gợi ý xStocks ngành công nghệ”

1. Fetch `/api/v1/categories` and match “công nghệ” against returned Vietnamese/English-equivalent labels or slugs. Preserve the returned category kind. If several real categories plausibly match, show them and ask the user to disambiguate.
2. Query the matching `assetType`, `sector`, or `theme` slug with the common Solana, matched-address, non-halted, active, and website-present filters. Do not derive a category from a product name or ticker.
3. Validate the exact category assignment on every product. Exclude it when verification, evidence URL, provenance, or invalidation state does not satisfy the contract.
4. Present at most five products in API order with xStock name, ticker, verified category, and evidence link. If `meta.total` exceeds the displayed count, state how many additional matches exist and offer to fetch the next page.
5. Stop with `recommendations_ready`. Do not verify for execution, inspect wallets, or request a swap until the user selects one exact product and gives an exact USDC purchase amount.

If the category is unsupported or yields no eligible product, say so and present returned categories whose `verifiedProductCount` is greater than zero, excluding `unknown` and `unclassified`. Do not silently use the familiar-product list, broaden the category, or revive an invalidated assignment. Missing sector/theme does not block a later exact-product purchase whose mint verification succeeds.

## Recommendation without category: “Gợi ý vài token stock”

Search the catalog separately in this fixed order: Apple, NVIDIA, Microsoft, Amazon, Alphabet, Meta, Tesla. Every search uses the common discovery filters. Accept only a unique exact match for the intended product/underlying identity; skip missing brands and surface duplicate ambiguity without choosing. Return the first five accepted products, or fewer when fewer qualify.

Describe the order as a familiar-name discovery list, never as popularity, performance, suitability, or a live market ranking. Show only verified categories and their evidence links. On any catalog API failure, report that live recommendations could not be loaded; do not fill gaps from memory. Stop with `recommendations_ready` and make no PayBox call.

## Recommendation mentions an amount but no product is selected

“Gợi ý token stock để mua với 100 USDC” remains a recommendation request. Preserve `100 USDC` in conversation state, return the appropriate category or familiar-name list, and ask the user to choose. Do not treat the amount, list order, a single remaining candidate, or `meta.selection=single` as authorization to verify for execution or open PayBox. After the user explicitly selects a product, continue the exact-purchase workflow with the preserved amount.

## Changed or expired terms

The PayBox UI must display refreshed terms. Do not submit silently. If the user closes and reopens the handoff, continue the existing request; do not call `paybox_request_swap` again.

## Timeout or uncertain outcome

Keep the original request ID. Reconcile it; never create a second transaction. Report `uncertain` when authoritative status is unavailable.

## Verification and execution capability

`identity.verified` proves the current catalog fingerprint and exact evidence checks. It does not prove PayBox can execute every Token-2022 behavior. Pass `executionRequirements` and `executionContext` through to the normal Mermail guard. Scaled UI multipliers affect display only: never scale the USDC input or raw route amounts. If Mermail returns `provider_capability_missing`, report the named capability and stop without retrying verification, calling another provider, or creating a fallback transaction.

Use `blocked` only before an execution request is created, `pending` after a request awaits review/signing/provider processing, and `uncertain` when submission may have occurred but status cannot be reconciled. Do not claim a balance is unchanged unless it was read or established by an authoritative result.
