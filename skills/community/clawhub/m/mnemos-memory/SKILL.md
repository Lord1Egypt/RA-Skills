---
name: mnemos-memory
description: Use when users or OpenClaw/ClawHub agents need to install, configure, self-bootstrap, troubleshoot, or operate Mnemos for persistent scoped agent memory, or when they mention Mnemos, agent memory, scoped memory, memory MCP tools, or memory automation.
---

# Mnemos Memory

Mnemos is a local-first memory layer for coding agents. Use this skill to guide users or OpenClaw agents onto the supported install path, explain the operating loop, and keep compatibility claims accurate.

## Default path

- Prefer `pip install "mnemos-memory[mcp]"` and `mnemos ui`.
- For OpenClaw / ClawHub, teach the agent to self-install `mnemos-memory[mcp]`, run `mnemos ui`, then wire `mnemos-mcp` to the canonical `MNEMOS_CONFIG_PATH` before relying on memory.
- Recommend SQLite as the supported persistent store.
- Recommend a real embedding provider (`openclaw`, `openai`, `openrouter`, or `ollama`) for production retrieval quality.
- Validate setup with the control-plane smoke check or `mnemos-cli doctor`.

## Claim discipline

- Safe to claim: local-first scoped memory, MCP tools, SQLite starter profile, Claude Code plugin flow, documented Codex flow.
- Be explicit that deterministic auto-memory is shipped for Claude Code via hooks.
- For Codex, Cursor, OpenClaw, and generic MCP hosts, do not imply automatic capture unless the host has its own automation or the user adds one.
- Do not present removed legacy backends as available runtime options.

## Workflow

1. Identify the host: Claude Code, Cursor, Codex, OpenClaw, or generic MCP.
2. If the repo is available locally, read `README.md`, `docs/MCP_INTEGRATION.md`, and `docs/codex.md` before answering.
3. Give the default install path first. Only fall back to manual config snippets if the user cannot use the control plane.
4. Explain the operating loop:
   - `mnemos_retrieve` at task start
   - `mnemos_store` for durable facts only
   - `mnemos_consolidate` before finishing substantial work
   - `mnemos_inspect` when a stored fact looks wrong
5. Read `references/hosts.md` for host-specific config snippets and caveats, especially the OpenClaw / ClawHub self-install flow when the agent must bootstrap itself.
6. Read `references/operations.md` for automation, capture-mode, storage guidance, and troubleshooting.

## Avoid

- Do not tell users to manually type memories as the primary workflow.
- Do not recommend `SimpleEmbeddingProvider` for production retrieval quality.
- Do not suggest external storage backends for Mnemos. Keep users on the SQLite path.
