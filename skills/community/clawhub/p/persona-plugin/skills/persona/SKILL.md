# Persona — Caller Memory & Identity

You have access to a persistent caller memory system. Use it to remember who you're talking to across calls and build a deeper understanding of each person over time.

## When to Use

- **Before every outbound call**: Use `persona_get_caller` to load context, then pass the `prompt_context` as the `purpose` parameter when calling `clawtalk_call`
- **End of every call**: Use `persona_log_call` to save the call record, then `persona_update_docs` to save what you learned about the caller

Three tools, used in sequence: get → log → update.

## Tools

### `persona_get_caller`

Look up a caller by phone number. Returns everything you know about them.

**Parameters:**
- `phone` (required) — E.164 format (e.g. `+15551234567`)

**Returns:**
- `found` — whether this caller exists in the system
- `prompt_context` — a pre-compiled text block to pass as the `purpose` when initiating a call
- `persona.soul` — their communication style and personality
- `persona.identity` — factual info (name, family, preferences)
- `persona.memory` — episodic memories from past calls
- `recent_calls` — last 3 calls with summaries

**When `found` is false**, this is a brand new caller. Introduce yourself and learn about them.

### `persona_log_call`

Log a completed call. **Use this at the end of every call.** Records the call metadata.

**Parameters:**
- `phone` (required) — E.164 format
- `summary` (required) — what happened in the call. Be specific: topics discussed, decisions made, emotions expressed, follow-ups mentioned.
- `purpose` — why the call happened (e.g. "check-in", "appointment reminder")
- `duration_seconds` — how long the call lasted
- `direction` — `"inbound"` or `"outbound"`
- `call_id` — ClawdTalk call ID. If provided, the backend auto-fetches the full transcript.

### `persona_update_docs`

Update the caller's persona documents. **Use this immediately after `persona_log_call`.**
You are the LLM — extract observations from the conversation and save them here.

**Parameters:**
- `phone` (required) — E.164 format
- `soul` (optional) — communication style and personality observations. Only include if you noticed something about HOW they communicate. Changes slowly.
  ```json
  {"style": "warm, patient", "pace": "slow", "humor": "dry, appreciates puns"}
  ```
- `identity` (optional) — factual information you learned. Accumulates over time.
  ```json
  {"name": "Margaret", "nickname": "Maggie", "family": {"daughter": "Susan"}, "likes": ["gardening", "tea"]}
  ```
- `memory` (optional) — episodic notes from THIS call, keyed by today's date.
  ```json
  {"2026-03-21": "Talked about new rose bushes. Doctor appointment next Tuesday. Susan hasn't called in a while."}
  ```

Each update creates a new VERSION — old versions are never lost.

## Typical Call Flow

```
1. Before making a call
   └─► persona_get_caller with the caller's phone number
       └─► If found: take the prompt_context from the result
       └─► If not found: this is someone new

2. Initiate the call
   └─► clawtalk_call with:
       - to: the phone number
       - purpose: the prompt_context from step 1
       - greeting: a personalized greeting based on what you know

3. During the call
   └─► Have a natural conversation
   └─► No tools needed — just talk

4. Call ends — TWO steps:

   Step A: Log the call
   └─► persona_log_call with:
       - phone number
       - summary of what you discussed
       - call_id from the clawtalk_call result

   Step B: Update persona (immediately after)
   └─► persona_update_docs with:
       - phone number
       - soul: any personality/style observations (optional)
       - identity: any new facts learned (optional)
       - memory: episodic notes from this call (always include)
```

## Important Notes

- Phone numbers must be in E.164 format: `+15551234567` (with country code)
- **Always call `persona_get_caller` BEFORE `clawtalk_call`** so you can pass persona context as the `purpose`
- **Always call both `persona_log_call` AND `persona_update_docs` at call end** — log first, then update
- The `persona_log_call` tool auto-creates the caller if they don't exist
- For `memory`, always key entries by today's date (e.g. `"2026-03-21": "..."`)
- For `identity`, MERGE with what you already know — don't repeat existing facts, add new ones
- For `soul`, only update when you notice something genuinely new about their communication style
- If the Persona API is unreachable, tools will return errors — the call can still proceed
