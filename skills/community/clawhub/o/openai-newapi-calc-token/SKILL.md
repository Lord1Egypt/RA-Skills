---
name: token-cost-skill
description: Use when calculating, auditing, implementing, or reviewing token pricing and billing formulas for OpenAI-style APIs, NewAPI-compatible gateways, cached input/prompt caching, per-1K or per-1M token prices, quota consumption, recharge ratios, and cost comparison dashboards.
---

# Token Cost Skill

Use this skill to calculate or review token billing without double-counting cached tokens or mixing incompatible pricing units.

## Core Rules

1. Identify the billing mode before calculating:
   - `openai-raw`: provider price table has input, cached input, and output prices.
   - `newapi-quota`: gateway billing uses model ratio, completion/output ratio, and group ratio.
   - `custom-multiplier`: dashboard-specific per-1K/per-1M cost projection.
2. Normalize price units first:
   - `/1K` prices use divisor `1000`.
   - `/1M` prices use divisor `1000000`.
3. Treat cached input as a subset of input tokens, not an extra token bucket.
4. Keep quota formulas separate from money formulas; only convert quota to money after quota is computed.
5. Show the expanded formula with the final result so users can audit every multiplier.

## OpenAI-Style Raw Pricing

Inputs:

- `inputTokens`: total input tokens reported for the request.
- `cachedInputTokens`: cached input tokens inside `inputTokens`.
- `outputTokens`: output tokens.
- `inputPrice`: non-cached input price per selected unit.
- `cachedInputPrice`: cached input price per selected unit.
- `outputPrice`: output price per selected unit.

Formula:

```text
unitDivisor = 1000 if priceUnit = "1K", else 1000000
cachedInputTokens = min(max(cachedInputTokens, 0), max(inputTokens, 0))
nonCachedInputTokens = max(inputTokens, 0) - cachedInputTokens

inputCost = (nonCachedInputTokens / unitDivisor) * inputPrice
cachedInputCost = (cachedInputTokens / unitDivisor) * cachedInputPrice
outputCost = (max(outputTokens, 0) / unitDivisor) * outputPrice
totalCost = inputCost + cachedInputCost + outputCost
totalTokens = max(inputTokens, 0) + max(outputTokens, 0)
```

Never use:

```text
totalTokens = inputTokens + cachedInputTokens + outputTokens
```

`cachedInputTokens` is already included in `inputTokens`.

## NewAPI-Compatible Quota Pricing

Use this mode when the gateway bills quota/credits by ratios.

Standard request quota formula:

```text
quota = (promptTokens + completionTokens * completionRatio) * modelRatio * groupRatio
```

Common money conversion:

```text
usdEquivalent = quota / 500000
actualCost = usdEquivalent / rechargeRatio
```

Notes:

- `completionRatio` is also called output ratio, completion multiplier, or completion billing ratio.
- `groupRatio` is the group multiplier.
- `modelRatio` is the model multiplier.
- `rechargeRatio` is not part of the quota formula; it is a post-processing conversion for real paid cost.

## Custom Multiplier Dashboards

Use only when a dashboard intentionally projects per-1K or per-1M prices instead of computing gateway quota.

```text
inputCost1K = basePrice1K * modelMultiplier * groupMultiplier / rechargeRatio
outputCost1K = basePrice1K * modelMultiplier * outputMultiplier * groupMultiplier / rechargeRatio
cacheReadCost1K = basePrice1K * modelMultiplier * cacheReadMultiplier * groupMultiplier / rechargeRatio
cacheCreateCost1K = basePrice1K * modelMultiplier * cacheCreateMultiplier * groupMultiplier / rechargeRatio
```

If `basePrice` is entered per 1M, convert first:

```text
basePrice1K = basePrice1M / 1000
```

## Verification Checklist

- Confirm whether token counts are request usage counts or price table units.
- Confirm whether `cachedInputTokens` is included inside `inputTokens`.
- Confirm whether prices are per `1K` or per `1M`.
- For OpenAI-style pricing, calculate non-cached input before calculating cost.
- For NewAPI-style pricing, calculate quota before converting to USD or local currency.
- Clamp negative token counts to `0`.
- Clamp cached input to no more than total input.
- Protect against division by zero in recharge ratio.
- Add tests for one normal case, one cached-input case, one unit-conversion case, and one zero-token case.

## Common Mistakes

| Mistake | Correct handling |
| --- | --- |
| Adding cached input to total input | Subtract cached input from input to get non-cached input |
| Mixing `/1K` and `/1M` prices | Normalize with the correct divisor first |
| Applying recharge ratio inside NewAPI quota | Compute quota first; apply recharge ratio only to money conversion |
| Using output price for cached input | Cached input uses its own price |
| Letting cached input exceed input | Clamp cached input to input tokens |

## Reference

Read `references/formulas.md` when you need source notes, examples, or implementation snippets.
