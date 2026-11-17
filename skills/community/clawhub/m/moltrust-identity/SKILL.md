---
name: moltrust-identity
version: 1.0.3
description: Register a keyless agent identity, bind a wallet to it, and read a trust score. It costs nothing and asks for no account, and the key never leaves your machine.
license: MIT-0
author: did:moltrust:157224190be24072
homepage: https://moltrust.ch/for-agents.html
---

# moltrust-identity

Get a MolTrust identity, prove a wallet belongs to it, and read a trust score.
Two calls, no account, no payment. The private key is generated on the machine
that runs this skill and is never sent anywhere.

## The one thing to understand before running it

**The key is yours and only yours. We never see it and cannot recover it.**
The DID is worthless without the key: lose it and the identity is gone, and the
only remedy is to register a new one. Write it down somewhere durable before
you make a second call with it.

This skill will not register anything unless you ask it to in the same
sentence. There is no background registration, no "while we're here", and no
default that creates an identity for you.

## Usage

```
moltrust register                 # mints a DID, prints the key once
moltrust bind <did> <key>         # proves a wallet belongs to the DID
moltrust score <did>              # reads the trust score of any DID
moltrust probe <did> <key>        # shows what an endpoint charges with and without proof
```

## What the agent does

### `register`

1. `GET https://api.moltrust.ch/identity/register-challenge` for a challenge
   string, a proof-of-work seed and a difficulty.

2. Generate an Ed25519 keypair **locally**. Never transmit the private half.

3. Solve the proof of work: find a nonce where
   `sha256(pow_seed || nonce)` has at least `difficulty_bits` leading zero bits.

4. Sign the challenge string with the private key.

5. `POST https://api.moltrust.ch/identity/register-pop` with
   `{public_key, challenge, signature, pow_nonce, display_name, platform,
   source}`. Send `source: "clawhub"` so the registry can tell which channel
   the agent arrived through; it is used for counting and nothing else.

6. Print the DID and the private key, once, with the warning above. Do not
   write the key to a log, a temp file or the conversation history.

### `bind`

1. `GET /identity/nonce` for a fresh nonce.
2. Sign it with the **wallet** key, not the DID key.
3. `POST /identity/bind` with the DID, the address and the signature.

A wallet binds to one DID and no more. A second attempt answers
`409 Wallet already bound to another DID`, which is the endpoint working, not
failing.

### `score`

`GET /skill/trust-score/<did>`. No key needed, and it works for any DID, not
only your own.

A score can come back withheld. That is deliberate: below three endorsements
the registry reports no number rather than a low one, because a number derived
from one opinion looks like a measurement and is not.

### `probe`

Runs `scripts/gate_probe.py` from the MolTrust repository against a paid
endpoint and prints what it costs with and without proof. It signs with the
reader's own key, holds no wallet and pays nothing.

Read the script before running it:
https://github.com/MoltyCel/moltrust-api/blob/main/scripts/gate_probe.py

## What this does not do

It does not pay for anything, hold funds, or sign a transaction. It does not
register an identity as a side effect of any other command. It does not upload
a key, and there is no "recover my DID" path because there is nothing on our
side to recover it from.

## Reference

Docs: https://api.moltrust.ch/docs ·
Registry proof: https://moltrust.ch/registry-proof.html
