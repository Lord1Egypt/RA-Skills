# Transactions

Sign and submit an arbitrary blockchain transaction outside Lobster Cash. Use this when another tool, skill, or external system provides a serialized transaction or a calls array that needs to be executed using the agent's wallet.

Do not use this for simple token transfers — use the send reference instead.

## When to use this skill

- Another agent skill (e.g. Jupiter swap, xStocks, any DeFi protocol)
  hands you a serialized transaction to execute
- An external system provides a calls array
- You need to inspect or manually control the sign/submit steps

## Transaction types

The `--type` flag determines what kind of transaction to create:

- **`serialized`** — A fully built, serialized transaction provided by an external tool or protocol (e.g. Jupiter swap, xStocks). The agent does not construct it — it just signs and submits. Use `--serialized-transaction` to pass the payload.
- **`calls`** — A JSON array of raw on-chain instruction calls. Use this when an external system gives you structured instructions rather than a pre-built transaction. Use `--calls` to pass the JSON array. Optionally add `--chain` to override the target chain.
- **`transfer`** — A simple token transfer (uses `--to`, `--amount`, `--token`). In practice, prefer the `send` command instead — it does the same thing in one step without the create→approve flow.

## Step 1 — Create the transaction

The `--serialized-transaction` flag accepts the payload in **base58**
(canonical), **base64**, or **0x-prefixed hex**. The proxy auto-detects
the encoding, so you can pass Jupiter / RPC / wallet-builder output
through verbatim without re-encoding it client-side.

For a serialized transaction from an external source:

```
lobstercash crypto tx create \
  --type serialized \
  --serialized-transaction <base58-or-base64-or-0xhex-transaction>
```

For a calls array:

```
lobstercash crypto tx create \
  --type calls \
  --calls '<json array>'
```

Parse the output. You need these values from the result:

- `Transaction ID` — pass as `--id` to approve
- The `messageToSign` and `messageToSignEncoding` values from the "Next step" line

The output includes a ready-made `lobstercash crypto tx approve` command you can copy.

## Step 2 — Approve the transaction

```
lobstercash crypto tx approve \
  --id <transactionId> \
  --message <messageToSign> \
  --encoding <messageToSignEncoding>
```

The command waits for on-chain confirmation by default.

## Step 3 — Check status (if needed)

If you need to re-check after the fact:

```
lobstercash crypto tx status \
  --id <transactionId>
```

## Reading the output

- `transaction.status`: `success`, `failed`, or `pending`
- `transaction.hash`: on-chain transaction hash
- `transaction.explorerLink`: Chain explorer URL

## Reporting to the user

Say: "Transaction submitted." and include the explorer URL so the user can verify it themselves. A clickable link is more useful than a raw hash.

Do not show the raw transaction hash or transaction ID unless the user specifically asks for it.

## What NOT to do

- Do not use this skill for simple token transfers. Use the send skill.
- Do not assume success from a pending status — commands wait for on-chain confirmation automatically.
- Do not construct serialized transactions yourself. This skill receives
  them from external sources — it does not build them.
