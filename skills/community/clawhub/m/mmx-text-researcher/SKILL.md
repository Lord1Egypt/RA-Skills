---
name: mmx-text-researcher
description: Deep research skill using MiniMax CLI (mmx). Activates when: (1) Arif asks to research, investigate, look up, find information, or deep-dive on a topic; (2) a question requires synthesis from multiple sources; (3) Arif needs structured output (JSON, tables, summaries); (4) any knowledge task that benefits from web search + synthesis. Uses mmx search + mmx text chat. NOT for simple factual lookups (use web_search tool directly).
metadata: {"openclaw": {"emoji": "🔍"}}
---

# MMX Text Researcher — Deep Research via MiniMax CLI

Use this skill when a question requires **investigation, synthesis, multi-source reasoning, or structured output**.

## Prerequisites

- `mmx` CLI must be authenticated: `mmx auth status`
- If not authenticated: `mmx auth login --api-key <key>`
- Check region: `mmx config show` (global vs CN)

## Core Research Loop

```
1. SEARCH  → mmx search "<query>" [--output json]
2. SYNTH   → mmx text chat --model MiniMax-Text-01 --message "Summarize from: <results>"
3. STRUCT  → mmx text chat --output json --message "Extract key facts as JSON"
4. VERIFY  → mmx search "<specific claim>" to cross-check
5. COMPILE → Final synthesis in requested format
```

## Commands Reference

### Web Search (structured JSON output)

```bash
mmx search "MiniMax AI latest developments"
mmx search query --q "specific fact to verify" --output json
```

### Deep Research Chat (MiniMax-Text-01 best for synthesis)

```bash
mmx text chat --model MiniMax-Text-01 --message "Research brief: <topic>. Provide structured output with: key findings, confidence level per finding, sources, and remaining unknowns."
```

### Streaming Research (for long investigations)

```bash
mmx text chat --model MiniMax-Text-01 --message "<research query>" --stream
```

### Multi-turn Research Thread

```bash
mmx text chat --message "I want to research X. Start by identifying the 5 most important sub-questions."
mmx text chat --message "Now investigate sub-question 1: <question>"
# ... continue threading
```

### Structured Output (JSON)

```bash
mmx text chat --model MiniMax-Text-01 --output json --message "Extract into JSON: { topic, findings: [{ claim, confidence, source }], gaps: [], next_steps: [] }"
```

### Fact Verification Loop

For claims made in previous research:
```bash
mmx search "specific claim to verify"
mmx text chat --message "Based on search results: does this support or refute the claim: <claim>? Cite sources."
```

## Output Format Options

Specify format in the prompt:
- `JSON` — structured machine-readable output
- `table` — tabular comparison or summary
- `brief` — executive summary (3-5 bullet points)
- `full` — comprehensive research report
- `verdict` — true/false/uncertain with reasoning

## Quality Checklist

- [ ] At least 2 independent sources per key claim
- [ ] Confidence level assigned per finding
- [ ] Unknowns/gaps explicitly stated
- [ ] Sources cited (URL or source name)
- [ ] Opposing views included if relevant

## Common Triggers

- "research X for me"
- "investigate this claim"
- "find information about"
- "deep dive into"
- "what is the current state of"
- "synthesize what we know about"
- "verify whether"
- "compare X vs Y"
