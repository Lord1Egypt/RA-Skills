---
name: nano-invoice
description: Bill for something in Nano (XNO) and know which payment belongs to which order. Creates one invoice per order with a unique exact amount (Nano has no memo field), checks the public ledger for it, and produces a receipt anyone can re-check. Read-only - it never holds a seed or sends money.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    envVars:
      - name: NANO_INVOICE_DB
        required: false
        description: SQLite file that stores your invoices. Defaults to a file in the working directory.
      - name: NANO_INVOICE_RPC
        required: false
        description: Nano node RPC to read from. Defaults to https://rpc.nano.to
---

# nano-invoice

Use this when you SELL something for Nano (XNO) and more than one buyer may pay the same
account. A Nano payment carries no memo, so two buyers sending 0.25 XNO look identical. This
skill gives every order its own invoice with a slightly different exact amount, so the payment
that arrives can only belong to one order.

It only reads the ledger and writes a local SQLite file. It never signs or sends.

All commands print JSON. Run them from this folder.

## 1. Create an invoice for an order

```
python3 -m nano_invoice create --merchant nano_YOUR_ACCOUNT --amount-xno 0.25 --order-key order-1001 --expires-s 1800
```

You get an `id` (`inv_...`), a `pay_raw` and an `instruction` such as
`send exactly 250000000000000000000000033954 raw to nano_...`. Give the buyer that instruction
word for word. `pay_raw` is the price plus a small tag; the buyer must send exactly that.

Running the same command again for the same `--order-key` returns the same invoice. It never
creates a second one, so it is safe to retry.

## 2. Check whether it was paid

```
python3 -m nano_invoice check --invoice inv_...
```

`invoice.state` is `open` until the exact amount arrives, then it records the paying block and
the sender. Serve the order only when the state shows it paid. A payment of the wrong amount, or
one that arrives after `expires_at`, does not close the invoice; it is reported under
`observations` and `refunds`.

Two optional flags keep your own money out of your income:
`--own nano_...` (an account of yours) and `--not-income nano_...=reason` (for example a faucet).

## 3. Give the buyer a receipt, or check someone else's

```
python3 -m nano_invoice receipt --invoice inv_... > receipt.json
python3 -m nano_invoice verify --receipt receipt.json
```

`receipt` works only for a paid invoice (it exits 2 for an unpaid one). `verify` re-checks every
claim in a receipt against the public ledger and exits 0 only if all of them hold - use it on a
receipt another agent hands you.

## 4. If a refund is due

```
python3 -m nano_invoice refund-hint --invoice inv_...
```

This prints who to refund and how much - the account that actually sent the money. It does not
send anything; use your wallet for that.

## Limits

- One invoice is matched by exact amount, so tell the buyer not to round it.
- The tag makes the amount unique among your open invoices, not secret.
- Checking is against a public node; if the node does not answer, nothing is concluded.

Source: https://github.com/dhyabi2/nano-invoice (MIT, Python standard library only).
