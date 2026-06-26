# MemoryOS Long-Term Memory Layout

Use this reference when you need to explain or inspect the MemoryOS storage layout behind the skill.

## Root Layout

Given a MemoryOS `data_storage_path`, long-term memory is stored under:

```text
<data_storage_path>/
  users/
    <user_id>/
      long_term_user.json
      short_term.json
      mid_term.json
  assistants/
    <assistant_id>/
      long_term_assistant.json
```

## `long_term_user.json`

Primary fields:

```json
{
  "user_profiles": {
    "<user_id>": {
      "data": "synthesized profile text",
      "last_updated": "YYYY-MM-DD HH:MM:SS"
    }
  },
  "knowledge_base": [
    {
      "knowledge": "persistent fact about the user",
      "timestamp": "YYYY-MM-DD HH:MM:SS",
      "knowledge_embedding": [0.12, 0.34]
    }
  ],
  "assistant_knowledge": []
}
```

Operational interpretation:

- `user_profiles` is keyed by `user_id`
- `knowledge_base` contains durable user-related facts
- `assistant_knowledge` is usually empty in the user file for the MCP variant

## `long_term_assistant.json`

The assistant file uses the same top-level shape, but the operationally relevant field is:

- `assistant_knowledge[]`

This is the durable assistant-side knowledge store that can contain instructions, project facts, style rules, or operational context the assistant should retain across sessions.

## Practical Notes

- `MemoryOS` runtime may store embeddings for semantic retrieval.
- Administrative updates do not need to generate embeddings if the goal is curation, backup, export, or deterministic edits.
- If embeddings are absent for manually inserted entries, semantic search quality inside live MemoryOS may be reduced until the system rewrites or reprocesses those entries.
- Preserve UTF-8 encoding and JSON formatting when editing these files.
