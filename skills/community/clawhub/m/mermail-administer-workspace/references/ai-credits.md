# Workspace AI credits

Use `get_ai_credit_usage` for the authenticated workspace's mode, period, allowance, charged/settled credits, reserved credits, remaining credits, renewal time, and action prices. Use `list_ai_credit_events` for bounded history (`query.cursor`, `query.limit` 1–100). The event history does not contain prompts, email bodies, or provider payloads. Do not combine AI credits with API usage, provision credits, or PayBox money.

In `observe` mode, recorded usage is hypothetical and does not reduce an enforced balance. In `enforce` mode, new AI work needs available credits. A reservation is not a settled charge: a delivered result or confirmed external action settles it, while an unresolved result stays reserved until authoritative reconciliation. Never infer a release from a timeout, browser disconnect, or expired lease.

At `ai_credits_exhausted` (HTTP 402), report `required`, `available`, and `renews_at` from the response. Pause new generation; automatic email work becomes manual handling and does not replay on renewal. Normal mail, saved drafts, manual replies, and security checks remain available. At `ai_credit_accounting_unavailable` (HTTP 503), report the outage and do not fabricate a balance or bypass accounting.

At `ai_action_in_progress`, retain the same idempotency key and request fingerprint to retrieve the original response when available. On an ambiguous outcome, inspect durable draft, delivery, or run state before any new action. A new key, altered inputs, or a second send is a distinct action and must not be used to force a retry or another charge.
