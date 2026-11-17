---
name: compose-email
description: >
  Create or edit email templates with Nitrosend's section-based designer.
  Guides through layout, content, and brand styling. Supports preview and
  test sends. Use when: "compose email", "design template", "create email",
  "email template", "edit template", or "update email design".
---

# Compose Email

Help the user create or edit an email template using Nitrosend's section-based email designer.

## Understand the Goal

Ask what the email is for:
- Newsletter / announcement
- Welcome email
- Promotional / sale
- Product update
- Event invitation
- Transactional (receipt, confirmation, etc.)
- Re-engagement

## Design the Email

The complete section registry and prop schemas returned by the intent scaffold
or `nitro://schema` are authoritative. Do not reconstruct that registry from
this skill. Illustrative section patterns include:

| Section | Key Props |
|---------|-----------|
| `header` | `logo_url`, `logo_alt`, `logo_width`, `background_color` |
| `text` | `content` (HTML string) |
| `image` | `src`, `alt`, `href`, `width` |
| `button` | `text`, `href`, `background_color`, `text_color`, `align`, `border_radius` |
| `columns` | `columns: [{width, sections: [...]}]` — nested sections |
| `hero` | Use the exact props returned by the live schema |
| `product` | `name`, `price`, `image_url`, `href`, `description` |
| `products` | Use the exact collection props returned by the live schema |
| `gallery` | Use the exact image-list props returned by the live schema |
| `social` | `links: [{platform, url}]`, `align` |
| `divider` | `color`, `width`, `padding` |
| `spacer` | `height` |
| `footer` | `unsubscribe_text` (optional override) |

### Durable Design Guidance

- Front-load the subject's value and make the preheader complementary.
- Prefer a clear hierarchy and one primary action.
- Design mobile-first, use readable type, descriptive alt text, and adequate
  contrast.
- Include a footer. Nitrosend supplies the active Brand's canonical legal
  identity and unsubscribe URL.

## Composition Contract

Newly authored copy or full sections always enter the composition contract
before persistence:

1. Call `nitro_manage_template` with `composition_mode: "intent"` and the
   user's goal and constraints.
2. Treat `next_call.input` as the selected complete baseline. Preserve its
   structure and fill it rather than replacing it with a smaller handcrafted
   layout. `composition_contract.creative_routes` is the route menu.
3. To use a different ready route, start a fresh intent with its
   `creative_route_id`. If a route reports missing evidence, obtain exactly
   those facts; never substitute another route or invent evidence.
4. Author inside the returned scaffold while preserving the contract,
   bindings, exact user constraints, and idempotency fields. Optionally call
   `composition_mode: "validate"`; persist with `composition_mode: "draft"`.

Alternatively, request server-side authoring via the returned metered
`composition_mode: "generate"` call, which composes, validates, and persists one
draft. Supplying creative fields without a contract returns the intent contract
instead of silently creating anything. Only mechanical `section_updates` —
shallow prop/style tweaks on allowed visual attributes — and clones without
creative overrides skip recomposition. `text_patch` copy edits are copy
changes: they enter the composition contract like any other new copy.

Full section authoring is an intentional escape hatch, not the default. For an
image-led route, follow `next_call.image_choice`. Use a described Brand Library
asset or exact operator asset when available. Otherwise obtain a verified
vendor, generated, or public stock asset, ingest it when needed, and reissue the
intent with the exact `image_url` plus an accurate statement of what it shows.
Brand memory can guide selection but cannot prove an image URL or its contents.

## Create or Update

**New template**: Use `nitro_manage_template` with `sections` array and `subject` (via the composition contract above).

**Update existing**: Use `nitro_manage_template` with `template_id` and the fields to change — prefer `section_updates` for targeted edits, and pass `if_version` for optimistic concurrency (the call is rejected if the template version has moved).

**Update a campaign's email**: Use `nitro_compose_campaign` with `campaign_id`, `mode: "patch"` and the same `section_updates`, plus `if_version`. A campaign's email is saved through its campaign, never through `nitro_manage_template`.

**Clone existing**: Use `nitro_manage_template` with `based_on` (source template ID); creative overrides enter the authoring contract.

Every non-dry-run persistence mutation — create, clone, targeted update, full
update — requires an `idempotency_key`; contract drafts reuse the stable key
carried by the returned `next_call`.

Always set a descriptive `name` for the template.

## Images

Host images on Nitrosend storage with `nitro_ingest` (V1 is image-only):

- Small local or chat-attached images: pass `image_data`
- Larger local files: request a direct upload with `upload: {kind, filename,
  content_type, byte_size, checksum}`, PUT the bytes to the returned
  `direct_upload.url` sending exactly the returned `direct_upload.headers`,
  then call `nitro_ingest` again with the `signed_id`
- Public remote image URLs: use directly in sections when permanence is not
  needed, or pass as `image_url` for a Nitrosend-hosted copy

Always pass an accurate `description` to `nitro_ingest`; it is retained with
the Brand Library asset and used as alt-text context. `image_data` accepts PNG,
JPEG, or WebP under the live tool's decoded-size limit. Direct upload checksum
is base64-encoded MD5.

The returned hosted URL (`media_url`/`image_url`) is what goes into the `image`
section's `src` — never place a `signed_id` directly in sections.

## Preview and Test

After creating/updating:
1. Use `nitro_review_delivery` with `target_type: "template"` and `target_id` to review content, validate, and check delivery readiness
2. Ask if they want a test email sent
3. If yes, use `nitro_send_test_message` with `target_type: "template"`, `target_id`, and an `idempotency_key` (reuse the same key on retry to avoid duplicate test sends) — sends to saved test recipients or specify explicit recipients with `to`

## Merge Tags

Use canonical personalization variables:

- `{{ contact.first_name }}`, `{{ contact.last_name }}`, `{{ contact.email }}`
- `{{ unsubscribe_url }}` — required in marketing emails
- `{{ event.* }}` for flow-event values allowed by the returned composition
  bindings
- `{{ data.* }}` only where the returned composition contract permits it
