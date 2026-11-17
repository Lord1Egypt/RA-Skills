# Sift — user_relevance Field

Every Signal emitted by Sift carries a `user_relevance` field with one of two values:

- `"user"` — the signal is relevant to the user's personal knowledge graph
- `"agent_only"` — the signal is agent-initiated research with no demonstrated user connection

**Default is `"agent_only"`** because much of Sift's research may be agent-initiated (scheduled runs, background enrichment, cooperative queries from other skills). A signal receives `user_relevance: "user"` only when:

1. The user explicitly requested the search or research (e.g., "search for X", "look up Y", or any direct user prompt that triggered the run), OR
2. The entity has a demonstrated connection to an entity already in Chronicle with `user_relevance: "user"`.

When in doubt, default to `"agent_only"`. See references/integration-notes.md for current backend architecture. can promote later if a user connection is established.

Signal example:
```json
{
  "signal_id": "sig-sift-20260402-001",
  "source_skill": "ocas-sift",
  "source_journal_type": "Research",
  "emitted_at": "2026-04-02T14:30:00Z",
  "user_relevance": "agent_only",
  "payload": {
    "type": "Concept/Event",
    "name": "2026 Solar Eclipse",
    "confidence": "high",
    "source_refs": ["https://example.com/eclipse"]
  }
}
```

Sift may read Thread's active context for query rewriting and Weave's database for entity disambiguation (both cooperative read-only; see `spec-ocas-interfaces.md` Cooperative Query Interfaces).
