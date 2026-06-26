---
name: research-deep
description: 'Deep research skill that decomposes questions into parallel sub-queries, executes searches concurrently, selectively fetches high-value sources, and synthesizes structured answers with confidence ratings. Replaces slow sequential search-read-search loops with a planned, parallel-first methodology. Use when asked to "research", "deep dive", "investigate", "find out about", or any multi-source research task.'
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.2"
  tags:
    - research
    - web search
    - deep dive
    - information retrieval
    - parallel search
    - synthesis
    - fact checking
  triggers:
    - "research"
    - "deep dive"
    - "investigate"
    - "find out about"
    - "what do we know about"
    - "gather information on"
    - "research deep"
---

# Deep Research

Structured, parallel-first research methodology for AI agents. Turns vague questions into multi-source, evidence-backed answers in one pass instead of slow sequential search loops.

## The Problem This Solves

Most AI agents research like this:

```
Search "X" → read result → realize they need Y → search "Y" → read →
realize they need Z → search "Z" → read → finally answer
= 6+ round trips, 3+ minutes, redundant reads
```

This skill forces a better pattern:

```
Decompose question → 3-5 parallel searches → selective fetch (2-3 best) → synthesize
= 2 round trips, under 60 seconds, no redundancy
```

## When to Use This Skill

- Multi-faceted questions requiring information from multiple sources
- Competitive analysis, market research, technology comparisons
- Fact-checking claims that need cross-referencing
- "What's the current state of X?" questions
- Any research task where sequential searching would be slow

## When NOT to Use This Skill

- Simple factual lookups (just use one WebSearch)
- Questions answerable from the local codebase (use Grep/Glob instead)
- Tasks requiring real-time data feeds or APIs (use the appropriate API)

## Instructions

When a user asks you to research a topic:

### Step 1: Decompose (Think Before Searching)

Break the question into 3-5 specific, non-overlapping sub-queries. Each sub-query should target a different facet of the question.

**Rules:**
- Each sub-query must be a concrete search string, not a vague topic
- Sub-queries should cover: definition/basics, current state, key players/examples, controversy/limitations, and future direction
- If the user's question is already narrow, decompose by source type: official docs, community discussion, academic papers, news coverage

**Example decomposition:**

User asks: "Is WebAssembly ready for production server-side use?"

```
Sub-queries:
1. "WebAssembly server-side production 2026 case studies"
2. "WASI preview 2 stability limitations"
3. "WebAssembly vs containers performance benchmarks 2025 2026"
4. "Fermyon Cosmonic Wasmer production deployments"
5. "WebAssembly server criticisms problems developer experience"
```

Note: query 5 deliberately searches for the negative case. Always include at least one adversarial/critical sub-query to avoid confirmation bias.

### Step 2: Parallel Search

Execute ALL sub-queries simultaneously using WebSearch. Do not wait for one result before starting the next.

```
# CORRECT: all in one message, parallel execution
WebSearch("WebAssembly server-side production 2026 case studies")
WebSearch("WASI preview 2 stability limitations")
WebSearch("WebAssembly vs containers performance benchmarks 2025 2026")
WebSearch("Fermyon Cosmonic Wasmer production deployments")
WebSearch("WebAssembly server criticisms problems developer experience")
```

```
# WRONG: sequential, one at a time
WebSearch("WebAssembly server-side") → read → WebSearch("WASI") → read → ...
```

**Optional academic sources:** If the topic has academic relevance, add an arxiv search in the same parallel batch. Not all topics need this — skip for product/market/community questions.

### Step 3: Selective Fetch (Quality Over Quantity)

From all search results, pick only the 2-3 most information-dense sources to WebFetch. Do NOT fetch every result.

