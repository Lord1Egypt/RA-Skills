---
name: haggin
description: Run a SaaS seller's price negotiations on HAGGIN (hagg.in) through its API. Use this whenever the user wants to recover a trial that just ended, win back a customer about to churn, answer the offers waiting in their HAGGIN inbox, open a "make an offer" page for a launch or a Black Friday, close a deal (payment link, what happens next, mark as paid), or get HAGGIN events into their own systems with webhooks. Also use it when they mention HAGGIN, a Haggin, hagg.in, or letting customers make an offer on their pricing. The agent reads, interprets and drafts on its own. It never accepts, counters, rejects or publishes without the seller's explicit yes.
version: 1.0.1
metadata:
  openclaw:
    requires:
      env: [HAGGIN_API_KEY]
    primaryEnv: HAGGIN_API_KEY
    envVars:
      - name: HAGGIN_API_KEY
        required: true
        description: A HAGGIN API key (hg_live_...), created at hagg.in/app/settings/api on a Pro or Business plan.
    homepage: https://hagg.in/docs/api
---

# HAGGIN

HAGGIN lets a SaaS company negotiate its prices with its customers. The seller publishes a **Haggin**: a page with its own link where a customer builds a structured offer (price, period, seats, commitment, extras such as a testimonial or a post to their audience). Offers land in the seller's inbox. The seller accepts, counters or passes. When both sides agree, the seller pastes a payment link from its own checkout, the buyer accepts the frozen terms, and the deal is **won**. HAGGIN never touches the money.

Vocabulary, used exactly like this:

- **Haggin**: a negotiation page, public or private, temporary or permanent. Not "campaign".
- **Offer**: one complete proposal, from either side. Immutable. A counteroffer is the next offer in the sequence.
- **Negotiation**: the thread of offers between one buyer and one seller about one product.
- **Deal**: an accepted offer with frozen terms. `agreed` (waiting for the payment link), `payment_ready`, `won` (the buyer accepted the terms).
- **Standard price**: the seller's normal published price. Every offer is read against it.

There is no chat. You cannot send the buyer a message. What you can send is an offer, a counteroffer, a yes, or a no.

## Setup

