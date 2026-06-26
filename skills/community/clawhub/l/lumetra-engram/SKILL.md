---
name: lumetra-engram
description: Persistent, explainable memory for your OpenClaw agent — store facts and recall them later via the hosted Engram MCP server (by Lumetra).
user-invocable: true
metadata:
  openclaw:
    emoji: "🧠"
    version: "0.1.1"
    homepage: "https://lumetra.io"
    repository: "https://github.com/lumetra-io/engram-openclaw-skill"
    license: "MIT"
    author: "Lumetra <hi@lumetra.io>"
    keywords: ["memory", "mcp", "engram", "lumetra", "context"]
    requires:
      bins: ["mcporter"]
      env: ["ENGRAM_API_KEY"]
    install:
      - id: "node"
        kind: "node"
        package: "mcporter"
        bins: ["mcporter"]
        label: "Install mcporter (node)"
---

# Engram Memory

You have access to **Engram**, a hosted memory service for AI agents. Engram lets you remember facts, decisions, and context across conversations using a hybrid retrieval engine (BM25 + vector + knowledge graph) and returns an explanation trace with every recall.

The Engram tools are surfaced through `mcporter` from the MCP server registered as `engram-lumetra` (or whatever name the operator chose during setup — see the one-time setup below). When in doubt, call `mcporter list` to see the available servers and tool selectors.

## One-time setup (operator)

Before this skill can do anything, the operator must register the Engram MCP server with `mcporter`. Single command:

```bash
mcporter config add engram-lumetra https://mcp.lumetra.io/mcp/sse \
  --transport sse \
  --header "Authorization=Bearer $ENGRAM_API_KEY"
```

After that, `mcporter list` should show `engram-lumetra` with 6 tools and `mcporter call engram-lumetra.list_buckets` should return a JSON bucket list. If `mcporter` is missing, OpenClaw will offer to install it from the requirement declaration above.

> The server is named `engram-lumetra` rather than just `engram` to avoid colliding with stale `engram` entries that `mcporter` may auto-import from `~/.cursor/mcp.json`, `~/.codeium/windsurf/mcp_config.json`, or similar editor configs.

## When to use

- **Before answering** anything that may rely on prior context: call `engram-lumetra.query_memory` first and ground your answer in the results.
- **When the user shares a fact** worth remembering (preferences, project details, decisions, deadlines): call `engram-lumetra.store_memory` to capture it.
- **At the end of a useful conversation**: capture stable takeaways with `engram-lumetra.store_memory`.

## Tools (invoke via `mcporter call`)

| Tool | Description |
|---|---|
| `engram-lumetra.store_memory(content, bucket?)` | Save a fact. `bucket` defaults to `"default"`. |
| `engram-lumetra.query_memory(question, bucket?)` | Hybrid retrieval + synthesized answer with citations. |
| `engram-lumetra.list_memories(bucket, limit?)` | List memories in a bucket, newest first (`limit` 1–100, default 20). |
| `engram-lumetra.list_buckets()` | Show all buckets in the tenant. |
| `engram-lumetra.delete_memory(memory_id, bucket)` | Delete one memory by ID. |
| `engram-lumetra.clear_memories(bucket)` | Delete every memory in a bucket (destructive!). |

If the operator registered the server under a different name, substitute it for `engram-lumetra.` in every selector.

## Style

- Store **atomic, declarative facts**, one concept per memory. Good: `"User prefers dark mode."` Bad: `"The user mentioned they like dark mode, also they live in Seattle, also..."`
- Use **buckets** to separate contexts: `"work"`, `"personal"`, `"project-alpha"`. If no bucket fits, omit it and the default bucket is used.
- Quote citations from the explanation trace when the user asks "how do you know that?".

## BYOK note

Engram is bring-your-own-key end-to-end — inference (embeddings, synthesis, graph extraction) runs through the user's OpenAI / Anthropic / Groq / Together / Fireworks / DeepSeek key configured at https://lumetra.io/models. Without a provider key, every `store_memory` and `query_memory` returns HTTP 412. If you see that error, tell the user to visit the models page.