**Selection criteria (pick sources that):**
1. Contain original data, benchmarks, or primary research (not summaries of summaries)
2. Are from authoritative domains for the topic (official docs, known experts, peer-reviewed)
3. Were published recently (prefer last 12 months unless historical context needed)
4. Cover different angles (don't fetch 3 sources that say the same thing)

**Skip fetching when:**
- The search snippet already contains the key fact you need
- The source is a generic listicle or SEO-optimized filler article
- You already have enough evidence for high-confidence conclusions

### Step 4: Synthesize

Combine all findings into a structured output. Do NOT just list what each source said — synthesize across sources.

**Output format:**

```markdown
## Research: [Topic]

### Key Findings

1. **[Finding 1]** (1-2 sentences)
   - Evidence: [specific data point or quote] — [source]
   - Evidence: [corroborating or conflicting data] — [source]

2. **[Finding 2]**
   - Evidence: ...

3. **[Finding 3]**
   - Evidence: ...

### Confidence Assessment

| Finding | Confidence | Basis |
|---------|-----------|-------|
| Finding 1 | High/Medium/Low | [why: e.g., "3 independent sources agree" or "single source, no corroboration"] |
| Finding 2 | ... | ... |

### Gaps & Unknowns

- [What we could NOT find or verify]
- [Questions that remain open]
- [Potential biases in available sources]

### Sources

- [Title](URL) — [one-line relevance note]
- [Title](URL) — [one-line relevance note]
```

## Confidence Rating Guide

| Level | Criteria |
|-------|----------|
| **High** | 3+ independent sources agree, includes primary data or official documentation, no significant contradictions found |
| **Medium** | 2 sources agree, or 1 highly authoritative source, minor contradictions exist but are explainable |
| **Low** | Single source only, or sources conflict significantly, or information is outdated (>12 months), or topic is rapidly evolving |

## Anti-Patterns (Common Mistakes)

### 1. The Sequential Trap
```
# BAD: search, read, search, read, search, read
WebSearch("topic") → WebFetch(result1) → "hmm I need more" → WebSearch("topic detail") → ...
```
**Fix:** Plan all queries in Step 1, execute in Step 2. If Step 2 reveals a completely unexpected angle, one additional targeted search is acceptable — but never more than one follow-up round.

### 2. The Fetch-Everything Trap
```
# BAD: fetching 8 URLs "just in case"
WebFetch(url1), WebFetch(url2), WebFetch(url3), ... WebFetch(url8)
```
**Fix:** Max 3 fetches. If you need more than 3, your sub-queries were too vague. Refine queries instead of fetching more pages.

### 3. The Summary-of-Summaries Trap
```
# BAD: "According to source 1... According to source 2... According to source 3..."
```
**Fix:** Synthesize across sources. Lead with the finding, then cite evidence from multiple sources inline.

### 4. The Missing Adversarial Query
```
# BAD: only searching for positive/confirming information
"X benefits", "X advantages", "X success stories"
```
**Fix:** Always include at least one query like "X problems", "X criticism", "X limitations", "X vs alternatives".

## Example

**User:** "What's the current state of Rust in production web backends?"

**Step 1 — Decompose:**
```
1. "Rust web backend production 2026 companies using"
2. "Actix Axum web framework comparison benchmark 2025 2026"
3. "Rust backend developer experience hiring difficulty"
4. "Rust vs Go web server performance latency throughput"
5. "Rust web backend problems criticism compile time"
```

**Step 2 — Parallel search** (all 5 at once)

**Step 3 — Selective fetch** (pick best 2-3):
- Official Rust survey 2025 results (primary data)
- A detailed Axum vs Actix benchmark post (original benchmarks)
- Skip: generic "Why Rust is great" blog posts

**Step 4 — Synthesize:**

```markdown
## Research: Rust in Production Web Backends (March 2026)

### Key Findings

1. **Rust backend adoption is growing but remains niche** (~8-12% of new web projects)
   - Evidence: Rust Survey 2025 shows 34% of respondents use Rust for web/networking, up from 28% — rust-lang.org
   - Evidence: But Stack Overflow 2025 shows Rust at 8.2% for "used professionally" vs Go at 14.1% — stackoverflow.com

2. **Axum has emerged as the dominant web framework**
   - Evidence: Axum downloads surpassed Actix-web in Q3 2025, now 2.1x higher — lib.rs
   - Evidence: Tokio ecosystem integration gives Axum a compounding advantage — shuttle.rs blog

3. **Hiring remains the primary blocker for teams considering Rust backends**
   - Evidence: "Finding Rust web developers is 3-4x harder than Go" — CTO interview, InfoQ 2025
   - Evidence: Counterpoint — several companies report Rust attracts higher-quality candidates — r/rust

### Confidence Assessment

| Finding | Confidence | Basis |
|---------|-----------|-------|
| Growing but niche | High | Two independent surveys + download data |
| Axum dominant | High | Download metrics + ecosystem analysis |
| Hiring is blocker | Medium | Anecdotal (interviews), no systematic hiring data |

### Gaps & Unknowns

- No reliable data on Rust backend failure/migration stories (survivorship bias)
- Limited information on Rust backend performance at >10K RPS in production
- Hiring difficulty may vary significantly by region (no geographic breakdown found)
```

## Customization

This skill works with any search-capable tool. The core methodology (decompose → parallel search → selective fetch → synthesize) is tool-agnostic. Adapt the tool names to your environment:

| Tool Category | Default | Alternatives |
|--------------|---------|-------------|
| Web search | `WebSearch` | Any web search MCP tool |
| Page fetch | `WebFetch` | Any URL fetcher |
| Academic papers | arxiv MCP (optional) | Semantic Scholar, Google Scholar |
| Community sentiment | Reddit/HN search (optional) | Any forum search |

## Tips for Best Results

1. **Time-bound your queries** — Add the current year to searches to avoid stale results
2. **Name specific entities** — "Vercel Edge Functions cold start" beats "serverless performance"
3. **Include version numbers** — "React 19 server components" beats "React server components"
4. **One follow-up max** — If parallel results reveal a critical gap, one additional search round is acceptable. If you need two, your decomposition was wrong.
5. **Cite inline** — Every factual claim should have a source next to it, not in a separate section

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
