---
name: nano-settlement-verify
description: Check that a Nano (XNO) payment really settled before you serve a paid call. Give it the block hash, the amount you quoted and your account; it asks a public Nano node and returns one JSON verdict. Read-only - no seed, no wallet, no node of your own.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    envVars:
      - name: NANO_RPC_URL
        required: false
        description: Nano node RPC to ask. Defaults to https://rpc.nano.to
---

# nano-settlement-verify

Use this when you SELL something for Nano (XNO) - a pay-per-call endpoint, an x402 route, a
paid answer - and a buyer hands you a block hash as proof of payment. It answers one question:
did that block really pay you the amount you quoted, and has the network confirmed it?

It only reads. It never holds a seed, signs, or sends. To hold or spend Nano, use a wallet
skill; this one is the seller's check.

## Run it

```
python3 verify_cli.py BLOCK_HASH EXPECT_RAW ACCOUNT [RPC_URL]
```

- `BLOCK_HASH` - the 64-hex send block the buyer gave you.
- `EXPECT_RAW` - the amount you quoted, in raw, as an integer. 1 XNO is 10^30 raw
  (`1000000000000000000000000000000`); 0.001 XNO is `1000000000000000000000000000`.
  Never use a decimal or a float here: it loses the low digits.
- `ACCOUNT` - the `nano_` account you expected to be paid.
- `RPC_URL` - optional; any Nano node RPC.

## Read the verdict

One JSON object on stdout, and an exit code:

| exit | meaning | what to do |
| --- | --- | --- |
| 0 | `{"settled": true, ...}` - confirmed send of exactly that amount to that account | serve the call |
| 2 | `{"settled": false, ...}` - the node has the block but has not confirmed it | wait a second and ask again |
| 3 | `{"verdict": "mismatch"}` or `{"verdict": "no_such_block"}` - wrong amount, wrong payee, or no such block | do not serve |
| 4 | `{"verdict": "node_unreachable"}` - nothing was checked | retry or try another RPC; do NOT treat this as a bad payment |

Only a `send` block settles anything. A receive, open or change block is refused however well
its amount matches. The account compared is the account PAID (the block's destination), not
the chain the block sits on.

## One rule that protects you

A block hash is public the moment it is broadcast, so anyone can present someone else's
payment. Record each hash you have served and refuse it the second time, or quote a unique
amount per order so a block can match only one order.

## Source

One file, Python standard library only: https://github.com/dhyabi2/nano-settlement-verify (MIT).
