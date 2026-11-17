---
name: nitrosend-analytics
description: >
  Inspect Nitrosend account, campaign, flow, or message performance and turn
  live metrics into bounded recommendations. Use when: "email analytics",
  "campaign performance", "how are my emails doing", "email insights",
  "check my stats", "open rate", or "deliverability report".
---

# Analytics

Use live Nitrosend data as the source of truth. Do not apply fixed global
"good", "warning", or "critical" thresholds from this skill.

## Select Scope

- Account overview: `nitro_get_insights` with `scope: "account"`
- Campaign: `scope: "campaign"` plus `entity_id`
- Flow: `scope: "flow"` plus `entity_id`
- Individual message and events: `scope: "message"` plus `entity_id`

Supported periods for account, campaign, and flow insights are `7d`, `30d`, and
`90d`.

## Interpret Responsibly

1. Lead with delivery, volume, opens, clicks, unsubscribes, complaints, and the
   trend data the tool actually returns.
2. Prefer benchmarks and recommendations returned by `nitro_get_insights`,
   then compare with the same account's prior period and similar sends.
3. Treat opens as directional because mailbox privacy features can inflate or
   obscure them. Give clicks, conversions, replies, complaints, and revenue
   greater weight when available.
4. State the sample size and period. Do not call a change meaningful when the
   evidence is too small or the compared periods differ materially.
5. Label external industry ranges as contextual, source them freshly, and do
   not present them as Nitrosend product facts or guarantees.

## Deeper Review

For a broader account review:

1. Pull 30-day and, when useful, 90-day account insights.
2. Query recent campaigns with `nitro_query` entity `campaigns`.
3. Query relevant flows using statuses allowed by the live `nitro_query`
   schema, such as `live` or `paused`.
4. Inspect audience and deliverability context from `nitro_get_status` and the
   returned insights rather than deriving unsupported counts.
5. Prioritize one or two testable changes and define the metric and observation
   window before recommending a rollout.

Typical hypotheses include subject or sender clarity for weak opens, content
hierarchy and CTA clarity for weak clicks, consent/frequency/targeting for
unsubscribes or complaints, and flow coverage for missed lifecycle moments.
These are hypotheses to test, not diagnoses from one metric alone.

## Scheduled Reports

Recurring reports run only when a user has configured them through a host that
actually exposes scheduling. Never imply that installing this plugin creates
background jobs by itself.
