# HAGGIN selling API, endpoint by endpoint

Base URL `https://hagg.in/api/v1`. Header `Authorization: Bearer hg_live_...` on every call. Checked against the route handlers and validation schemas of the running code (September 2026). The live spec is `https://hagg.in/api/v1/openapi.json`.

Contents:

1. Conventions
2. Shapes (what comes back)
3. Account: `/me`, `/me/profile`, `/me/billing`, `/selling/organization`
4. Haggins: `/selling/haggins`
5. Negotiations: `/selling/negotiations`
6. Deals: `/selling/deals`
7. Webhooks: `/selling/webhook-endpoint`, `/selling/webhook-deliveries`
8. Webhook payloads
9. Errors

## 1. Conventions

- **Access.** `read` endpoints work with any key. `write` endpoints need a full-access key. Everything under `/selling` needs a company on Pro or Business; `/me` works for any key.
- **Bodies** are JSON, `snake_case`, up to 100 KB. Unknown keys are ignored. Optional texts accept `null` as "leave it empty", inside `items[]` too.
- **Responses**: `{ "data": ... }`. Lists: `{ "data": [...], "pagination": { "limit", "offset", "total", "has_more" } }`. Some `data` can be `null` (noted below).
- **Pagination**: `limit` 1 to 100 (default 50), `offset` from 0 (up to 1,000,000).
- **Ids** are UUIDs. A path id that is not a UUID answers `404`.
- **Idempotency**: `Idempotency-Key` header on writes, up to 255 characters, remembered at least 24 hours per key. Replays carry `Idempotent-Replayed: true`. A refused request (4xx) is replayed too: fix the body and use a new key. A key still in progress is released after about two minutes.
- **Rate limits** per key per minute: 120 requests, 30 writes. Headers `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` (unix seconds) on every authenticated response; on writes they can show the write ceiling (30). Refused writes count too. `429` carries `Retry-After` (seconds).
- Every response carries `X-Request-Id`.
- Enum values used throughout:
  - `currency`: `USD`, `EUR`, `GBP`
  - `billing_period`: `month`, `year`, `one_time`
  - `pricing_model`: `flat`, `per_seat`
  - option and item `type`: `licenses`, `annual_commitment`, `lifetime`, `content`, `testimonial`, `ceo_call`, `referral`, `case_study`, `custom`
  - content `format`: `x_post`, `linkedin_post`, `instagram`, `tiktok`, `youtube`, `blog_post`, `newsletter`, `podcast`, `other`
  - Haggin `status`: `draft`, `live`, `closed`, `expired`; `kind`: `public`, `private`; `on_expiry`: `keep_open`, `close`
  - negotiation `status`: `waiting_for_seller`, `waiting_for_buyer`, `accepted`, `rejected`, `closed`, `expired`
  - offer `status`: `pending`, `countered`, `accepted`, `rejected`, `withdrawn`, `expired`; `author`: `buyer`, `seller`
  - deal `status`: `agreed`, `payment_ready`, `won`; `payment_status`: `pending`, `paid`. A zero-amount deal starts at `payment_ready`, `payment_status: "paid"`, `paid_at` set, and never emits `deal.payment_ready`.
  - seller close `reason`: `too_low`, `not_our_audience`, `spam`

## 2. Shapes

**Product**: `id`, `name`, `standard_price_cents`, `currency`, `billing_period`, `pricing_model`. On a Haggin detail also `description`, `info_url`, `negotiation_count` (above zero, the product is locked).

**Option** (on a Haggin detail): `type`, `key` (custom only), `label` (custom only), `enabled`, `hint` (buyer-facing), `internal_notes` (seller only), `config: { formats: [] }` (content only; empty means all formats).

**Offer**: `id`, `seq` (1 is the first), `author`, `status`, `amount_cents`, `currency`, `billing_period`, `licenses` (nullable), `is_lifetime`, `annual_commitment`, `price_term_months` (nullable), `custom_terms` (nullable), `standard_price_cents` (the standard price per unit when the offer was made), `created_at`, `items[]` each `{ party, type, format, key, label, detail }`.

**Buyer**: `id`, `name`, `company`, `role`, `website`, `channels[]` each `{ format, handle, audience }`. On negotiation details and deals also `email`, which is `null` until a deal is agreed and the buyer consented to share it. The inbox list never carries `email`.

