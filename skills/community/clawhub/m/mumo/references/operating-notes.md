# Operating Notes

Practical agent mechanics that don't belong in the kernel but matter during real sessions.

## Recovery

Use `list_sessions` to recover sessions when:

- the agent restarted mid-session
- a round timed out but may still be running
- multiple sessions are active

Use `get_session` for full state. Prefer `wait_for_round` while a round is in flight.

## Idempotency

MCP write tools are idempotent by arguments. Retrying the same call after a transport failure replays the same operation rather than creating duplicates.

Don't make meaningless edits to a prompt just to "try again" — that creates a new operation.

## Synthesis boundary

mumo's deliberation surface is raw participant output plus moderator attention. Don't write your synthesis back into mumo as an `append_round` unless the user explicitly wants a synthesis round.

Your final answer to the user can freely synthesize your read of the panel. Make the distinction clear: mumo produced the raw material; your response is your interpretation for the user.

## /progress for diagnostic polling

`wait_for_round` is the right default — it blocks server-side and returns when the round settles. For diagnosing partial-round failures, watching per-model state in flight, or polling cheaply without holding an HTTP connection open, hit `GET /api/sessions/{id}/progress` directly.

What it returns per round:

- `moderation_status`: `pending` | `complete` | `failed`
- `refund_status`: `none` | `pending` | `credited` | `not_applicable` (plus `refund_deadline_at` / `failure_code` when relevant)
- `progress_version`: monotonic counter — increments only on real state changes, so diff this to short-circuit no-op polls
- `models[]`: per-model state (`queued` | `streaming` | `absent` | `final` | `error`) plus `partial_text_length`, `last_chunk_at`, `since_last_chunk_ms`, `deadline_at`, `expired_at_read`, and `error_code` on errors

Two practical patterns:

1. **Cheap polling.** Every response carries a weak `ETag`. Send it back via `If-None-Match` on the next poll — the server returns `304 Not Modified` on no change. The validator covers round-level state, per-model state, and (for non-terminal rounds) a 5-second wall-clock bucket so timing fields stay fresh.
2. **Partial-round forensics.** When `wait_for_round` returns `proceed_with_partial_result` or `abandon`, `/progress` is where to look for the per-model story: which model produced how many characters before failing, what `error_code` it terminated on, when its last chunk arrived. Useful when the user asks "what actually happened" and you need more than the `failed_models[]` summary in the wait_for_round result.

Don't use `/progress` as a replacement for `wait_for_round` in the normal loop — `wait_for_round` is cheaper end-to-end because it consolidates the server-side polling. Reach for `/progress` when you specifically need the per-model state shape or the ETag-based no-change semantics.

## Platform meta in edge cases

The kernel's test — "does this help participants think about the user's problem?" — covers most cases. A few edge cases worth noting:

- **Model behavior is the user's topic.** If the user is evaluating model capabilities, model-comparative observations are problem context, not platform meta. Include them.
- **Budget constraints are real.** If the user has said they're watching costs, "this is a $0.50/round panel" is useful context for deciding whether to append. But frame it as a decision input, not a report.
- **Tool failures.** If a model failed to respond and the round is incomplete, that's worth noting in your prompt or to the user. It changes the epistemic state of the session.
