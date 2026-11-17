# Provider policy

Do not infer credentials from environment variables or hard-code a cheapest model.
Use the selected agent's native catalog/status and an operator-owned ordered tier policy.
The bundled policy is an optional OpenAI example, not a universal recommendation.
Change the identifiers for the models your account exposes.

Availability, allowlist membership, capability metadata, and successful inference are
separate evidence. An available catalog row does not prove that OAuth, a particular
runtime, or the exact model route will work. v4 never runs a paid canary automatically.
Before activation, explicitly test the exact route and inspect the actual model used.

Unknown image/tool/context capability blocks a requirement that needs it. Catalogs
that omit tool metadata require a trustworthy normalized export with supportsTools=true;
do not fill this field by guessing. Native route issues block recommendations until resolved.

Tier ordering represents the user's quality/cost/latency preference. v4 does not scrape
prices, claim live pricing, infer model quality from names, or estimate model latency.
Retirements should be handled by refreshing catalog/status and reviewing provider notices.

Prompt cache lifetime and billing vary by provider, account, and model. Compare measured
cache writes, cache reads, input and output cost. Never assume that extra cache-warming
heartbeats save money. Same-provider fallbacks do not guarantee resilience to auth outages.

Sources: https://docs.openclaw.ai/releases/2026.9.4
https://developers.openai.com/codex/models
