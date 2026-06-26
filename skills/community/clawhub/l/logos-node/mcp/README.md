# MCP Integration — v0.2 Placeholder

This directory is reserved for the future **logos-rag-mcp** server that will power
a smarter version of the Logos Node skill.

---

## Planned architecture

```
SKILL.md
  └─ MCP call: mcp://localhost:3000/logos-docs
       └─ logos-rag-mcp (citizenweb3/logos-rag-mcp — not yet published)
            ├─ Vectorized Logos documentation
            ├─ Release notes + breaking-change history
            ├─ Node API reference (logos-node-api.md)
            └─ Sharp-edges knowledge base
```

When the MCP server is available, the skill will replace static procedure file references
with live tool calls to retrieve up-to-date, context-aware instructions.

## Why MCP?

Static markdown files in `skill/` are good but have one limitation: if Logos releases a new
version with changed steps (new flags, new paths, new peer format), someone must manually
update the files in this repo.

With a RAG-backed MCP server:
- The server indexes the Logos docs repo automatically
- The skill always retrieves the most current instructions
- No PR to this repo needed for routine Logos version changes

## Activating in SKILL.md (when ready)

Uncomment the `# TODO v2` section in `skill/SKILL.md` and add:

```yaml
allowed-tools:
  - Bash
  - Read
  - Write
  - WebFetch
  - mcp__logos_docs__install
  - mcp__logos_docs__update
  - mcp__logos_docs__status
```

## Contributing

If you want to build logos-rag-mcp, open an issue in citizenweb3/ai-integrations
or start a PR in a new repo `citizenweb3/logos-rag-mcp`.
