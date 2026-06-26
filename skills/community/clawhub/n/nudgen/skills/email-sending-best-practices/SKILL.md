---
name: email-sending-best-practices
description: >
  Use this skill when the user wants to review, audit, improve, or plan email
  sending quality and deliverability. This includes sender reputation, consent,
  list hygiene, subject and preview quality, campaign vs lifecycle vs
  transactional strategy, and Nudgen-specific sending behaviors (Postmark,
  tracking, unsubscribe handling, contact status states, and campaign rules).
  Trigger on phrases like "deliverability", "sender reputation", "unsubscribe
  flow", "retention email strategy", "subject line review", or "email sending
  best practices".
metadata:
  version: 1.0.0
---

# Email Sending Best Practices

Use this skill for email-program quality, risk, and strategy. It is generic where appropriate, with Nudgen-specific caveats where product behavior changes recommendations.

## When To Use

Use this skill when the task is about:

- inbox placement and sender reputation
- consent quality and list hygiene
- unsubscribe and preference behavior
- content quality: subject, preview, sender identity, and template clarity
- deciding between campaign, lifecycle, and transactional messaging
- reviewing Nudgen email setup for best-practice gaps

Do not default to this skill for pure API implementation tasks; use the `api` skill for endpoint-level integration details.

## When Not To Use

Do not use this skill when the task is:

- implementing endpoint payloads or SDK wiring only
- running purely operational CLI commands without strategy review
- unrelated copywriting tasks with no sending, consent, or deliverability context

## Working Style

When this skill is active:

1. Identify the main problem area first.
2. Load only relevant reference files.
3. Give durable best-practice guidance first.
4. Add Nudgen-specific caveats when they materially change recommendations.
5. Separate immediate fixes from medium-term program improvements.

## Category Routing

- Deliverability, domain setup, warming, inbox placement, and sender reputation:
  Read `references/deliverability.md`
- Consent quality, audience hygiene, imports, and unsubscribe/preference policy:
  Read `references/audience-and-consent.md`
- Content quality, sender identity, template readability, and rendering:
  Read `references/content-and-design.md`
- Campaign vs lifecycle vs transactional strategy and KPI framing:
  Read `references/email-types-and-program-strategy.md`
- Nudgen operational behavior that affects recommendations:
  Read `references/nudgen-operational-caveats.md`

## Output Checklist

Aim to leave the user with:

- likely root causes and priority
- concrete recommendations to change now
- Nudgen-specific caveats that affect implementation
- metrics/signals to monitor after rollout
