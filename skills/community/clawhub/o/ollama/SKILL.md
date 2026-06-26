---
name: Ollama
slug: ollama
version: 1.0.0
homepage: https://clawic.com/skills/ollama
description: Run, tune, and troubleshoot local Ollama models with reliable API patterns, Modelfiles, embeddings, and hardware-aware deployment workflows.
changelog: Initial release with local model setup, stable JSON output, custom model workflows, safer remote access, and recovery playbooks.
metadata: {"clawdbot":{"emoji":"🦙","requires":{"bins":["ollama"],"anyBins":["curl","jq"],"config":["~/ollama/","~/.ollama/"]},"os":["linux","darwin","win32"],"configPaths":["~/ollama/","~/.ollama/"]}}
---

## When to Use

User needs to install, run, integrate, tune, or debug Ollama for local or self-hosted model workflows. Agent handles smoke tests, model selection, API usage, Modelfile customization, embeddings, RAG fit checks, and safe operations.

Use this instead of generic AI advice when the blocker is specific to local runtime behavior: wrong model tag, broken JSON output, poor retrieval, slow inference, context sizing, GPU fallback, or unsafe remote exposure.

## Architecture

Memory lives in `~/ollama/`. If `~/ollama/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/ollama/
|-- memory.md          # Durable context and activation boundaries
|-- environment.md     # Host, GPU, OS, runtime, and service notes
|-- model-registry.md  # Approved models, tags, quants, and fit notes
|-- modelfiles.md      # Reusable Modelfile patterns and parameter decisions
|-- rag-notes.md       # Embedding choices, chunking, retrieval checks, vector dimensions
`-- incident-log.md    # Repeated failures, fixes, and rollback notes
```

## Quick Reference

Load only the file needed for the current blocker.

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Install and smoke-test workflow | `install-and-smoke-test.md` |
| Local API and OpenAI-compatible patterns | `api-patterns.md` |
| Modelfile creation and context control | `modelfile-workflows.md` |
| Embeddings and local RAG checks | `embeddings-and-rag.md` |
| Runtime operations and performance tuning | `operations-and-performance.md` |
| Failure recovery and incident triage | `troubleshooting.md` |

## Requirements

- Local `ollama` access on the target machine, or permission to guide installation.
- Enough RAM, VRAM, and disk for the exact model and context window being proposed.
- Explicit user approval before exposing Ollama beyond localhost, changing service managers, or deleting model files.
- Exact model tags and runtime facts must be verified with live commands such as `ollama list`, `ollama ps`, and `ollama show`.

Never assume model capabilities, context length, quantization, or GPU usage from memory alone.

## Operating Coverage

This skill is for practical Ollama execution, not abstract local-LLM discussion. It covers:
- local installs on macOS, Linux, and Windows
- CLI workflows for pull, run, copy, show, create, and remove
- REST API usage on `http://127.0.0.1:11434/api` and OpenAI-compatible usage on `/v1`
- hardware-aware model sizing, context tuning, and throughput tradeoffs
- Modelfile-based customization for prompts, parameters, adapters, and reproducible model names
- embeddings and local RAG pipelines where indexing, querying, and retrieval must stay consistent

## Data Storage

Keep only durable operational context in `~/ollama/`:
- host facts that materially change advice: OS, GPU class, CPU-only constraints, service manager, remote or local deployment
- approved model tags, copied aliases, quant choices, and context limits that worked in practice
- Modelfile defaults, JSON output patterns, and safe OpenAI-compatible mappings
- embedding model choices, vector dimensions, chunking defaults, and retrieval checks
- recurring failures such as partial pulls, CPU fallback, port conflicts, or broken upgrades

## Core Rules

### 1. Verify the Runtime Before Giving Advice
- Confirm `ollama` is installed and reachable before proposing any deeper fix.
- Start with the smallest factual checks: `ollama --version`, `ollama list`, `ollama ps`, and one minimal generation or `/api/tags` request.
- Treat "it runs" and "it runs correctly" as different states.

### 2. Pin Exact Model Names and Inspect Them Live
- Use exact tags, not vague family names, for anything reproducible or production-adjacent.
- Inspect the real model with `ollama show` or `/api/show` before claiming context length, quantization, or capabilities.
- Avoid silent drift from floating tags when stability matters.

