---
name: build-flow
description: >
  Build email/SMS automation flows with triggers, steps, waits, splits, and
  webhooks. Covers welcome series, cart abandonment, post-purchase, win-back,
  browse abandonment, and custom event-driven flows. Use when: "automation
  flow", "welcome series", "drip campaign", "cart abandonment flow",
  "win-back flow", "build flow", or "email sequence".
---

# Build Flow

Help the user design and create automation flows using Nitrosend.

## Understand the Goal

Ask what kind of flow they need. Common patterns:

| Flow Type | Trigger Event | Typical Steps |
|-----------|--------------|---------------|
| **Welcome series** | `contact_add` | Email 1 (immediate) -> Wait 1d -> Email 2 -> Wait 2d -> Email 3 |
| **Cart abandonment** | `cart_abandoned` | Wait 1h -> Email 1 -> Wait 1d -> Email 2 (with discount) |
| **Post-purchase** | `checkout` or custom | Email 1 (thank you) -> Wait 3d -> Email 2 (review request) |
| **Win-back** | Custom event or segment | Email 1 -> Wait 3d -> Split (opened?) -> Yes: Email 2 / No: Email 3 |
| **Browse abandonment** | `browse_abandoned` | Wait 2h -> Email with viewed products |
| **Onboarding** | `contact_add` or custom | Welcome -> Wait 1d -> Getting started -> Wait 2d -> Feature highlight |
| **Re-engagement** | Custom trigger | Email 1 -> Wait 7d -> Split (engaged?) -> Yes: normal cadence / No: final offer |

## Design the Flow

### Available Step Types

| Step | Required Props | Notes |
|------|---------------|-------|
| `email` | `subject` + (`design` or `body`) | Design uses `{sections, theme}` |
| `sms` | `body` | SMS text content |
| `wait` | `duration` (seconds) | 3600=1hr, 86400=1day, 604800=1week |
| `split` | `filters`, `yes` steps, `no` steps | Conditional branching; splits may nest inside `yes`/`no` branches |
| `emit_event` | `event_name` | Fire event to trigger other flows |
| `webhook` | `url` | POST or PUT to external URL |
| `subscribe` | `channel` (phone/email/all) | Opt contact in |
| `unsubscribe` | `channel` (phone/email/all) | Opt contact out |

### Split Filters

Use the filter schema returned by the intent response or `nitro://schema`; do
not assume this document is an exhaustive registry. Common current filters
include contact identity and subscription fields, tags and lists, creation and
interaction timestamps, delivery/engagement metrics such as
`contact_last_opened_at` and `contact_last_clicked_at`, event history, and
custom or enrichment fields. Use only names and predicates accepted by the live
schema.

Prefer behavior-based branches when the necessary evidence exists. Keep waits
and message frequency proportionate to the user's audience and test the cadence
against account performance rather than asserting universal timings.

## Create the Flow

Use `nitro_compose_flow` with:
- `name`: Descriptive flow name
- `trigger`: `{ event: "trigger_event_name" }` — optionally add `segment_id` or `contact_list_id`
- `steps`: Array of step objects

Offer `dry_run: true` first to preview the flow graph.

**Composition contract**: any newly authored email step enters the contract
before persistence. Call `nitro_compose_flow` with `composition_mode: "intent"`.
Treat `next_call.input` as the selected complete baseline for the flow and its
email steps; preserve and fill it by default. Use the compact
`composition_contract.creative_routes` menu and start a fresh intent with
`creative_route_id` to select another ready route (that top-level field applies
one route to the whole sequence; to assign routes per email in a multi-email
flow, use `email_baseline_selections` entries of `action_name` + `route_id` —
plus that email's `image_binding_ids` when the route is image-led — as the
returned contract describes). If that route lacks frozen
evidence, obtain the exact reported facts. Never fall back silently or invent
evidence.

For image-led routes, follow `next_call.image_choice` and supply an exact image
URL plus an accurate description. Preserve all contract, binding, user
constraint, and idempotency fields. Optionally validate, then persist with
`composition_mode: "draft"`; full section authoring is an intentional escape
hatch. The returned metered `optional_server_authoring_call`
(`composition_mode: "generate"`) may instead author, validate, and persist one
draft. SMS-only flows and rename-only patches do not need email authoring
context.

## Review and Approve

1. Show the dry-run preview (node types and connections)
2. Get user approval on the flow design
3. Create for real (without dry_run)
4. Review: `nitro_review_delivery` with `target_type: "flow"`, `target_id`, and
   the exact current `revision_id` (flow reviews require it)
5. Approve: `nitro_control_delivery` with `target_type: "flow"`, `target_id`,
   `operation: "approve"`, the exact current draft `revision_id`, and
   `expected_brand_sid` (copy `meta.current_brand.sid` from the review result)
6. Go live: `nitro_control_delivery` with `target_type: "flow"`, `target_id`,
   `operation: "live"`, `revision_id`, and `expected_brand_sid`

Flow `approve`, `reject`, and `live` all require the exact current draft
`revision_id`; `pause`/`resume` omit it, and `resume` never publishes a draft.
Every `nitro_control_delivery` call requires the `expected_brand_sid` brand
assertion from the result you reviewed — it never switches brands.

## Modify Existing Flows

To rebuild an existing flow:
- Use `nitro_compose_flow` with `mode: "replace"`, `flow_id`, `confirm: true`,
  `expected_draft_revision_id` (the current draft revision), and a stable
  `idempotency_key`

To rename or update selected email actions:
- Use `nitro_compose_flow` with `mode: "patch"`, `flow_id`, an
  `idempotency_key`, targeting email actions by `action_name` + their
  `if_version` concurrency token

Every non-dry-run persistence mutation (create, rename patch, replace) requires
an `idempotency_key`; drafts persisted through the composition contract reuse
the stable key supplied by the returned `next_call`.
