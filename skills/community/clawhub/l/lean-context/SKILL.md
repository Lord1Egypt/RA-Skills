---
name: token-optimizer
description: |
  Reduce token usage in AI agent systems (Claude Code, OpenClaw, GPT Codex, Cursor, Windsurf, Aider, etc.) by applying context compression, selective loading, prompt deduplication, caching strategies, and efficient tool definitions. Use when: (1) the user wants to cut AI costs or token burn, (2) optimizing CLAUDE.md, AGENTS.md, system prompts, or skill files for size, (3) designing token-efficient agent architectures, (4) auditing a project or config for context bloat, (5) building skills or prompts that minimize context window usage, (6) asking about context engineering, prompt compression, LLMLingua, compaction, or sub-agent patterns for token savings. Triggers on: "reduce tokens", "optimize tokens", "token usage", "context bloat", "prompt compression", "context engineering", "token audit", "cut costs", "token-efficient", "compact context".
---

# Token Optimizer

Cut token usage without cutting quality. Every technique below is battle-tested in production Claude Code, OpenClaw, and agentic systems.

## The 3 Token Drains (fix these first)

1. **Tool output accumulation** — Every file read, shell command, and MCP response appends *full output* to context permanently. A 10K-line log file stays in context for every subsequent message. This is the #1 silent drain.
2. **Context compounding** — The model re-reads the entire conversation on every turn. Message 50 costs more than message 5 because it re-reads 49 prior messages. Long sessions become token furnaces.
3. **System prompt baseline** — CLAUDE.md / AGENTS.md / system prompts load before every single request. A 5,000-token config file costs 5,000 tokens per turn, forever.

## Strategy 1: Slash System Prompt Size

Target: **under 500 tokens** for primary config files.

```
# CLAUDE.md / AGENTS.md template (good — ~150 tokens)
## Rules
- TypeScript strict mode
- Test every new function
- Follow existing patterns

## Key Files
- API routes: src/api/README.md
- DB schema: docs/schema.md
- Style guide: docs/style-guide.md
```

**Principles:**
- Give the *shape* of the project, not the full docs
- Use file pointers instead of inline documentation
- Link to reference files — the model reads them only when needed
- 3-5 rules + 3-5 file pointers is the sweet spot

## Strategy 2: Selective Loading (Progressive Disclosure)

Never load everything upfront. Use a three-tier system:

| Tier | When loaded | Token cost |
|------|------------|------------|
| Metadata (name+description) | Always | ~100 words |
| Core instructions (SKILL.md body) | On trigger | <5K words |
| Reference files | On demand | Unlimited |

**Implementation patterns:**

**File pointers over inline content:**
```
# Bad: inline everything
## API Reference
[2000 lines of API docs]

# Good: pointer + on-demand load
## API Reference
See docs/api.md — load only when working on API endpoints.
```

**Domain-split references:**
```
skill/
├── SKILL.md (core workflow only)
└── references/
    ├── aws.md      # load only for AWS tasks
    ├── gcp.md      # load only for GCP tasks
    └── azure.md    # load only for Azure tasks
```

**Conditional loading via grep patterns:**
For large reference files, include search patterns in SKILL.md:
```
# BigQuery Metrics
See references/metrics.md. Search patterns:
- Revenue queries: grep "revenue|billing" references/metrics.md
- User analytics: grep "cohort|retention|churn" references/metrics.md
```

## Strategy 3: Compaction & Session Hygiene

**When to compact vs clear:**
- `/compact` — Context is long but thread is still relevant. Summarizes and restarts from summary.
- `/clear` — Switching tasks entirely. Wipes everything. Clean slate.

**Rules:**
- New topic = new session. No exceptions.
- Point at specific files, never "read the codebase"
- Batch related tasks in one prompt: "Fix bug, refactor, add tests" > three separate prompts
- Use scripts for data you'll read yourself — keep the agent out of the loop

## Strategy 4: Efficient Tool Definitions

Tools are context too. Every tool definition loads on every request.

**Principles:**
- Minimal viable tool set — if a human can't tell which tool to use, the model can't either
- CLI > MCP when possible: `head -20 file.log` (10 tokens) vs MCP JSON response (1000+ tokens)
- Tools should return summaries, not raw dumps
- Disconnect unused MCP servers — per-request overhead is real

**Tool output compression:**
```
# Bad: full JSON dump
{"status":"success","data":{"items":[...500 lines...],"meta":{"page":1,"total":847}}}

# Good: structured summary
"847 items found. First 5: [names]. See full results in .cache/search.json"
```

## Strategy 5: Prompt Compression Techniques

### Extractive Compression (low effort, good ROI)
Select relevant sentences, discard the rest. Best for narrative documents.
```
# Before: 500 tokens
Customer John reported unstable internet for 3 days with video call disruptions.
Support ticket #4521 opened on 2026-04-15. Multiple attempts to reset router failed.

# After (extractive): 30 tokens
John: unstable internet 3 days, video call disruptions, router reset failed.
```

