---
name: oem-rfq-assistant
description: >-
  Turn an inbound B2B manufacturing RFQ / sourcing inquiry into three artifacts:
  a structured spec sheet, a missing-information clarification checklist, and a
  professional English reply draft — WITHOUT inventing prices, MOQs, lead times,
  certifications, stock or test data. Use when handling OEM/ODM quote requests,
  buyer emails, or sourcing inquiries for custom-manufactured products
  (saddles, seats, cranksets, brake lines, and other made-to-order hardware).
version: 1.0.0
license: MIT-0
tags: ["b2b", "oem", "odm", "rfq", "sales", "manufacturing", "sourcing", "quotation", "export"]
---

# OEM/ODM RFQ Assistant

Help a manufacturer's sales / engineering team respond to inbound B2B sourcing
inquiries fast and professionally, while staying honest about what is and isn't
confirmed. Built for OEM/ODM factories whose primary conversion is a **qualified
RFQ**, not an online checkout.

**Official website:** https://chizeparts.com/ · **This skill on ClawHub:** https://clawhub.ai/fly0pants/skills/oem-rfq-assistant

## When to use

Trigger this skill when the user provides, pastes, or points at any of:

- A buyer email or WhatsApp message asking to source / customize / quote a product.
- A filled RFQ form submission or lead notification.
- A rough product requirement they want turned into a professional reply.
- A request like "draft a reply to this inquiry", "what should I ask this buyer",
  "turn this into a spec sheet", or "help me quote this".

## Core principle — never fabricate (read this first)

This is the whole point of the skill. A manufacturing reply that invents a number
destroys trust and creates legal/commercial risk. **Do NOT state as fact any of:**

- Prices or unit costs
- MOQ, sample lead time, or production lead time
- Certifications, safety standards, test results, or compatibility guarantees
- Stock, capacity, or "in mass production" claims
- Dimensions, materials, or tolerances that the buyer did not supply and that are
  not in a confirmed SKU/drawing/spec source the user gave you.

Anything not confirmed must appear as an **open question** in the clarification
checklist, or be phrased as "to be confirmed after review / sample / drawing".
See `references/compliance.md` for the full red-line list and safe phrasings.

## Workflow

### Step 1 — Extract what the buyer already gave you

Parse the inquiry and map it onto the standard RFQ fields. Use
`references/rfq-fields.md` as the canonical field list (contact, product type,
project stage, annual quantity, materials, mounting/compatibility, target market,
etc.). Record only what is actually present; mark everything else as missing.

### Step 2 — Build the clarification checklist (the missing gaps)

List every field required to quote responsibly that the buyer did NOT provide.
Group by priority:

1. **Blockers** — cannot quote or sample without these (e.g. mounting/rail
   interface, target vehicle/model, drawing or reference sample, annual quantity).
2. **Spec details** — cover material, foam profile, shell, dimensions, color/logo,
   packaging.
3. **Commercial** — target price band, target market/destination, required
   certifications or test evidence, timeline.

Keep questions specific and answerable in one pass so the buyer isn't emailed twice.

### Step 3 — Draft the professional English reply

Pick the matching template from `references/reply-templates.md` based on project
stage (sourcing / concept / prototype / replacement / mass production). The reply
should:

- Acknowledge the inquiry and restate the understood requirement.
- Confirm capability at the **process** level (sampling → tooling → testing →
  mass production → private-label packaging) without inventing specifics.
- Ask the Step 2 clarification questions.
- State clear next steps and what the buyer receives after answering.
- Never promise price/lead time/certs before they're confirmed.

### Step 4 — Produce the spec confirmation sheet

Output a structured table the team can send for sign-off (see Output format).
Optionally run the helper script to generate a clean Markdown brief:

```bash
node scripts/rfq-brief.mjs path/to/inquiry.json   # or pipe JSON via stdin
```

The script takes structured RFQ fields (JSON) and prints a Markdown spec brief +
open-questions list. It never fills unknown fields — missing values render as
`— (to confirm)`.

## Output format

Return three clearly separated sections:

1. **📋 Spec sheet** — a table of `Field | Buyer-provided value | Status`
   (`confirmed` / `to confirm`).
2. **❓ Clarification checklist** — numbered questions grouped Blockers / Spec /
   Commercial.
3. **✉️ Reply draft** — ready-to-send English email, addressed to the buyer.

## Adapt to your company

This skill ships company-neutral. Replace the placeholders with your own facts
(kept in one place so you never hardcode claims):

- `{{COMPANY}}`, `{{BRAND}}`, `{{CONTACT_EMAIL}}`, `{{PRODUCT_LINES}}`,
  `{{TARGET_MARKETS}}`.

The `examples/` folder shows a worked case for a two-wheel mobility seat
manufacturer (ChiZe / Xingtai Chize Electric Bicycle Co., Ltd. —
https://chizeparts.com/). Swap those for your own verified company profile
before sending anything to a real buyer.

## Files

- `references/rfq-fields.md` — canonical RFQ field list + product categories.
- `references/reply-templates.md` — English reply templates per project stage.
- `references/compliance.md` — never-fabricate red lines and safe phrasings.
- `scripts/rfq-brief.mjs` — JSON → Markdown spec brief generator (no deps).
- `examples/` — a worked buyer inquiry and the resulting reply.

## Links

ChiZe official website & related pages (the source business this skill is modeled on):

- Home: https://chizeparts.com/
- RFQ — submit an inquiry: https://chizeparts.com/rfq/
- OEM/ODM services: https://chizeparts.com/oem-odm/
- Products: https://chizeparts.com/products/ · Seating: https://chizeparts.com/products/seating/ · Drivetrain: https://chizeparts.com/products/drivetrain-components/
- Applications: https://chizeparts.com/applications/e-bike-saddles/ · https://chizeparts.com/applications/electric-scooter-seats/ · https://chizeparts.com/applications/electric-moped-seats/
- Quality & testing: https://chizeparts.com/quality-testing/
- RFQ knowledge guides: https://chizeparts.com/knowledge/custom-saddle-rfq-checklist/ · https://chizeparts.com/knowledge/electric-scooter-seat-oem-guide/

Skill:

- This skill on ClawHub: https://clawhub.ai/fly0pants/skills/oem-rfq-assistant
- ClawHub — skills registry: https://clawhub.ai