### 3. Separate Runtime, Modelfile, and App Prompt Responsibilities
- Debug local behavior in layers: runtime first, then model definition, then application prompt.
- If output quality changed, check whether `SYSTEM`, `TEMPLATE`, or `PARAMETER` settings in the Modelfile are fighting the app prompt.
- Put durable defaults in a named model, not in ad hoc copy-pasted prompts.

### 4. Choose Models by Hardware and Latency Budget
- A model that technically loads but falls back to CPU or swaps memory is not a good fit.
- Use `ollama ps` to confirm processor split before promising performance.
- Keep separate defaults for chat, coding, extraction, vision, and embeddings instead of forcing one model to do everything.

### 5. Make API and Structured Output Flows Deterministic
- Prefer non-streaming responses when the next step needs strict parsing.
- Use `format: "json"` or a JSON schema, set low temperature, and validate the parsed result before taking downstream actions.
- For OpenAI-compatible clients, verify `/v1` assumptions instead of assuming every feature maps 1:1.

### 6. Treat Embeddings and RAG as a Single System
- Use the same embedding model for indexing and querying unless you intentionally migrate and re-index.
- Inspect retrieved chunks before blaming the model for weak answers.
- Fix chunking, metadata, top-k, and vector dimensions before increasing prompt size.

### 7. Treat Remote Access and Upgrades as Operational Changes
- Do not bind Ollama to non-localhost or open port `11434` without explicit approval and a minimal-risk network plan.
- Record service manager changes, environment variables, and rollback steps before upgrading.
- Protect model storage and disk headroom before large pulls or replacements.

## Ollama Traps

- Using `latest` everywhere -> upgrades silently change behavior and break reproducibility.
- Testing only with `ollama run` -> app integration still fails on `/api` or `/v1`.
- Assuming slow responses mean "bad model" -> often it is CPU fallback, oversized context, or disk pressure.
- Letting app prompts and Modelfile instructions fight each other -> outputs become inconsistent and hard to debug.
- Re-indexing with one embedding model and querying with another -> retrieval quality collapses without obvious errors.
- Exposing the API on a LAN without auth or scoping -> local convenience becomes a security problem.
- Chasing larger context before fixing retrieval or prompt shape -> memory use rises while answer quality barely improves.

## External Endpoints

Use external network access only when the task requires model downloads, official docs lookup, or optional cloud execution explicitly approved by the user.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://ollama.com/* | model identifiers, optional doc queries, and optional cloud API requests | Official docs, library lookups, model pulls managed by the Ollama runtime, and optional cloud execution |

No other data is sent externally.

## Security & Privacy

Data that leaves your machine:
- model identifiers and download requests when pulling models through Ollama
- optional prompts and attachments only if the user explicitly chooses `https://ollama.com/api` instead of local inference
- optional documentation lookups against official Ollama pages

Data that stays local:
- prompts and outputs served through the local Ollama runtime on the user machine
- durable workflow notes under `~/ollama/`
- local Modelfiles, retrieval notes, and performance baselines unless the user exports them

This skill does NOT:
- expose Ollama remotely without explicit approval
- store `OLLAMA_API_KEY` or other secrets in skill files
- mix local and cloud execution silently
- invent unsupported model features, GPU behavior, or API compatibility
- recommend remote installers or destructive cleanup without explaining risk first

## Trust

By using this skill, model pulls and optional cloud requests may go to Ollama infrastructure when the user explicitly chooses those paths.
Only install if you trust Ollama with that data.

## Scope

This skill ONLY:
- installs, verifies, operates, and troubleshoots Ollama workflows
- helps choose, pin, inspect, and customize models with reproducible patterns
- keeps local memory for host constraints, model defaults, and recurring failure fixes

This skill NEVER:
- claim that every Ollama model supports the same tools, context, or JSON reliability
- recommend unauthenticated remote exposure as a default
- treat local RAG quality as solved without checking embeddings, chunking, and retrieval results
- modify its own skill files

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `ai` - Frame when local Ollama is the right fit versus cloud inference.
- `models` - Compare local model families, sizes, and capability tradeoffs before pinning defaults.
- `api` - Reuse robust HTTP request, retry, and parsing patterns around local services.
- `embeddings` - Extend vector search and chunking strategy beyond the Ollama runtime itself.
- `langchain` - Integrate Ollama into multi-step chains, agents, and retrieval pipelines.

## Feedback

- If useful: `clawhub star ollama`
- Stay updated: `clawhub sync`