### Selection-Based Compression (chunk-level filter)
Keep or discard entire chunks. Best for factual/citation-heavy content. Zero rewrite cost.
```
# Approach: filter chunks by relevance score, only pass top-k to model
relevant_chunks = [c for c in retrieved if c.score > 0.75][:3]
```

### LLMLingua-style Token-Level Compression
Uses a small model to remove low-information tokens. Up to 20x compression with <2% quality loss.
- Use for: ICL examples, retrieved documents, long instructions
- Don't use for: code, structured data, exact citations
- Libraries: `llmlingua` (Python), `LLMLingua2`

## Strategy 6: Deduplication Patterns

**Across context:**
- Never repeat instructions already in system prompt
- Reference previous context by turn number instead of re-stating: "as discussed in turn 3"
- Deduplicate few-shot examples — 3 diverse examples > 10 similar ones

**Across sessions:**
- Store shared context in files, not in conversation
- Use memory files (`memory/*.md`) for cross-session continuity instead of re-explaining
- Hash-check before loading: if a file hasn't changed, use cached summary

**Across tools:**
- Don't read the same file twice — reference previous read
- Use `jq` to extract specific fields instead of loading full JSON
- Pipe commands: `grep ERROR log.txt | head -5` instead of `cat log.txt`

## Strategy 7: Caching & Architecture

**Prompt caching** (provider-level):
- Anthropic: automatic prompt caching for repeated prefixes (system prompts, tools)
- OpenAI: cached responses for identical prompts
- Strategy: structure prompts so static content comes first, dynamic content last

**Sub-agent architecture:**
```
Main agent (clean context, ~2K tokens)
├── Sub-agent 1: deep research (uses 50K tokens, returns 1K summary)
├── Sub-agent 2: code generation (uses 30K tokens, returns diff)
└── Sub-agent 3: testing (uses 20K tokens, returns pass/fail + details)
```
Each sub-agent explores extensively but returns only distilled results. Main agent stays lean.

**Model-tiering:**
- Haiku/fast models: formatting, lookups, mechanical edits
- Mid-tier: implementation, tests, explanations
- Top-tier: architecture decisions, complex reasoning, multi-file refactors

## Strategy 8: Agent-Specific Optimizations

**OpenClaw:**
- HEARTBEAT.md: Keep under 200 tokens. Reference external files for detailed checks.
- MEMORY.md: Curated, not raw. Review monthly. Remove stale entries.
- SOUL.md / USER.md: Load every session. Keep tight.
- Skills: Only the SKILL.md body loads on trigger. Put details in `references/`.
- Tool output: Use `jq`, `head`, `tail`, `grep` to scope output before it enters context.
- Write to files instead of returning large outputs in chat.

**Claude Code:**
- `.claudeignore` — Exclude node_modules, build artifacts, lock files, data files
- `context-mode` MCP plugin — Automatically compresses MCP tool outputs
- `/compact` after 20-30 messages or when switching sub-tasks
- `/model` to switch tiers mid-session (Haiku for lookups, Sonnet for implementation, Opus for architecture)
- `MAX_THINKING_TOKENS=8000` env var to cap extended thinking budget
- Skills load on-demand only — install freely, they don't add baseline cost

**General (applies to all agents):**
- `.gitignore` pattern for AI: exclude binaries, media, large generated files
- Structured output (JSON, YAML) > unstructured prose for tool responses
- `--no-ask-user` / `--allow-all` flags reduce confirmation round-trips

## Quick Audit Checklist

Run this against any AI project:

```
Token Audit:
□ System prompt / config files under 500 tokens?
□ Reference docs in separate files, not inline?
□ Tool outputs scoped (jq/head/grep), not raw dumps?
□ Sessions reset between topics?
□ MCP servers limited to active ones only?
□ Few-shot examples: 3 diverse > 10 similar?
□ Sub-agents used for deep exploration work?
□ Model tier matches task complexity?
□ Caching enabled for static prompt prefixes?
□ Deduplication: no repeated instructions across context layers?
□ .claudeignore / .gitignore excluding non-essential files?
□ Extended thinking budget capped for simple tasks?
```

## Strategy ROI Matrix

| Strategy | Effort | Savings | Best For |
|----------|--------|---------|----------|
| Slash system prompt | Low | 10-30% baseline | Every project |
| Selective loading | Medium | 40-70% per-query | Multi-domain agents |
| Compaction | Low | 50-80% long sessions | Coding agents |
| Efficient tools | Medium | 50-90% MCP usage | Tool-heavy workflows |
| Prompt compression | High | Up to 20x on docs | RAG, research agents |
| Deduplication | Low | 10-25% per session | All agents |
| Caching & sub-agents | High | 30-60% overall | Production systems |
| Model tiering | Low | 3-5x per-query cost | All multi-model setups |

## References

For deeper implementation details — LLMLingua integration code, LangChain compression pipelines, TikToken measurement, sub-agent architecture patterns, semantic deduplication, and dollar savings formulas — see [references/compression-deep-dive.md](references/compression-deep-dive.md).
