---
name: send-campaign
description: >
  End-to-end campaign workflow: create, design, target audience, preview,
  test, approve, and send or schedule an email or SMS campaign. Use when:
  "send campaign", "email blast", "newsletter", "send to my list",
  "broadcast email", or "schedule campaign".
---

# Send Campaign

Guide the user through the full campaign lifecycle.

## Step 1: Create the Campaign

Ask:
- Campaign name
- Channel: email (default) or SMS
- Subject line (email only)

For email, choose design approach:
- **Inline sections**: Build design from scratch (use compose-email patterns)
- **Clone template**: Use `template_id` from an existing template
- **Plain text**: Just `body` + `subject`

Use `nitro_compose_campaign` with the chosen approach.

**Composition contract**: newly authored email copy or design always enters the
contract before persistence. Call `nitro_compose_campaign` with
`composition_mode: "intent"`; `next_call.input` is the server-selected complete
baseline and `composition_contract.creative_routes` is the compact route menu.
Preserve and fill the baseline by default. To choose another ready route, start
a fresh intent with its `creative_route_id`. A route that lacks frozen evidence
returns the exact missing facts; obtain those facts rather than substituting a
layout or inventing evidence.

Follow `next_call.image_choice` for image-led routes. Reissue intent with an
exact, verified `image_url` and an accurate description of what the image shows.
Then fill the returned `next_call`, preserving its contract, bindings, explicit
user constraints, and idempotency fields. Optionally validate before persisting
with `composition_mode: "draft"`. Full section authoring is an intentional
escape hatch. The returned metered `optional_server_authoring_call`
(`composition_mode: "generate"`) may instead compose, validate, and persist one
draft.
Supplying creative fields without a contract returns the intent contract instead
of creating the campaign. Cloning a template without creative overrides, plain
operational edits, and `dry_run` previews skip recomposition. Preserve explicit
user constraints verbatim: exact copy, URLs, offers, sender fields, audience,
schedule, and legal text.

## Step 2: Target Audience

Ask who should receive this:
- **Contact lists**: Use `audience: { audience_type: "lists", contact_list_ids: [LIST_ID] }` — query lists with `nitro_query` entity "lists"
- **Segment**: Use `audience: { audience_type: "segment", segment_id: SEGMENT_ID }` — query segments with `nitro_query` entity "segments"
- **All subscribers**: Use `audience: { audience_type: "all_contacts" }` only when the user explicitly wants an all-subscribed-contacts send

To suppress recipients (warmup or exclusions), add `exclude_contact_list_ids` and/or `exclude_segment_ids` inside `audience` — pass `[]` to clear; omitting them in patch mode preserves existing exclusions.

If they need a new segment, use `nitro_define_segment` to create one with filters.

## Step 3: Preview and Test

1. Review: `nitro_review_delivery` with `target_type: "campaign"` and `target_id` for validation, readiness, and delivery context
2. Test send: `nitro_send_test_message` with `target_type: "campaign"`, `target_id`, and an `idempotency_key` (reuse the same key on retry to avoid duplicates)
3. Share preview results and ask for approval

## Step 4: Approve

Run `nitro_control_delivery` with `target_type: "campaign"`, `target_id`, `operation: "approve"`, and `expected_brand_sid` — copy `meta.current_brand.sid` from the review result you just showed the user. This required brand assertion guarantees the approval lands on the brand that was reviewed; it never switches brands.

This runs preflight checks:
- Can send (within limits)
- Subscription active
- One ready, explicitly selected sender identity
- Physical address set
- Sender configured

Treat the returned review/admission findings as authoritative. Do not recreate
capacity, sender, content, or billing gates from plan names or local rules.

Report any failed checks and help fix them.

## Step 5: Send or Schedule

Ask: send now or schedule for later?

- **Send now**: `nitro_control_delivery` with `target_type: "campaign"`, `target_id`, `operation: "live"`, and `expected_brand_sid`
- **Schedule**: `nitro_control_delivery` with `target_type: "campaign"`, `target_id`, `operation: "schedule"`, `scheduled_at` (ISO 8601), and `expected_brand_sid`

Every `nitro_control_delivery` call requires the `expected_brand_sid` assertion (`meta.current_brand.sid` from the reviewed result).

For an `all_contacts` audience, both `live` and `schedule` require
`confirm_send_to_all: true` — an explicit all-subscribed-contacts confirmation.

Do not claim a universal optimal send time. Use the recipient context and the
account's own results; if there is insufficient evidence, label the timing as a
test rather than a fact.

## After Sending

Suggest checking results:
- Use `nitro_get_insights` with `scope: "campaign"` and the campaign ID
- Key metrics: open rate, click rate, unsubscribe rate
- Compare against the live insights response and the account's own baseline
