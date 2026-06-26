# Mai Design Spec

## Goal

Build `mai`, an AI shopping matchmaking agent installable in OpenClaw and Hermes. Mai lets merchants publish products and manage inventory, and lets buyers discover merchants/products, compare prices, discuss with sellers, read reviews, and create orders.

## Chosen Approach

Use a hybrid C approach:

- First version: local-first installable skill with deterministic CLI and JSON store.
- Future path: data model includes a sync outbox and stable schema for a hosted marketplace.
- Transaction path: record order state and external payment references; do not custody funds.

## Package Shape

- `SKILL.md`: agent behavior, safety boundaries, workflows, and CLI usage.
- `scripts/mai.py`: dependency-free deterministic CLI.
- `scripts/verify.sh`: package verification and smoke workflow.
- `scripts/install.sh`: local installer for OpenClaw and Hermes skill directories.
- `tests/test_cli.py`: workflow and status-machine tests.
- `references/transaction-model.md`: transaction and dispute handling rules.
- `references/data-schema.md`: JSON schema and sync contract.
- `README.md`: installation and usage.
- `package.json`, `clawhub.json`, `agents/openai.yaml`: ecosystem metadata.

## Core Workflows

Merchant:

1. Create merchant profile.
2. Publish product with SKU, title, price, stock, category, tags, description, shipping.
3. Adjust stock.
4. Record buyer/merchant discussion.
5. Quote and confirm orders.

Buyer:

1. Discover merchants.
2. Search products by text, price, and city.
3. Compare SKUs by price, stock, reviews, and merchant signal.
4. Read reviews.
5. Discuss with seller.
6. Create and track orders.

## Transaction Model

Happy path:

`draft -> quoted -> confirmed -> payment_pending -> paid_external -> fulfilled -> completed`

Supported dispute path:

`disputed -> resolved/refunded/cancelled`

Rules:

- Confirming an order reserves stock.
- Cancelling or refunding releases reserved stock.
- Mai stores external `payment_url` and `payment_reference` only.
- The agent must not claim escrow, direct payment execution, or refund completion without external evidence.

## Data Model

Top-level store:

- `merchants`: merchant profiles keyed by id.
- `products`: products keyed by SKU.
- `orders`: order records keyed by order id.
- `messages`: buyer/merchant discussion records.
- `reviews`: buyer reviews.
- `inventory_events`: stock movement records.
- `sync.pending_events`: local-first outbox for future hosted marketplace integration.

## Registry Extension

The hosted marketplace extension adds `scripts/mai_registry.py`, a dependency-free HTTP JSON service. Merchants push local stores to the registry; buyers search the registry and create messages or draft orders; merchants pull registry inbox data back into local `messages` and `orders`.

Registry endpoints:

- `GET /health`
- `POST /sync/push`
- `GET /search/products`
- `GET /search/merchants`
- `POST /messages`
- `POST /orders`
- `GET /merchants/{merchant_id}/inbox`

Public marketplace controls:

- API keys are stored as salted hashes.
- Merchant keys are scoped to one merchant id.
- Buyer keys are scoped to one buyer id.
- Admin keys are required for moderation and payment release/refund.
- Public search is rate-limited by IP.
- Authenticated requests are rate-limited by API key.
- Risky products are hidden as `pending_review` until admin approval.
- Payment custody uses PSP-backed state records; the built-in `demo` provider is for development only.
- Deployment assets include `Dockerfile`, `docker-compose.yml`, and `registry.example.env`; public traffic should run behind HTTPS.

## Acceptance Criteria

- OpenClaw/Hermes can discover the package as a skill through `SKILL.md` and metadata.
- Users can install the same package into OpenClaw and Hermes with `bash scripts/install.sh --both`.
- Merchants can publish products and adjust inventory.
- Buyers can search products, discover merchants, compare prices, read reviews, discuss, and create orders.
- Orders enforce allowed status transitions.
- Confirmed orders reserve stock and insufficient stock blocks confirmation.
- External payment references can be recorded without pretending Mai is a payment processor.
- Registry-backed discovery lets separate buyer and merchant agents find each other through pushed merchant/product supply and pulled buyer demand.
- Public marketplace controls cover authentication, authorization, rate limiting, risk scoring, moderation, and PSP-backed custody records.
- `bash scripts/verify.sh` validates CLI, tests, metadata consistency, and a full shopping workflow.
