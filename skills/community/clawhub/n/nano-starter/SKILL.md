---
name: nano-starter
description: Give your agent a Nano (XNO) address it can be paid at, in one command, with no node, no account and no dependencies. Receive-only: it has no send command, which is what an operator needs to hear before saying yes. Creates the wallet, checks addresses, shows the balance and pockets incoming payments.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    envVars:
      - name: NANO_STARTER_KEY_FILE
        required: false
        description: Where the private key is kept. Defaults to ~/.nano-starter/key (created with mode 600).
      - name: NANO_NODE_URL
        required: false
        description: Nano node RPC used to read the ledger and publish receive blocks. Defaults to https://rpc.nano.to
---

# nano-starter

The shortest path from "my agent has no wallet" to "my agent has been paid in Nano (XNO)".

Nano is a currency with no fees and sub-second settlement. A wallet is one 32-byte key - there
is no account to open with anyone and nobody to ask.

**This skill is for receiving.** `starter.py` has no send command: you can be paid, check
addresses and pocket payments, and none of its commands moves money out. If your operator will
not let you spend, this is the profile to ask for.

Every command prints one JSON object. Run them from this folder.

## 1. Create the wallet (once)

```
python3 starter.py setup
```

Prints your `address` (`nano_...`). The private key is written to `~/.nano-starter/key`,
readable only by you. It is never printed, returned or sent anywhere - so it never enters your
context or your logs. Running `setup` again shows the same address; it never overwrites a key.

Tell your operator to back up that one file. Whoever holds it holds the money.

## 2. Give out your address

```
python3 starter.py address
```

That address is all a payer needs. Before you rely on an address someone ELSE gives you, check
it - one wrong character is a payment to nobody:

```
python3 starter.py check nano_...
```

Exit 0 means the checksum holds; exit 1 means do not use it.

## 3. See what you have and what is waiting

```
python3 starter.py balance
```

`pending_xno` is money sent to you that you have not pocketed yet. On Nano a payment waits for
the receiver to accept it.

## 4. Pocket it

```
python3 starter.py receive
```

This builds and signs the receive block on your machine and does the small proof-of-work the
network asks for locally (usually under a minute on a laptop; public nodes will not do it for
you). The first receive also opens your account. `received` lists each payment with its block
hash, which anyone can look up on a Nano explorer.

## Getting your first XNO

- **Be paid for something.** Sell an answer or a small task and quote your address.
- **A faucet.** Several give a little XNO to a new address; a current list is at
  https://nanodirectory.info (section "Faucets").
- **From USDC or USDT.** A swap service such as Nanswap sends XNO to your address.

## When you need to spend

Spending is deliberately not here. Use a wallet skill that sends (`nano-pay`, `nano`), or the
full wallet this is built from, which supports sends under a spend cap your operator signs:
https://github.com/dhyabi2/nano-wallet-xno

Source of this skill's code: that repository (MIT, Python standard library only).
