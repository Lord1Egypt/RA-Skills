See local agent workspace copy for the full reference text. Shared publishable copy stays generic.
Implemented design includes confidence thresholds, VIP/never-archive controls, multi-mode rollout, and split notification routing.

Additional operational notes
- For non-interactive cron/agent runs, prefer the launcher pattern that exports any required auth env vars before calling Python/CLI helpers. In this environment, `gog` reads tokens through a keyring backend and non-interactive runs must provide the needed keyring secret up front.
- Keep shared/public logic generic. User-specific editorial/business filters (for example press-release handling or custom PR heuristics) belong in the local overlay, not in the published skill defaults.
- Be conservative with reply-like messages. Generic non-actionable filters should avoid matching obvious replies (`Re:`, `Fwd:`, `In-Reply-To`, `References`) unless that behavior is explicitly intended.
- Prefer idempotent fetch/process loops: skip already-processed messages at query time when possible and also deduplicate by message ID within a run.
- Gmail mutation can differ between thread-level and message-level operations. When thread mutation fails for a specific item (for example `404 notFound`), fall back to message-level mutation instead of failing the whole pass.

Canonical public guidance
- Prefer an **Inbox-by-exception** model: messages stay in Inbox only when clearly important/actionable.
- Everything processed should receive `Auto/Triaged`, even when only a generic category is available.
- A useful public fallback is to classify unmatched automation/company mail as a generic notification/update rather than leaving it in Inbox.
- Keep the public skill focused on canonical labels and normalization; user-specific label names and editorial nuances belong in the local overlay.
