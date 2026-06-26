---
name: book-tickets
description: >-
  Buy tickets for a bookable real-world activity through Outgoing. Use after
  discovering an activity (one with is_bookable true and ticket pricing) when the
  user wants to purchase tickets or complete a booking ("book 2 tickets to that
  show", "get us seats for Friday", "buy the General Admission passes").
  Bookings are async and resolve via webhook. Powered by Outgoing, which works
  in cities worldwide.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🎫"
    homepage: https://www.outgoing.world/developers
    primaryEnv: OUTGOING_API_KEY
    requires:
      env:
        - OUTGOING_API_KEY
      anyBins:
        - curl
    envVars:
      - name: OUTGOING_API_KEY
        required: true
        description: >-
          Outgoing API key with the partner scope (og_api_…). Request one at https://outgoing.world.
---

# Book tickets — powered by Outgoing

Purchase tickets for a bookable activity. Bookings are **asynchronous**: you
`POST` a request, get a `202 Accepted` with a `booking_id`, and the outcome
(confirmed / failed) arrives at your **webhook** — there is no polling endpoint.

This is the **second step**. Discover the activity first with one of the
Outgoing discovery skills (date-night, kids-weekend, stay-active, … or the
general **outgoing**) — you need its `activity_id` and exact ticket type/session
from `ticket_price`. Only activities with **`is_bookable: true`** can be booked.

Full reference (every field, schemas, `GET /partner/v1/orders`) as plain
Markdown: <https://www.outgoing.world/llms.txt> and
<https://www.outgoing.world/llms-full.txt>.

## Prerequisites

```bash
export OUTGOING_API_KEY="og_api_…"   # partner scope — get one at https://outgoing.world
```

- `Authorization: Bearer $OUTGOING_API_KEY` and `X-External-User-Id: <user>` on
  every call; the user must be provisioned (`POST /partner/v1/users`) first.
- A **webhook URL** you control (HTTPS in production) to receive the result.
- A **payment token** pre-authorizing the charge. For testing use
  `DRYRUN_SUCCESS` or `DRYRUN_FAIL` — no card is charged.

> **Test first.** Always validate the flow with `DRYRUN_SUCCESS`/`DRYRUN_FAIL`
> before using a real `payment_token` — a real token triggers an actual purchase.

## Create a booking — `POST /partner/v1/bookings`

```bash
curl -sS -X POST https://api.outgoing.world/partner/v1/bookings \
  -H "Authorization: Bearer $OUTGOING_API_KEY" \
  -H "X-External-User-Id: user-123" \
  -H "Content-Type: application/json" \
  -d '{
    "external_user_id": "user-123",
    "activity_id": "550e8400-e29b-41d4-a716-446655440000",
    "tickets": [
      { "ticket_type_name": "General Admission", "num_tickets": 2,
        "session_date": "2026-04-25", "session_time": "19:00" }
    ],
    "authorization_amount_cents": 3000,
    "idempotency_key": "01929f3b-7c2a-7000-8d3f-1b2c3d4e5f60",
    "webhook_url": "https://partner.example.com/webhooks/outgoing-booking",
    "payment_token": "DRYRUN_SUCCESS"
  }'
```

| Field | Required | Notes |
|-------|----------|-------|
| `activity_id` | yes | From discovery; must be `is_bookable: true`. |
| `tickets[]` | yes (≥1) | `ticket_type_name` (exact, from `ticket_price.sessions[].tickets[].name`), `num_tickets`, and `session_date`/`session_time` for multi-session events. |
| `authorization_amount_cents` | yes | Pre-authorized **total** in USD cents; treated as a max ceiling. |
| `idempotency_key` | yes | Unique per attempt; replaying returns the original `booking_id` (no duplicate). |
| `webhook_url` | yes | HTTPS in prod; receives the result payload. |
| `payment_token` | yes | Real token, or `DRYRUN_SUCCESS` / `DRYRUN_FAIL`. |

Returns `202 { booking_id, idempotency_key, status: "accepted" }` — processing
continues in the background.

## Webhook result

Outgoing `POST`s your `webhook_url` when the booking resolves (retried up to 3×).
`status` is one of `confirmed`, `failed`, `cancelled`, `pending`,
`user_input_required`, `deliverable_ready`. On `confirmed` you also get
`purchase_amount_cents`, `booking_fee_cents`, `total_charged_cents`, and
`ticket_details` (`confirmation_code`, `download_urls`, `notes`). On `failed`,
`error_message`. You can also list past bookings via `GET /partner/v1/orders`.

## Workflow

1. Get the activity (discovery skill). Confirm `is_bookable: true`; read
   `ticket_price` (currency, sessions, ticket names).
2. **Confirm the order and total cost with the user before submitting** — a real
   `payment_token` results in a real charge.
3. Generate a fresh `idempotency_key` (UUID) per intended booking; reuse the same
   key only when retrying the *same* booking.
4. POST the booking (DRYRUN first when validating).
5. Tell the user it's submitted; resolve via webhook (or `GET /orders`). On
   `confirmed`, share the `confirmation_code`, `download_urls`, and
   `total_charged_cents`. On `failed`, relay `error_message` and offer a retry
   with a new key.

## Errors

`400` validation (ticket/session mismatch — message lists valid options; sold
out; non-HTTPS webhook). `401` bad key/scope. `402` invalid/expired
`payment_token`. `404` user not provisioned or activity not found. `429` rate
limit. Relay `{ "error": "…" }` messages; never fabricate a result.

> Need something to book? Find it first with the **outgoing** skill (or any of
> its plan-specific companions).
