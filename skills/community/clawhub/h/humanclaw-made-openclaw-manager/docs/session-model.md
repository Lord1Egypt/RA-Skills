# Session Model

`ThreadShadow` is the observation layer. `Session` is the promoted work object.

Each shadow owns:

- `shadow_id`
- `source_type`
- `source_thread_key`
- `title`
- `latest_summary`
- `turn_count`
- `last_message_at`
- `state`
- `promotion_reasons`
- `linked_session_id`

The primary managed work object is still `Session`, not a raw chat thread.

Each session owns:

- `session_id`
- `title`
- `objective`
- `owner`
- `source_channels`
- `current_state`
- `active_run_id`
- `priority`
- `blockers`
- `pending_human_decisions`
- `derived_summary`
- `tags`
- `metadata`
- `scores`
- `created_at`
- `updated_at`
- `archived_at`

Each `Run` is a concrete execution attempt inside a session. Runs use this state model:

- `accepted`
- `queued`
- `running`
- `waiting_human`
- `blocked`
- `completed`
- `failed`
- `cancelled`
- `superseded`

Recovery is checkpoint-first:

1. read `summary.md`
2. read `checkpoint.json`
3. preview recent `spool.jsonl`
4. open a new run with `resume_context`
5. continue from structured state instead of rescanning the whole chat
