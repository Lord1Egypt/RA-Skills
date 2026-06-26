# probe-first-research

A deep research skill for OpenClaw / ClawHub that uses a **probe-first methodology**: before committing to expensive full-page fetches, it runs a fast snippet-only reconnaissance pass to map the information landscape.

## Why Probe First?

Existing research skills either:
- **Plan blind** (decompose the question from closed-book knowledge, then search) — risks missing what's actually out there
- **Search blind** (immediately deep-dive into every result) — wastes effort on low-value sources

This skill does neither. It runs 2-3 cheap searches, reads only snippets (~10 seconds), then makes informed decisions about where to go deep.

## Five-Phase Workflow

| Phase | Name | What happens | Cost |
|-------|------|-------------|------|
| 1 | **Probe** | 2-3 searches, snippet-only | ~10 sec, zero fetches |
| 2 | **Orient** | Analyze probe, plan sub-questions, confirm with user | [STOP POINT] |
| 3 | **Deep Search** | Targeted fetch + 2-round iteration | Main cost here |
| 4 | **Synthesize** | Cross-topic integration, conflict resolution | Analysis |
| 5 | **Deliver** | Structured report with confidence levels | [STOP POINT] |

## Key Features

- **Low-cost reconnaissance** before committing resources
- **2 user checkpoints** — confirm direction after probe, review final report
- **Automatic multi-agent escalation** — spawns parallel agents for complex topics (4+ sub-questions)
- **Anti-hallucination protocol** — every claim needs a source; single-source numbers get cross-verified
- **Confidence labeling** — HIGH / MEDIUM / LOW / SPECULATIVE on all findings
- **Freshness management** — flags stale sources, applies date filters for time-sensitive topics
- **Language matching** — output follows the user's input language

## Installation

Install via the OpenClaw plugin marketplace, or add directly:

```bash
openclaw install probe-first-research
```

## Usage

```
/probe-first-research What are the current approaches to LLM inference optimization?
```

The skill will:
1. Probe the topic with 2-3 snippet-only searches
2. Present findings and a research plan for your approval
3. Execute targeted deep searches based on your confirmed plan
4. Deliver a structured report with sources and confidence levels

## Requirements

- OpenClaw / Claude Code environment
- `web_search` and `web_fetch` tools available
- `sessions_spawn` available (optional, for multi-agent mode)

## License

MIT
