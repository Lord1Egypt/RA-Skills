# Balance

Check the current token balances in the agent wallet.

## Command

```
lobstercash crypto balance
```

## Reading the output

The output includes a `chain` field (e.g. `base`, `solana`) indicating
which network the balances are on, followed by one line per token in the
format `  <token>: <amount>`, e.g. `  usdc: 42.50`. Common tokens: `usdc`, plus
the chain's native token (`eth` on Base, `sol` on Solana).

Use the `chain` field to know which network the funds live on — this matters
when deciding parameters for `send` or `x402 fetch`.

Amount is a decimal string. Parse it as a float for arithmetic. Do not
display more than 2 decimal places to the user.

If the output says "No balances found": the wallet exists but holds no
tokens. Say "Your wallet is empty" not "wallet not found."

## When to run this skill

- Before every `send` command — check the balance covers the amount.
- Before every `x402 fetch` — check there is enough USDC.
- When the user asks "how much do I have" or similar.
- When diagnosing why a transaction failed.

## Insufficient balance

If the balance is too low for what the user wants to do:
Say: "Your wallet has [X] USDC. This needs [Y] USDC."
Then use `lobstercash crypto request --amount <needed> --description "<reason>"` to
generate a funding request link for the user.

Do not attempt the operation with insufficient funds. The error message
from the CLI in that case is technical and confusing to users.