**Haggin summary** (inside a negotiation): `id`, `title`, `slug`, `status`, `kind`, `price_term_months`, `public_url`, `published_at`, `expires_at` (`null` means permanent), `closed_at`.

**Haggin, seller view** (list and detail): the summary plus `intro`, `invited_name`, `invited_email`, `duration_days`, `on_expiry`, `created_at`, `updated_at`, `url` (the app page). The list adds `products[]` and `negotiations: { total, open, won }` (confirmed negotiations only; `won` counts negotiations that ended in a deal, whatever the deal's status). `products[].negotiation_count` counts confirmed negotiations too. The detail adds `goal`, `business_context`, `allow_custom_offers`, `deal_terms`, `max_duration_days`, `products[]` (extended), `options[]`.

**Negotiation core**: `id`, `status`, `url`, `closed_by` (`buyer`, `seller`, `system` or null), `close_reason` (`rejected`, `closed_by_seller`, `withdrawn_by_buyer`, `haggin_closed`, `haggin_expired`, `expired`), `close_detail` (the seller's `too_low`, `not_our_audience`, `spam` or the buyer's `too_expensive`, `found_alternative`, `just_looking`), `expires_at`, `created_at`, `last_activity_at`, `closed_at`.

**Negotiation, list item**: the core plus `haggin: { id, title, slug, kind, status }`, `product`, `buyer` (no email), `offer` (the current one), `interpretation: { ratio, potential }` (`ratio` is `null` when not comparable, such as lifetime), `deal` (summary or null).

**Negotiation, detail**: the core plus `haggin` (summary), `product`, `buyer` (with `email` rule), `offer` (current, nullable), `offers[]` (every offer, oldest first), `deal` (summary or null). No `interpretation` on the detail: compute the ratio yourself (see SKILL.md).

**Deal summary**: `id`, `status`, `payment_status`, `payment_link_url`, `terms_version`, `agreed_at`, `won_at`, `paid_at`, `url`.

**Deal, list item**: the summary plus `negotiation_id`, `haggin: { id, title, slug }`, `product`, `buyer`, `accepted_offer`.

**Deal, detail**: the summary plus `negotiation_id`, `payment_provider` (`manual_link` today), `payment_link_added_at`, `terms_text` (the frozen terms), `instructions`, `instructions_sent_at`, `product`, `buyer`, `accepted_offer`, `terms_acceptance: { accepted_at, terms_version }` or null.

**Webhook endpoint**: `id`, `url`, `enabled`, `events[]` (empty means all), `secret` (`null` for read-only keys), `disabled_reason` (`too_many_failures` or null), `consecutive_failures`, `last_delivery_at`, `last_delivery_status`, `created_at`, `updated_at`.

**Webhook delivery**: `id`, `event_type`, `status` (`pending`, `delivered`, `failed`, `exhausted`), `attempts`, `next_attempt_at`, `last_attempt_at`, `response_status`, `response_body` (first 1 KB), `error`, `delivered_at`, `created_at`, `payload` (the envelope that was sent).

**Entitlements** (`/me/billing` and inside `/me`): `plan` (`free_trial`, `campaign`, `pro`, `business`), `plan_source` (`subscription`, `grant`, `none`), `plan_expires_at`, `subscription_status`, `max_live_haggins` (`null` is unlimited), `live_haggins`, `available_slots`, `trial_remaining`, `unused_campaign_purchases`, `publish`: either `{ allowed: true, source: "plan" | "campaign_purchase" | "trial", max_duration_days, permanent_allowed }` or `{ allowed: false, reason, upgrade_hint }`.

## 3. Account

### GET /me (read, any key)

Who the key belongs to and what it can do right now. Response: `{ user: Profile, key: { id, access: "read" | "full", modes: ["selling"] }, selling: { enabled: true, organization (null until the company exists), entitlements } | { enabled: false, reason: "mode_not_allowed" | "no_organization" | "plan_required", message } }`.

### PUT /me/profile (write, any key)

What the other side sees about the person behind the key. Replaces the whole profile. Body: `name` (required, up to 120), `company` (up to 120), `role` (up to 80), `website` (a URL up to 200, `https://` added if missing), `channels[]` (up to 9) each `{ format, handle (up to 120), audience (integer or null) }`, stored as sent. Response: Profile (`id`, `email`, `name`, `company`, `role`, `website`, `channels`).

### GET /me/billing (read, any key)

The plan of the company the key sells as, and whether a Haggin could be published right now. Response: Entitlements, or `data: null` while there is no company. Read only: paying and changing plan happen in the app.

### GET /selling/organization (read)

Response: `{ id, name, slug, website, created_at }`.

### PUT /selling/organization (write)

Replaces both fields. Body: `name` (2 to 80), `website` (up to 200, `https://` added if missing; leave it out and it is cleared). Response: the organization.

## 4. Haggins

### GET /selling/haggins (read, paginated)

Newest first. Query: `status` (`draft`, `live`, `closed`, `expired`), `kind` (`public`, `private`), `limit`, `offset`. Response items: Haggin, seller view, list item.

### POST /selling/haggins (write) → 201

Creates a draft. Nothing is public and nothing is spent until publish. Body:

| Field | Required | Notes |
| --- | --- | --- |
| `title` | yes | 2 to 80 characters. |
| `kind` | yes | `public` or `private`. |
| `invited_name` | private | Up to 120. |
| `invited_email` | private, required | Only this address can make an offer. Both `invited_*` are dropped on a public Haggin. |
| `intro` | no | Up to 280. Shown on the page. |
| `goal` | no | `get_customers`, `convert_trials`, `recover_churn`, `test_pricing`, `run_launch`, `other`. |
| `business_context` | no | `launching`, `low_conversion`, `losing_on_price`, `many_customers`, `experimenting`, `other`. |
| `products[]` | yes, 1 to 5 | Each: `name` (1 to 80), `standard_price_cents` (1 to 10,000,000,000), `currency`, `billing_period`, `pricing_model`, optional `description` (up to 2000), `info_url` (http or https, up to 2048). All products share one currency. |
| `options[]` | yes (can be empty) | Each: `type`, `enabled`, optional `hint` (up to 280), `internal_notes` (up to 500), `config: { formats: [] }` for `content`. Built-in types once each. `custom` needs `key` (6 to 24 lowercase letters and digits, made up by you, stable for the life of the extra) and `label` (up to 40); up to 5 custom extras, no repeated `key` or `label`. |
| `allow_custom_offers` | yes | Free text on offers. |
| `price_term_months` | no | 1 to 120, or `null` (default). The starting time limit on agreed prices. |
| `duration_days` | yes | 1 to 365, or `null` for permanent (Pro and Business). Capped at publish by the plan's `max_duration_days`; on a capped plan `null` becomes the cap, it is not refused. |
| `on_expiry` | yes | `keep_open` or `close`. |
| `deal_terms` | no | Up to 4000. HAGGIN's default terms apply when empty. |

Response: Haggin, seller view, detail.

Example, a private one:

```json
{
  "title": "Acme, let's talk",
  "kind": "private",
  "invited_name": "Ana",
  "invited_email": "ana@bravolabs.com",
  "products": [{ "name": "Team plan", "standard_price_cents": 9900, "currency": "USD", "billing_period": "month", "pricing_model": "per_seat" }],
  "options": [
    { "type": "licenses", "enabled": true },
    { "type": "annual_commitment", "enabled": true },
    { "type": "testimonial", "enabled": true, "internal_notes": "Only if they have an audience" }
  ],
  "allow_custom_offers": true,
  "price_term_months": 12,
  "duration_days": 14,
  "on_expiry": "close"
}
```

### GET /selling/haggins/{id} (read)

Response: Haggin, seller view, detail. What comes back can be sent to PUT as it is.

### PUT /selling/haggins/{id} (write)

Replaces the editable part. Body: `title`, `intro`, `products[]` (the full list after the edit; existing ones carry their `id`, new ones don't, missing ones are removed), `options[]` (the full list; what you leave out is gone, `internal_notes` included), `allow_custom_offers`, `price_term_months`, `on_expiry`, `deal_terms`, and `expires_at` (ISO 8601 in UTC ending in `Z`, or `null`; only applied on a live Haggin, must be in the future and within `max_duration_days` from publish when there is one). Every field listed is replaced: leave `price_term_months` out and it resets to `null`, leave `intro` out and it is cleared, leave `deal_terms` out and the default text returns. `kind`, `invited_*`, `duration_days`, `goal` and `business_context` can't change here. A product with `negotiation_count` above zero keeps its name, description, price, currency, period and pricing model whatever you send, only `info_url` changes, and it can't be removed; once one product is locked, every product's currency is pinned to it. A `products[].id` that isn't this Haggin's answers `not_found`. Closed and expired Haggins answer `request_rejected`. Response: the detail.

### POST /selling/haggins/{id}/publish (write, emails the seller's team)

Goes live and spends a slot (Pro, Business) or an allowance (trial, Campaign). Only from `draft`; live, closed and expired answer `request_rejected`. `duration_days` is capped by the plan; `expires_at` is set from it. Refused with `no_allowance` when nothing is left; `GET /me/billing` says why beforehand. Response: the detail. Nobody outside the seller's team is emailed: for a private Haggin, the seller sends the link.

### POST /selling/haggins/{id}/close (write, emails the seller's team)

Ends it for good, from `live` or `draft`; the slot is free at once, and a closed draft can't be edited or published later. With `on_expiry: "close"` every open negotiation is closed too (`closed_by: "system"`, `close_reason: "haggin_closed"`, a `negotiation.closed` event each) and each buyer is emailed. Already closed answers `request_rejected`. Response: the detail.

## 5. Negotiations

### GET /selling/negotiations (read, paginated)

The inbox, selling side. Query:

| Param | Values | Notes |
| --- | --- | --- |
| `view` | `attention`, `open`, `waiting`, `accepted`, `closed`, `all` | Default `all`. `attention` is waiting on the seller; `waiting` is waiting on the buyer; `closed` covers rejected, closed and expired. |
| `sort` | `best`, `newest`, `oldest`, `highest`, `ratio`, `licenses`, `potential`, `activity` | Default `activity`. `best` is potential, then ratio, then money normalised to the product's period. |
| `haggin_id` | UUID | One Haggin. |
| `product_id` | UUID | One of that Haggin's products. |
| `min_ratio`, `max_ratio` | number | Offer divided by standard price. `max_ratio=0.3` is below 30%. Offers without a ratio (lifetime) are excluded by either. |
| `min_licenses` | integer | At least this many seats. |
| `item` | `content`, `testimonial`, `ceo_call`, `referral`, `case_study`, `licenses`, `annual_commitment`, `lifetime` | Offers where the buyer gives it. `annual_commitment` also matches yearly offers. |
| `format` | a content format | Only with `item=content`: that format. |
| `q` | text | Buyer name, buyer company, Haggin title or product name contains it. |
| `limit`, `offset` | | |

Filtering and sorting run over the 500 most recently active negotiations that match `view`, `haggin_id` and `product_id`; `pagination.total` never exceeds 500. A filter value the API doesn't know, or a `haggin_id`/`product_id` that isn't a UUID, answers `validation_error`. Response items: negotiation list items (no buyer email).

### GET /selling/negotiations/{id} (read)

Response: negotiation detail, with `offers[]`.

### POST /selling/negotiations/{id}/accept (write, emails the buyer)

Accepts the current offer. Only when `status` is `waiting_for_seller` and the current offer is the buyer's and pending; otherwise `request_rejected`. Creates the deal (`deal` in the response). The buyer is emailed: for a zero amount, straight to the terms (the deal starts at `payment_ready`, marked paid); otherwise told to wait for the payment link. Response: negotiation detail.

### POST /selling/negotiations/{id}/counter (write, emails the buyer)

Only when `waiting_for_seller`. Body, same shape as an offer:

| Field | Notes |
| --- | --- |
| `amount_cents` | Required. Integer, 0 or more. Zero only with items or custom terms. |
| `billing_period` | Required by the schema (`validation_error` without it), then normalised: `is_lifetime` forces `one_time` and clears `annual_commitment`, `annual_commitment` forces `year`, otherwise the product's own period is used. |
| `licenses` | Integer 1 to 100000, or null. |
| `is_lifetime` | Default false. |
| `annual_commitment` | Default false. |
| `price_term_months` | 1 to 120 or null. Dropped on lifetime and one-time. On a yearly price, a multiple of 12 (`request_rejected` otherwise). The seller can set it, change it or drop it. |
| `custom_terms` | Up to 1000. |
| `items[]` | Up to 20. Each `{ party: "buyer" | "seller" (default buyer), type, format (content only), key (custom only), detail (up to 200) }`. Types allowed: `content`, `testimonial`, `ceo_call`, `referral`, `case_study`, `custom`; any other type, a `custom` item with `party: "seller"` or an unknown `key` answers `request_rejected`. Extras asked of the buyer don't have to be enabled on the Haggin. A `custom` item must match one of the Haggin's own extras by `key` and is always `party: "buyer"`; its `label` is filled by the server. `null` in `format`, `key`, `label` or `detail` is read as absent, so an offer's items can be sent back as returned. Duplicates by party and type (and format or key) are collapsed. |

The response is the negotiation detail, now `waiting_for_buyer`, with the new offer last in `offers[]`. Example:

```json
{ "amount_cents": 79000, "billing_period": "month", "licenses": 10, "annual_commitment": true, "price_term_months": 12, "items": [{ "party": "buyer", "type": "testimonial" }] }
```

Read by the server as 790.00 a year for 10 seats, annual commitment, for 12 months, plus a testimonial. Note the period: `annual_commitment` made it `year`.

### POST /selling/negotiations/{id}/reject (write, emails the buyer)

Turns down the current offer and ends the negotiation. Only when `waiting_for_seller`. Body: `{ "reason": "too_low" | "not_our_audience" | "spam" | null }`. The buyer reads the reason. Response: negotiation detail (`rejected`).

### POST /selling/negotiations/{id}/close (write, emails the buyer)

Walks away from an open negotiation, whoever's move it is. Body: `{ "reason": ... | null }`, same values. Already closed answers `request_rejected`. Response: negotiation detail (`closed`).

### POST /selling/negotiations/bulk-reject (write, emails each buyer)

Body: `{ "negotiation_ids": [uuid, ...] }`, 1 to 200. Each one goes through the same rule as reject, with no reason attached; the ones that fail (not yours, not waiting on you, or nonexistent) are skipped, not failed. Duplicate ids are dropped and counted in neither. Response: `{ "rejected": n, "skipped": n }`.

## 6. Deals

### GET /selling/deals (read, paginated)

Newest first by agreement date. Query: `status` (`agreed`, `payment_ready`, `won`), `limit`, `offset`. Response items: deal list items, with `buyer.email` when consented. The money lives under `accepted_offer`.

### GET /selling/deals/{id} (read)

Response: deal detail, with `terms_text`.

### PUT /selling/deals/{id}/payment-link (write, emails the buyer the first time)

Body: `{ "url": "https://..." }`, up to 2048 characters, `https://` only. From `agreed` the deal becomes `payment_ready` and the buyer is emailed. On `payment_ready` the link is replaced silently. Refused on `won` deals and on zero-amount deals (`request_rejected`). Response: deal detail.

### POST /selling/deals/{id}/instructions (write, emails the buyer every time)

Body: `{ "instructions": "..." }`, 1 to 2000 characters. Only on `won` deals ("Wait until they accept the terms" otherwise). Overwrites the previous note; each call sends the email again with replies going to the key's owner. Response: deal detail.

### POST /selling/deals/{id}/paid (write)

Body: `{ "paid": true | false }`. Only on `won` deals with an amount. `true` sets `payment_status: "paid"` and `paid_at`, and emits `deal.paid`; `false` undoes it. Response: deal detail.

## 7. Webhooks

### GET /selling/webhook-endpoint (read)

Response: the endpoint, or `data: null` when none is set. `secret` is `null` for read-only keys.

### PUT /selling/webhook-endpoint (write)

Creates or replaces the one endpoint. Body: `url` (required; `https://`, a public hostname with a dot, no credentials, no IP literal, no private or local address), `enabled` (default true), `events[]` (default `[]`, which means every event; otherwise exactly those). Response: the endpoint with `secret` (`whsec_` plus base64). Rejected URL shapes come back as `validation_error`; a hostname that doesn't resolve, or resolves to a private address, as `request_rejected`. The hostname is resolved again on every delivery and the connection pinned to that address. There is no delete: send `enabled: false`.

### POST /selling/webhook-endpoint/rotate-secret (write)

New secret in the response. The old one stops validating at once. `404` when there is no endpoint.

### POST /selling/webhook-endpoint/test (write)

Queues a `ping` and returns the delivery still `pending` (`attempts: 0`); it is sent right after the response, so check `GET /selling/webhook-deliveries` for the outcome. `404` without an endpoint; `request_rejected` when the endpoint is disabled.

### GET /selling/webhook-deliveries (read, paginated)

The latest 50 deliveries, newest first, with `payload`, `response_status`, `response_body` and `error`. Deliveries older than 30 days are pruned.

### POST /selling/webhook-deliveries/{id}/retry (write)

Tries one delivery again, now, whatever its state. Response: `{ "result": "delivered" | "failed" | "exhausted" | "skipped" }`. `request_rejected` when the endpoint is disabled.

## 8. Webhook payloads

Each delivery is a POST with `Content-Type: application/json`, `User-Agent: HAGGIN-Webhooks/1.0` and the Standard Webhooks headers:

```
webhook-id:         <delivery id, also the envelope id>
webhook-timestamp:  <unix seconds>
webhook-signature:  v1,<base64 HMAC-SHA256 of "{id}.{timestamp}.{raw body}" keyed with the base64-decoded secret after "whsec_">
```

Verify with a five-minute tolerance and a constant-time comparison. Redirects are not followed; answer 2xx from the exact URL configured. Ten seconds to answer.

Envelope: `{ "id", "type", "created_at", "data" }`.

- `ping`: `data: { organization: { id, name } }`.
- `haggin.published`, `haggin.closed`: `data: { haggin: HagginSummary }`.
- `offer.received`, `offer.countered`, `offer.accepted`, `offer.rejected`, `negotiation.closed`, `deal.payment_ready`, `deal.won`, `deal.paid`: `data: { haggin: HagginSummary, negotiation: { id, status, url, closed_by, close_reason, created_at, last_activity_at }, product, buyer (email rule applies), offer (current), offers_count, deal (summary or null) }`.

`offer.received` fires once the buyer's address is confirmed. `offer.countered` fires for either side. `offer.rejected` only for the seller's rejection. `negotiation.closed` covers a walk away by either side, closures by an ending Haggin, and negotiations that expire.

Retries: attempt 1 at once, then after 1, 2, 4, 8, 16, 24 and 24 hours (8 attempts). After 50 consecutive failures the endpoint is disabled with `disabled_reason: "too_many_failures"` and the team is emailed; re-enable it with `PUT`.

## 9. Errors

`{ "error": { "code", "message", "fields"?, "request_id" } }`.

| Status | Code | Meaning |
| --- | --- | --- |
| 400 | `invalid_json` | The body is not JSON. |
| 400 | `invalid_idempotency_key` | The header is longer than 255 characters. |
| 401 | `invalid_api_key` | No key, a malformed one, or a revoked one. Same answer for all three. |
| 403 | `insufficient_access` | A read-only key tried to write. |
| 403 | `plan_required` | Selling through the API is part of Pro and Business. |
| 403 | `no_organization` | The account has no company yet. |
| 403 | `mode_not_allowed` | The key was not created for selling. |
| 403 | `no_allowance` | No slot or allowance left to publish with. |
| 404 | `not_found` | Doesn't exist, isn't yours, or the id is not a UUID. |
| 409 | `idempotency_in_progress` | The first request with this key is still running. |
| 413 | `body_too_large` | Over 100 KB. |
| 422 | `validation_error` | `fields` maps each bad field (snake_case path) to its messages. |
| 422 | `request_rejected` | Valid, but not allowed in the current state, or refused by the Haggin's rules (term not in whole years, unknown extra). The message says why. |
| 422 | `idempotency_key_reused` | Same key, different method, path or body. |
| 429 | `rate_limited` | `Retry-After` says when. Also for 20 failed authentications from one address in five minutes. |
| 500 | `internal_error` | Safe to retry. Send HAGGIN the `request_id`. |
