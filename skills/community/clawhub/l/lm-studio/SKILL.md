---
name: LM Studio
slug: lm-studio
version: 1.0.0
homepage: https://clawic.com/skills/lm-studio
description: Run and integrate LM Studio with local model lifecycle control, OpenAI-compatible APIs, embeddings, and MCP-aware workflows.
changelog: Initial release with local server workflows, model lifecycle checks, API recipes, MCP guidance, and troubleshooting for LM Studio.
metadata: {"clawdbot":{"emoji":"🧪","requires":{"bins":["curl","jq"]},"os":["linux","darwin","win32"],"configPaths":["~/lm-studio/"]}}
---

## When to Use

User wants to run local models with LM Studio, connect an app to its local server, or debug weak local inference behavior.

Use this for server readiness, model loading, OpenAI-compatible API integration, embeddings, MCP setup, and local-first operating decisions.

## Architecture

Memory lives in `~/lm-studio/`. If `~/lm-studio/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/lm-studio/
├── memory.md         # Activation, preferred port, known-good defaults
├── server-notes.md   # Reachability checks and server mode notes
├── model-profiles.md # Verified models by workload
└── incidents.md      # Repeated failures and confirmed fixes
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup behavior and activation boundaries | `setup.md` |
| Memory schema and status states | `memory-template.md` |
| Server startup and smoke tests | `server-workflows.md` |
| Download, load, unload, and swap models | `model-lifecycle.md` |
| OpenAI-compatible request patterns | `api-recipes.md` |
| MCP connection patterns and guardrails | `mcp-playbooks.md` |
| Symptom-based debugging | `troubleshooting.md` |

## Requirements

- LM Studio or `llmster` is already installed on the machine.
- `curl` and `jq` are available for smoke tests and response inspection.
- `lms` is optional but preferred for repeatable server and model operations.
- Keep requests local by default; only add remote MCP servers or network exposure when the user explicitly asks.

## Core Rules

### 1. Prove the server is reachable before changing client code
- Use `server-workflows.md` to confirm the actual port, endpoint reachability, and model visibility.
- "LM Studio is open" is not enough. Require one real request to succeed before touching integration code.

### 2. Separate downloaded, listed, loaded, and active models
- Use `model-lifecycle.md` for discovery, loading, unloading, and verification.
- Never assume a downloaded filename, API model id, CLI identifier, and active runtime instance are the same thing.

### 3. Prefer OpenAI-compatible endpoints for app integration
- Start from `api-recipes.md` and change only the base URL and model identifier before rewriting an existing client.
- Verify each workload separately: `responses`, `chat/completions`, `embeddings`, or `completions`.

### 4. Match model size and context to machine limits
- Treat slow first token, OOM, and context overflow as runtime-fit problems first, not prompt problems first.
- Reduce model size, quantization burden, or context length before escalating complexity.

### 5. Validate after every runtime change
- After loading a new model, changing context length, or altering server settings, run one end-to-end smoke test.
- Record the known-good combination in memory so the agent can reuse it instead of rediscovering it.

### 6. Treat MCP as a separate risk layer
- Use `mcp-playbooks.md` to connect servers, but debug model serving and MCP behavior independently.
- Never install untrusted MCP servers or silently route local data to remote endpoints.

### 7. Escalate beyond local when the task exceeds the local setup
- LM Studio is strong for privacy-sensitive work, offline execution, extraction, and controlled agent loops.
- For unsupported capabilities or repeated quality failures, say so explicitly and recommend a stronger remote path.

## Common Traps

- Assuming port `1234` without checking reachability -> integrations fail even though the app looks healthy.
- Treating `GET /v1/models` as proof a model is ready -> Just-In-Time listings can appear before a usable runtime is confirmed.
- Reusing cloud model names in local requests -> the client is fine, but the local model identifier is wrong.
- Forcing JSON, tools, or vision on an unverified local model -> failures get blamed on prompts instead of capability mismatch.
- Leaving large models loaded while debugging another issue -> RAM or VRAM pressure hides the real cause.
- Installing random MCP servers -> privacy and system access boundaries disappear quickly.

## Security & Privacy

Data that leaves your machine:
- None by default for local `localhost` server calls.
- Optional model downloads or MCP servers follow the user's explicit configuration, not this skill's default path.

Data that stays local:
- Prompt content sent to the LM Studio server running on the same machine.
- Notes stored in `~/lm-studio/` if the user wants persistent context.

This skill does NOT:
- Assume remote access is safe by default.
- Store secrets in skill memory files.
- Install MCP servers or open network access without explicit user intent.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `models` — Choose models by workload, context budget, and quality tradeoffs.
- `api` — Shape request payloads, retries, parsing, and integration debugging.
- `self-host` — Operate local infrastructure with practical reliability and security habits.
- `open-router` — Escalate from local-first execution to routed cloud models when capability gaps matter.
- `docker` — Package helper services or MCP servers consistently on the local machine.

## Feedback

- If useful: `clawhub star lm-studio`
- Stay updated: `clawhub sync`
