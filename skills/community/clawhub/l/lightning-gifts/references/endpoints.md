# Routes used by the giver flow

Everything is served by the same service that renders the site, under `{APP_URL}/api` with
`{APP_URL} = https://lightning.gifts`. JSON in and out; there is no versioned public API and no SDK,
so treat route names and payload shapes as fixed.

Payload fields keep the code's vocabulary: `tipId`, `tipperId`, `tippeeId` — even on the
gift-named routes. A gift is a "tip", a giver a "tipper", a recipient a "tippee".

| Response | Means |
| --- | --- |
| `401` | no credential was accepted |
| `403` | the credential was valid but the caller is someone else |
| `409` | the state forbids it (already claimed, giver is caller, expired, not mintable) |
| `410` | the one-time proof is missing or spent |
| `422` | this deployment's invoice cap is lower than `amount + fee` |
| `429` | rate limited |
| `500` | money-path refusal, kill switch, or payout failure — read the body text |

## Giver routes

A user key acting as its own user, or a session.

| Route | Methods | Notes |
| --- | --- | --- |
| `/api/gifts` | POST, GET | POST creates (`amount`, `currency`, `expiry`, `onboardingFlow`, `tippeeLocale`, `anonymousTipper`, `generatePassphrase`, `passphraseLength`; optionally `note`, `tippeeName`, `claimWebhookUrl`, `withdrawWebhookUrl`). Response: `id`, `amount`, `fee`, `invoice`, `status`, `expiry` — and the full gift record rides along (`tipperId`, `invoiceId`, `version` — the optimistic-concurrency token for `PUT` — plus `passphrase` when generated; `withdrawalId` appears only once the gift reaches `WITHDRAWN`). GET lists the caller's gifts; with the operator key, `?expired=true&reclaimable=true` returns the reclaimable set. |
| `/api/gifts/{id}` | GET, PUT, DELETE | Read or update a pending gift. DELETE refuses with `409` if the funding invoice was paid, the wallet re-check fails, or the invoice could not be cancelled (money-safety guard, fails closed; see `pitfalls.md` #8). |
| `/api/gifts/{id}/claimToken` | POST | `{claimUrl}` out. Single use, ≤7 days and ≤ gift expiry; `{"printed":true}` mints to the gift's own expiry; `SKIP` gifts get 30 days. `409` unless funded, unclaimed and unexpired. |
| `/api/gifts/{id}/reclaim` | POST | `204`. Moves a reclaimable gift's sats to the giver's staging wallet. Damped 10/min. |
| `/api/gifts/{id}/markCopied` | POST | Printed-card bookkeeping. |
| `/api/gifts/{id}/generatePassphrase` | POST | Replace the gift's claim passphrase. |

## Handoff — what the recipient does

Include this when you explain the gift to the recipient; you do not drive it.

| Route | Methods | Notes |
| --- | --- | --- |
| `/api/received-gifts/{id}` | GET | Public shape of one gift: `amount`, `hasClaimed`, `status`, `type`, `tipper{…}` and more of the id in the claim link — so a recipient **can** confirm the amount from the by-id read before claiming (the list endpoint is what hides it). |
| `/api/received-gifts/{id}/markSeen` | POST | `UNSEEN` → `SEEN`. The gift page calls it on open. |
| `/api/received-gifts/{id}/claim` | POST | Claims a `SEEN` gift. Needs the one-time proof from the `?ct=` link; a bare id answers `410`. The giver's own account is refused (`409 GIFT_UNAVAILABLE`) — claiming is another user's act. |
| `/api/claimTokens` | POST | `{passphrase}` in, `{claimUrl}` out — the `/redeem` flow. 30 minutes, 5/min/IP. |
| `/api/invoices` | POST | The payout: `{flow, invoice}`, `flow` = `tippee` (recipient) or `tipper` (reclaimed balance). `204` on success. |

## Public routes worth calling

| Route | Notes |
| --- | --- |
| `GET /api/payments-capability` | `{canReceive, reason, checkedAt, source}`. Fails open. Check before creating a gift someone is about to fund. |
| `GET /api/exchange/rates` | BTC and fiat quotes, for converting a human's figure to sats. |
| `GET /api/stats` | `{totalSatsSent}` — withdrawn gifts, in sats. Cite it rather than a remembered number. |

## Worked examples

Every command below is written with literal values — no shell variables — so it is copy-paste-safe
and trivial to read: the base URL is always `https://lightning.gifts`, the User-Agent is always
`lightning-gifts-skill/1.0`, and `<your-api-key>` is the one value you must supply (from your secret
store, never a file committed to the repo).

```bash
# 1. can this deployment receive money right now?
curl -sS -A "lightning-gifts-skill/1.0" https://lightning.gifts/api/payments-capability

# 2. create: amount is SATS; expiry is future and <=90 days
curl -sS -A "lightning-gifts-skill/1.0" -X POST https://lightning.gifts/api/gifts \
  -H "Authorization: Bearer <your-api-key>" -H "Content-Type: application/json" \
  -d '{"amount":21000,"currency":"USD","expiry":"<future ISO, <=90 days out>",
       "onboardingFlow":"DEFAULT","tippeeLocale":"en","anonymousTipper":false,
       "generatePassphrase":false,"passphraseLength":4}'

# 3. watch the gift flip UNFUNDED -> UNSEEN after you pay the invoice (no confirm endpoint)
curl -sS -A "lightning-gifts-skill/1.0" https://lightning.gifts/api/gifts/<id> \
  -H "Authorization: Bearer <your-api-key>"

# 4. mint the claim link — this is the credential you hand over
curl -sS -A "lightning-gifts-skill/1.0" -X POST https://lightning.gifts/api/gifts/<id>/claimToken \
  -H "Authorization: Bearer <your-api-key>" -H "Content-Type: application/json" -d "{}"

# 5. reclaim, after expiry only, funded gifts only
curl -sS -A "lightning-gifts-skill/1.0" -X POST https://lightning.gifts/api/gifts/<id>/reclaim \
  -H "Authorization: Bearer <your-api-key>"

# 6. pay yourself out of the reclaimed balance (exact total, or 500)
curl -sS -A "lightning-gifts-skill/1.0" -X POST https://lightning.gifts/api/invoices \
  -H "Authorization: Bearer <your-api-key>" -H "Content-Type: application/json" \
  -d '{"flow":"tipper","invoice":"<BOLT11 invoice for the exact total>"}'
```

The API is never called with a key that has been committed anywhere, sent in a URL, echoed into a
log line, or patched together by shell interpolation: `Authorization: Bearer …` travels in a
header, exactly as shown above.

## Error bodies

- `422` carries `{errorMessage, failureCode, maxSats, requestedSats}` — `maxSats` is the ceiling that
  applies, so read it instead of guessing.
- `500` on a money path carries the classified code in its text; see `pitfalls.md`.
- The generated reference at `https://lightning.gifts/api-docs.md` has the full field list and wins
  over this file whenever they disagree.