You need a personal API key. The seller creates it at `https://hagg.in/app/settings/api`. The selling API is part of the Pro and Business plans. Keys come in two kinds: **full access** (does everything) and **read only** (can look, can't touch). A key starts with `hg_live_` and is shown once.

Read the key from the environment (`HAGGIN_API_KEY`) or from wherever the user keeps secrets. If they paste it into the conversation, use it and never repeat it back.

Every request:

```
Base URL:       https://hagg.in/api/v1
Authorization:  Bearer hg_live_...
Content-Type:   application/json    (on writes)
```

JSON in, JSON out, `snake_case`. Money is in minor units: `9900` is 99.00. Times are ISO 8601 in UTC. Ids are UUIDs. One thing comes back under `data`; lists add `pagination`.

Make `GET /me` your first call. `data.selling.enabled` says whether the selling endpoints will answer:

| `selling.reason` | What it means | What to tell the seller |
| --- | --- | --- |
| `mode_not_allowed` | The key was not created for selling. | Create a key at Settings, API keys. |
| `no_organization` | The account has no company yet. | Name the company in the app first. |
| `plan_required` | The company is not on Pro or Business. | The API needs Pro. Keys are kept and start answering again on Pro. |

`GET /me/billing` says whether a Haggin could be published right now (`publish.allowed`, `publish.max_duration_days`, `publish.permanent_allowed`). Check it before you promise to publish anything. It answers for every plan, so on a Free Trial or Campaign account `publish.allowed` can be `true` while the selling endpoints still refuse with `plan_required`. Through the API, only `publish.source: "plan"` means you can publish.

## The rule

**The seller decides. You prepare.**

Do freely, without asking:

- Read anything: Haggins, the inbox, negotiations, deals, deliveries.
- Interpret offers, rank them, explain them.
- Draft: a counteroffer, a private Haggin, a launch page, a reply plan.
- Create and edit Haggin **drafts**. A draft is private and costs nothing.

Do only after the seller says yes to that exact action, with those exact terms:

- Accept, counter, reject or close a negotiation. Bulk reject.
- Publish a Haggin. Close a Haggin.
- Put a payment link on a deal. Send "what happens next" instructions.
- Change or rotate the webhook endpoint.

Why: every one of these emails a real person, spends the seller's allowance, or commits their company to a price. A wrong counteroffer is a real offer the buyer can accept. HAGGIN's own principle is that automation never invents commercial terms on the seller's behalf.

What "yes" means here:

- One yes per negotiation, per action. "Accept anything above 80%" is a policy, not a yes. Apply it to build your proposal, then get the yes for each offer it touches.
- The seller has seen the terms you are about to send: amount, period, seats, commitment, extras, time limit. Show the request body in your proposal. Send exactly that.
- Every number in a counteroffer is the seller's, or one you proposed and they confirmed. Never fill a gap with a guess.
- Mark a deal as paid only when the seller tells you the money landed. It is their bookkeeping.

How to propose, per offer, in one compact block:

```
Ana Ruiz, Bravo Labs (38K on X). Team plan, 10 seats.
Offered: $590/month for 10 seats, 12 months, + testimonial.
Standard: $99/seat/month, so $990. Ratio 0.60. Potential: medium.
Your note on testimonials: "Only if they have an audience". She has one.
Recommend: counter at $9,480/year (790 a month) for 10 seats, annual commitment, 1 year, keep the testimonial.
  {"amount_cents": 948000, "billing_period": "year", "licenses": 10, "annual_commitment": true,
   "price_term_months": 12, "items": [{"party": "buyer", "type": "testimonial"}]}
Say: accept / counter as above / counter at another number / pass.
```

Then stop and wait.

## Reading an offer

An offer is a set of numbers, not a message. The fields, and how to read them:

- `amount_cents`: the **total for the period, for the whole scope**. `59000` with `licenses: 10` and `billing_period: "month"` is 590 a month for ten seats, not per seat.
- `billing_period`: `month`, `year` or `one_time`. `annual_commitment: true` means the buyer commits to a year. `is_lifetime: true` means one payment, forever.
- `licenses`: seats, when the product is `per_seat` or the seller opened that lever.
- `price_term_months`: how long the agreed price holds. `null` means no limit. After it, the regular price applies. A monthly price is limited in months, a yearly one in whole years.
- `items[]`: the extras. `party: "buyer"` is what the buyer gives (a `content` item carries a `format`, `custom` ones carry the seller's own `label`). `party: "seller"` is what the seller adds (an onboarding call, extra seats). `detail` is the buyer's short note on that item.
- `custom_terms`: free text, only if the seller allowed custom offers. It is a note, not the deal.
- `standard_price_cents`: the standard price **per unit, in the product's period, when the offer was made**. The history stays honest even if the seller changes prices later.

**Ratio.** The inbox list gives `interpretation.ratio` and `interpretation.potential` for the current offer. The negotiation detail does not, so for older offers or your own checks compute it the way HAGGIN does:

```
expected = standard_price_cents, moved to the offer's period (month to year: x12, year to month: /12)
           x licenses if the product is per_seat (at least 1; flat products ignore seats)
ratio    = amount_cents / expected
```

Lifetime offers have no ratio. Express them as months at the standard price instead (`amount / monthly standard / seats`).

Buckets: below 0.5, 0.5 to 0.8, above 0.8. Ratio 1 or more is full price or better.

**Potential** (`low`, `medium`, `high`) is HAGGIN's qualitative read of the whole deal, not of the price: ratio, seats (10 and 20 are the steps), annual or lifetime, strategic extras (content, case study, referral, CEO call), a testimonial or one of the seller's own extras, the buyer's biggest audience (5K and 20K are the steps), and whether the buyer named a company.

**The seller's own criteria** live on the Haggin. `GET /selling/haggins/{id}` returns each option with a buyer-facing `hint` and the seller's `internal_notes` ("minimum 8K followers"). Read them once per Haggin and apply them when you read offers. They are the closest thing to the seller's rules.

**The buyer.** `buyer.channels` says where they publish and how big the audience is. `buyer.email` is `null` until a deal is agreed and the buyer consented to share it. HAGGIN carries the messages until then. Don't try to work around it.

Tell the seller the whole picture: what they get paid, for how long, what the buyer gives, and what it is worth against the standard price.

## Playbooks

### Recover the trial that just ended, or win back a customer

One person, one private link. Only the invited email can make an offer on it, the link can't be guessed, and it is not indexed.

1. `GET /me`: `selling.enabled` must be true. Then `GET /me/billing`. If `publish.allowed` is false, or `publish.source` is not `"plan"`, say so and stop: the reason and `upgrade_hint` are in the answer.
2. Ask for what you don't have: the person's name and email, the product and its standard price (with currency, period and whether it is flat or per seat), which levers are open, whether the price should have a time limit, and how long the door stays open.
3. `POST /selling/haggins` with `kind: "private"`, `invited_name`, `invited_email`, one product, the options, `price_term_months` if wanted, `duration_days` and `on_expiry`. It comes back as a `draft`.
4. Show the draft: title, product and price, what can be negotiated, time limit, duration. Ask for the yes to publish.
5. `POST /selling/haggins/{id}/publish`. Then give the seller `public_url`. **HAGGIN does not email the invited person.** The seller sends the link, from their own inbox, in their own words.

Suggested defaults when the seller has no opinion: `duration_days: 14`, `on_expiry: "close"`, `price_term_months: 12` on a monthly product, licenses and annual commitment on, testimonial on with a hint. Say they are defaults.

### Answer this week's offers

1. `GET /selling/negotiations?view=attention&sort=best`. `attention` is what waits on the seller. `best` puts potential first, then ratio, then money.
2. For each Haggin involved, `GET /selling/haggins/{id}` once, for the standard prices, the levers and the internal notes.
3. For each negotiation, `GET /selling/negotiations/{id}` when there is history: `offers[]` is the whole back and forth, oldest first. A buyer who already moved once is worth a different answer than a first offer.
4. Present all of them in one message, best first, each in the block above. Then wait.
5. For each yes, send one write with a fresh `Idempotency-Key`, then report what came back (`status`, and `deal.id` after an accept).

The three answers:

- **Accept**: `POST /selling/negotiations/{id}/accept`. Creates the deal. The buyer gets an email. If the amount is zero, the buyer is sent straight to the terms: the deal starts at `payment_ready`, marked paid, and never emits `deal.payment_ready`.
- **Counter**: `POST /selling/negotiations/{id}/counter` with the same shape as an offer. `amount_cents` and `billing_period` are required; without `billing_period` the request is a `validation_error`. Rules the server applies: `annual_commitment: true` makes the period `year`; `is_lifetime: true` makes it `one_time`; otherwise the period is the product's, whatever you send. `is_lifetime: true` also clears `annual_commitment`. `price_term_months` on a yearly price must be a multiple of 12, and is dropped on lifetime and one-time. The seller may set a time limit, change it or drop it. Add the seller's own items with `party: "seller"`. Extras you ask of the buyer don't have to be switched on for the Haggin. A `custom` item must be one of the Haggin's own extras, by `key`, and is always `party: "buyer"`. A zero amount is fine as long as something else is on the table. A term that isn't whole years on a yearly price, an unknown custom `key` or an item of type `licenses`, `annual_commitment` or `lifetime` come back as `request_rejected`, not `validation_error`. Sending an offer's `items[]` back as the API returned them works: `null` in `format`, `key`, `label` and `detail` is read as absent.
- **Pass**: `POST /selling/negotiations/{id}/reject`, optional `reason` (`too_low`, `not_our_audience`, `spam`). Ends the negotiation. The buyer reads the reason in the email.

`POST /selling/negotiations/{id}/close` walks away from an open negotiation whoever's move it is. Rejecting is for an offer on the table; closing is for a thread the seller wants to end.

A counter is a real offer. If the buyer accepts it, it is a deal. Send only what the seller confirmed.

### Run a launch, a Black Friday, or a permanent "make an offer" page

Same as a private Haggin with `kind: "public"`, several products if needed (up to 5, one currency), an `intro` for the page, `duration_days` (or `null` for permanent, Pro and Business only) and `on_expiry` (`keep_open` lets open negotiations finish after the door closes; `close` ends them and tells the buyers). `allow_custom_offers` lets buyers add free text.

Show the seller `public_url` after publishing. The page carries their company name, their products, their standard prices and what can be negotiated.

Editing: `PUT /selling/haggins/{id}` **replaces** the editable part, products and options included. Read it, change what you need, send the whole thing back. A product that already has offers keeps its name, description, price, currency, period and pricing model, and can't be removed; only its `info_url` can change. Once one product is locked, every product's currency is pinned to it. Every editable field is replaced: leave `price_term_months` out and it resets to `null`, leave `deal_terms` out and the default text comes back. A live Haggin's end date moves with `expires_at` (ISO 8601 in UTC, ending in `Z`). Closed and expired Haggins can't be edited, and publishing one answers `request_rejected`.

Closing early: `POST /selling/haggins/{id}/close`. For good. The slot is free at once. A closed draft is dead too: it can't be edited or published later.

### Close the deal

1. `GET /selling/deals?status=agreed`: deals waiting for a payment link. `buyer.email` is here once the buyer consented to share it. The money is under `accepted_offer` (`amount_cents`, `currency`, `billing_period`), not at the top level.
2. The seller gives you the link from their own checkout (Stripe, Paddle, anything), `https://` only. `PUT /selling/deals/{id}/payment-link` with `{"url": "https://..."}`. The first time, the deal becomes `payment_ready` and the buyer gets an email. A deal with a zero amount has no link: the buyer goes straight to the terms.
3. The deal becomes `won` when the buyer accepts the frozen terms in the app. Watch for it with the `deal.won` webhook, or poll `GET /selling/deals?status=won`.
4. Once won, `POST /selling/deals/{id}/instructions` tells the buyer what happens next (access, onboarding, invoice). Every call sends the email again, with replies going to the person whose key you use. Only when the seller has written or approved the text.
5. `POST /selling/deals/{id}/paid` with `{"paid": true}` when the seller says the money landed. `false` undoes it. Won deals with an amount only; a zero-amount deal is already marked paid.

### Clean the noise

1. Find it: `GET /selling/negotiations?view=attention&max_ratio=0.3`, or `q=` for a name or company, or `item=` for offers where the buyer gives a given extra. `min_licenses`, `min_ratio` and `haggin_id` narrow further. A filter value the API doesn't know answers `validation_error`.
2. List the candidates with the reason each one is noise. Every rejected buyer gets an email, and in bulk it carries no reason, so say so.
3. On the seller's yes, `POST /selling/negotiations/bulk-reject` with `negotiation_ids` (up to 200). The answer is `{rejected, skipped}`. Skipped ones were not waiting on the seller, were not theirs, or don't exist. Duplicate ids are dropped and counted in neither.

A low offer is still information about what people would pay. Suggest a counter before a pass when the buyer looks real.

### Get told when something happens

One endpoint per company. HAGGIN POSTs a signed JSON envelope for each event the endpoint subscribed to.

1. `PUT /selling/webhook-endpoint` with `url` (https, a public hostname, never an IP; one that doesn't resolve or resolves to a private address is refused with `request_rejected`), `enabled` and `events`. An empty `events` list means every event, including ones added later. The answer carries `secret` (`whsec_...`) for full-access keys. Put it in the seller's system; don't paste it around. `POST /selling/webhook-endpoint/rotate-secret` when it leaks: the old one dies at once. There is no delete; `enabled: false` switches it off.
2. `POST /selling/webhook-endpoint/test` queues a `ping` and returns the delivery still `pending`; it is sent right after. `GET /selling/webhook-deliveries` shows what the endpoint answered. `POST /selling/webhook-deliveries/{id}/retry` tries one again now.
3. Verify signatures with any Standard Webhooks library, or by hand: headers `webhook-id`, `webhook-timestamp`, `webhook-signature` (`v1,<base64>`); the signed string is `{id}.{timestamp}.{raw body}`; the HMAC-SHA256 key is the base64-decoded part after `whsec_`; reject timestamps more than five minutes away.
4. Retries: eight attempts over about three days. After 50 consecutive failures the endpoint is paused and the seller gets an email; set it `enabled: true` again to resume.

Events: `haggin.published`, `haggin.closed`, `offer.received`, `offer.countered`, `offer.accepted`, `offer.rejected`, `negotiation.closed`, `deal.payment_ready`, `deal.won`, `deal.paid`. `negotiation.closed` also fires when a negotiation expires. In `data`, the `haggin`, `product`, `buyer`, `offer` and `deal` shapes are the API's; `negotiation` is a shorter summary (`offers_count`, no `offers[]`), see the reference.

No server to receive them? Poll `view=attention` instead. Webhooks tell the seller's systems; they never send anything to buyers.

## Writes done right

- **Idempotency.** Send an `Idempotency-Key` header (a fresh UUID per action) on every write. A retry with the same key and body gets the same answer for at least 24 hours, marked `Idempotent-Replayed: true`, and does nothing twice: no second email, no second offer. A refused request (4xx) is remembered too: fix the body and send it with a new key. The same key with a different method, path or body is refused (`idempotency_key_reused`). `idempotency_in_progress` means the first attempt is still running: wait a moment, retry with the same key; after about two minutes the key is released. After a `500`, the key is released: retry with the same key.
- **Rate limits.** Per key, per minute: 120 requests, 30 of them writes. Every authenticated response carries `X-RateLimit-Limit`, `X-RateLimit-Remaining` and `X-RateLimit-Reset`; on writes they may show the write ceiling of 30. Refused writes count too. A `429` has `Retry-After` in seconds. Wrong keys are limited per address too: 20 failures in five minutes.
- **Pagination.** `limit` (1 to 100, default 50) and `offset`. Lists answer `pagination.total` and `has_more`. The inbox filters and sorts over the 500 most recently active negotiations that match `view`, `haggin_id` and `product_id`: narrow with those first. There, `total` never exceeds 500.
- **Bodies** up to 100 KB. Where a text is empty you get `null`, and you can send `null` back. Everything else is in `references/api.md`: the error table below skips three codes you only get with a broken request (`invalid_json` 400, `invalid_idempotency_key` 400, `body_too_large` 413).
- **Errors** always look the same: `error.code` (stable, branch on it), `error.message` (for people), `error.fields` on validation errors, `error.request_id` (quote it when writing to HAGGIN).

| Code | Status | What to do |
| --- | --- | --- |
| `invalid_api_key` | 401 | The key is missing, malformed or revoked. Ask for a valid one. |
| `insufficient_access` | 403 | A read-only key tried to write. Ask for a full-access key. |
| `plan_required` | 403 | The company is not on Pro or Business. Say so. |
| `no_organization` | 403 | No company on the account. The seller names one in the app. |
| `mode_not_allowed` | 403 | The key can't sell. Create one at Settings, API keys. |
| `no_allowance` | 403 | Nothing left to publish with. `GET /me/billing` says why. |
| `not_found` | 404 | Doesn't exist, or isn't this company's. Same answer for both. |
| `idempotency_in_progress` | 409 | The first request with this key is still running. Wait, retry. |
| `validation_error` | 422 | `fields` says which field and why. Fix the body. |
| `request_rejected` | 422 | Valid, but not allowed right now: not the seller's move, already closed, already won, or a body the Haggin's rules refuse (term not in whole years, unknown extra). The message says. Tell the seller, don't retry. |
| `idempotency_key_reused` | 422 | Same key, different body. Use a fresh key. |
| `rate_limited` | 429 | Wait `Retry-After` seconds. |
| `internal_error` | 500 | HAGGIN's fault. Retry with the same idempotency key. Keep `request_id`. |

## Reference

`references/api.md` has every endpoint with its query parameters, body fields, response shape and limits, verified against the running code. Open it when you need a field you don't see here, or before building a body you haven't sent before. The live spec is at `https://hagg.in/api/v1/openapi.json` and the human reference at `https://hagg.in/docs/api`.
