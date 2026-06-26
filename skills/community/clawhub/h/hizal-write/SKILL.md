---
name: hizal-write
description: Persist what the agent learns as it builds. Self-triggering — fires whenever the agent makes a decision, discovers a pattern, learns a convention, hits a gotcha, or gains knowledge worth keeping. Use continuously, not just at the end. Triggers on phrases like "good to know", "I'll remember that", "worth noting", "that's a pattern", "lesson learned", "this is how we do it", or any moment the agent learns something it would otherwise forget.
---

# Hizal Write

Write as you build. Not optional.

## Available Write Tools

| What you're writing | Tool | Scope |
|---------------------|------|-------|
| Personal observation or lesson learned | `hizal__write_memory` | AGENT |
| Architecture or design decision | `hizal__write_knowledge` | PROJECT |
| Convention this codebase follows | `hizal__write_convention` | PROJECT (auto-inject) |
| Agent identity or personality | `hizal__write_identity` | AGENT (auto-inject) |
| Org-wide knowledge | `hizal__write_org_knowledge` | ORG |
| Principle (requires human promotion) | `hizal__store_principle` | ORG |
| Custom chunk type | `hizal__write_chunk` | varies |

**Do not use `hizal__write_context`** — it's deprecated. Use the purpose-built tools above.

## Custom Chunk Types via write_chunk

For chunk types not covered by the built-in tools, use `hizal__write_chunk`. Chunk types are customizable per org — always discover what's available before assuming a type doesn't exist.

### Discover Available Types

```
hizal__list_chunks()  # inspect chunk_type values in results
```

Or check the project's AGENTS.md for the org's type conventions.

### Usage

```
hizal__write_chunk(
  type="<chunk-type-slug>",
  query_key="<unique-key>",
  title="<short title>",
  content="<full content>",
  scope="PROJECT",  # or AGENT, ORG
  project_id="<id>",  # required for PROJECT scope
  org_id="<id>",  # required for ORG scope
  agent_id="<id>"  # required for AGENT scope
)
```

`write_chunk` accepts the same common fields as all other write tools (query_key, title, content, gotchas, related, source_file, inject_audience, etc.). It also accepts `custom_fields` for type-specific metadata.

### When to Use write_chunk vs Built-in Tools

- **Built-in tools** — use whenever the content maps cleanly to MEMORY, KNOWLEDGE, CONVENTION, IDENTITY, ORG_KNOWLEDGE, or PRINCIPLE
- **write_chunk** — use for any custom org type (e.g., SPEC, RUNBOOK, ADR, INVESTIGATION)
- When in doubt, check what chunk types the org has defined and pick the closest match

## Write One Chunk Per Decision

Don't batch everything into one chunk at the end. Write as you go:

- Made an architecture decision? → `write_knowledge` now
- Learned a codebase convention? → `write_convention` now
- Discovered something useful personally? → `write_memory` now
- Found a custom type that fits better? → `write_chunk` now

## Common Fields

All write tools accept:

- **query_key** — unique key for this topic (enables exact lookup later)
- **title** — short descriptive title
- **content** — the full context content
- **source_file** / **source_lines** — where this came from
- **gotchas** — list of warnings or pitfalls
- **related** — list of related query_keys
- **inject_audience** — DNF targeting spec for auto-injection (omit for defaults)

## Example

```
hizal__write_knowledge(
  project_id="<id>",
  query_key="nuvei-webhook-signing",
  title="DMN Webhook Signature Verification",
  content="All DMN payloads are verified using SHA-256 HMAC. The checksum is computed from sorted key-value pairs + merchant secret. See package internal/checksum for implementation.",
  related=["nuvei-payload-structure", "merchant-credentials"],
  gotchas=["Never use /payment for credential verification"]
)
```

## Promote AGENT → PROJECT

If a personal memory chunk is broadly useful for the team, promote it:

1. Read the chunk with `hizal__read_context`
2. Write it back as `write_knowledge` or `write_convention` with the content
3. Optionally delete the original AGENT chunk with `hizal__delete_context`
