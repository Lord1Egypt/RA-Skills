# Token Cost Formula Reference

## OpenAI-Style Raw Pricing

OpenAI pricing tables distinguish `Input`, `Cached input`, and `Output` prices. Prompt caching usage reports cached tokens as part of input/prompt tokens, so cached tokens must be split out before pricing.

Example with `/1M` prices:

```text
inputTokens = 100000
cachedInputTokens = 20000
outputTokens = 50000
inputPrice = 5
cachedInputPrice = 0.5
outputPrice = 15

nonCachedInputTokens = 100000 - 20000 = 80000
inputCost = 80000 / 1000000 * 5 = 0.4
cachedInputCost = 20000 / 1000000 * 0.5 = 0.01
outputCost = 50000 / 1000000 * 15 = 0.75
totalCost = 0.4 + 0.01 + 0.75 = 1.16
```

JavaScript implementation pattern:

```js
function calculateOpenAI({
  priceUnit = "1M",
  inputPrice = 0,
  cachedInputPrice = 0,
  outputPrice = 0,
  inputTokens = 0,
  cachedInputTokens = 0,
  outputTokens = 0,
}) {
  const divisor = priceUnit === "1K" ? 1000 : 1000000;
  const totalInput = Math.max(Number(inputTokens) || 0, 0);
  const cachedInput = Math.min(Math.max(Number(cachedInputTokens) || 0, 0), totalInput);
  const nonCachedInput = totalInput - cachedInput;
  const output = Math.max(Number(outputTokens) || 0, 0);

  const inputCost = (nonCachedInput / divisor) * (Number(inputPrice) || 0);
  const cachedInputCost = (cachedInput / divisor) * (Number(cachedInputPrice) || 0);
  const outputCost = (output / divisor) * (Number(outputPrice) || 0);

  return {
    inputCost,
    cachedInputCost,
    outputCost,
    totalCost: inputCost + cachedInputCost + outputCost,
    totalTokens: totalInput + output,
  };
}
```

## NewAPI-Compatible Quota Pricing

NewAPI-compatible gateways commonly bill request quota with:

```text
quota = (promptTokens + completionTokens * completionRatio) * modelRatio * groupRatio
```

Then convert quota to money:

```text
usdEquivalent = quota / 500000
actualCost = usdEquivalent / rechargeRatio
```

Example:

```text
promptTokens = 1000
completionTokens = 500
completionRatio = 2
modelRatio = 15
groupRatio = 1

quota = (1000 + 500 * 2) * 15 * 1 = 30000
usdEquivalent = 30000 / 500000 = 0.06
```

## Custom Multiplier Cost Projection

Use this only when the user intentionally asks for a per-1K/per-1M dashboard, not gateway quota.

```text
inputCost1K = basePrice1K * modelMultiplier * groupMultiplier / rechargeRatio
outputCost1K = basePrice1K * modelMultiplier * outputMultiplier * groupMultiplier / rechargeRatio
cacheReadCost1K = basePrice1K * modelMultiplier * cacheReadMultiplier * groupMultiplier / rechargeRatio
cacheCreateCost1K = basePrice1K * modelMultiplier * cacheCreateMultiplier * groupMultiplier / rechargeRatio
```

Weighted comparison:

```text
weightedCost1M = (inputCost1M * inputWeight + outputCost1M * outputWeight) / (inputWeight + outputWeight)
```

If all weights are zero, use denominator `1` and return `0` or the safe computed default instead of dividing by zero.
