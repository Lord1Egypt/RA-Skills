# Example: Read-Only Quote with Fee Analysis

Fetch a swap quote from Orca without any on-chain interaction. Read-only — no wallet or keypair needed.

> **Playbook**: [Swap (single-pool)](../SKILL.md#swap-single-pool) — quote-only variant of the swap flow.

## Using curl

```bash
curl -s "https://pools-api.mainnet.orca.so/swap-quote?\
from=So11111111111111111111111111111111111111112&\
to=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v&\
amount=1000000000&\
slippageBps=100&\
amountIsInput=true"
```

## Using TypeScript

```typescript
const SNORKEL_URL = process.env.SNORKEL_URL ?? "https://pools-api.mainnet.orca.so";

const MINTS: Record<string, { address: string; decimals: number }> = {
  SOL:     { address: "So11111111111111111111111111111111111111112", decimals: 9 },
  USDC:    { address: "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", decimals: 6 },
  USDT:    { address: "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB", decimals: 6 },
  ORCA:    { address: "orcaEKTdK7LKz57vaAYr9QeNsVEPfiu6QeMU1kektZE", decimals: 6 },
  BONK:    { address: "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263", decimals: 5 },
  JitoSOL: { address: "J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn", decimals: 9 },
  JUP:     { address: "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN", decimals: 6 },
};

interface SwapHop {
  pool: string;
  input: { mint: string; amount: string };
  output: { mint: string; amount: string };
  fees: {
    transferFee: Record<string, unknown>;
    tradeFee: {
      base: { amount: string; feeRate: string };
    };
  };
}

interface QuoteResponse {
  data: {
    request: {
      from: string;
      to: string;
      amount: string;
      slippageBps: string;
      amountIsInput: string;
    };
    swap: {
      inputAmount: string;
      outputAmount: string;
      split: SwapHop[][];
    };
    price_impact?: string;
  };
}

async function fetchQuote(
  fromSymbol: string,
  toSymbol: string,
  amount: number,
  slippageBps = 100
): Promise<void> {
  const from = MINTS[fromSymbol];
  const to = MINTS[toSymbol];
  if (!from || !to) {
    throw new Error(`Unknown token: ${!from ? fromSymbol : toSymbol}`);
  }

  const amountBaseUnits = String(Math.round(amount * 10 ** from.decimals));
  const params = new URLSearchParams({
    from: from.address,
    to: to.address,
    amount: amountBaseUnits,
    slippageBps: String(slippageBps),
    amountIsInput: "true",
  });

  const res = await fetch(`${SNORKEL_URL}/swap-quote?${params}`);
  if (!res.ok) {
    throw new Error(`Quote failed: ${res.status} ${await res.text()}`);
  }

  const quote: QuoteResponse = await res.json();
  const swap = quote.data.swap;

  // --- Human-readable output ---

  const inputHuman = Number(swap.inputAmount) / 10 ** from.decimals;
  const outputHuman = Number(swap.outputAmount) / 10 ** to.decimals;
  const rate = outputHuman / inputHuman;

  console.log(`\n=== Orca Quote: ${fromSymbol} -> ${toSymbol} ===\n`);
  console.log(`Input:      ${inputHuman} ${fromSymbol}`);
  console.log(`Output:     ${outputHuman.toFixed(6)} ${toSymbol}`);
  console.log(`Rate:       1 ${fromSymbol} = ${rate.toFixed(6)} ${toSymbol}`);

  if (quote.data.price_impact) {
    console.log(`Price impact: ${quote.data.price_impact}`);
  }

  // --- Fee analysis ---

  console.log(`\n--- Fee Analysis ---\n`);

  const hops = swap.split.flat();
  let totalFeeBaseUnits = 0;

  for (let i = 0; i < hops.length; i++) {
    const hop = hops[i];
    const feeAmount = Number(hop.fees?.tradeFee?.base?.amount ?? 0);
    const feeRate = Number(hop.fees?.tradeFee?.base?.feeRate ?? 0);
    const inputAmount = Number(hop.input.amount);
    const inputMint = hop.input.mint;

    const feeMintSymbol = Object.entries(MINTS).find(
      ([_, m]) => m.address === inputMint
    );
    const feeDecimals = feeMintSymbol ? feeMintSymbol[1].decimals : from.decimals;
    const feeHuman = feeAmount / 10 ** feeDecimals;
    const feePercent = feeRate / 10000;

    console.log(`Leg ${i + 1}:`);
    console.log(`  Pool:     ${hop.pool}`);
    console.log(`  In:       ${(inputAmount / 10 ** feeDecimals).toFixed(6)} ${feeMintSymbol?.[0] ?? hop.input.mint.slice(0, 8)}`);
    console.log(`  Fee:      ${feeHuman.toFixed(6)} ${feeMintSymbol?.[0] ?? "?"} (${feePercent.toFixed(2)}%, feeRate: ${feeRate})`);

    totalFeeBaseUnits += feeAmount;
  }

  const totalFeePercent = (totalFeeBaseUnits / Number(swap.inputAmount)) * 100;

  console.log(`\nTotal fee:  ${totalFeePercent.toFixed(4)}% of input`);
  console.log(`Routes:     ${swap.split.length} split(s), ${hops.length} hop(s)`)
}

// --- Run ---

fetchQuote("SOL", "USDC", 1).catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
```

## Output

```
=== Orca Quote: SOL -> USDC ===

Input:      1 SOL
Output:     80.892868 USDC
Rate:       1 SOL = 80.892868 USDC
Price impact: 0.0202696185559360146479140100

--- Fee Analysis ---

Leg 1:
  Pool:     FpCMFDFGYotvufJ7HrFHsWEiiQCGbkLCtwHiDnh7o28Q
  In:       1.000000 SOL
  Fee:      0.000200 SOL (0.02%, feeRate: 200)

Total fee:  0.0200% of input
Routes:     1 split(s), 1 hop(s)
```

> Representative output. Actual quote values vary with live market conditions.

## Other Quote Examples

### USDC to ORCA

```bash
curl -s "https://pools-api.mainnet.orca.so/swap-quote?\
from=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v&\
to=orcaEKTdK7LKz57vaAYr9QeNsVEPfiu6QeMU1kektZE&\
amount=100000000&\
slippageBps=100&\
amountIsInput=true"
```

This quotes 100 USDC (100 * 10^6 = 100000000 base units) to ORCA.

### BONK to SOL

```bash
curl -s "https://pools-api.mainnet.orca.so/swap-quote?\
from=DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263&\
to=So11111111111111111111111111111111111111112&\
amount=100000000000&\
slippageBps=200&\
amountIsInput=true"
```

This quotes 1,000,000 BONK (1000000 * 10^5 = 100000000000 base units) to SOL with 2% slippage tolerance (suitable for volatile pairs).

### Exact Output Quote

To get a quote for an exact output amount instead of exact input, set `amountIsInput=false`:

```bash
curl -s "https://pools-api.mainnet.orca.so/swap-quote?\
from=So11111111111111111111111111111111111111112&\
to=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v&\
amount=100000000&\
slippageBps=100&\
amountIsInput=false"
```

This asks: "How much SOL do I need to get exactly 100 USDC?"
