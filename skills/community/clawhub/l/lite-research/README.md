# lite-research

**Quick research agent using web search and fetch tools**

---

## Overview

This skill performs fast, focused research on any topic using advanced search strategies. It's designed to give you a solid overview without the overhead of multi-agent deep research.

**When to use:** User asks to "research [topic]" (not "deep research")

---

## How It Works

1. **Analyzes the topic** to identify key concepts, synonyms, and related terms
2. **Generates 2-5 strategic queries** using research-proven techniques
3. **Executes searches** with count=5 for each query
4. **Fetches and reads** the top results from each query
5. **Compiles findings** into a coherent summary with sources

---

## Search Strategy

The skill uses advanced search techniques rather than basic queries:

### Query Generation Techniques

| Technique | Example |
|-----------|---------|
| **Synonym variations** | `"artificial intelligence" OR "AI" OR "machine learning"` |
| **Overview/intro focus** | `"artificial intelligence" overview introduction basics` |
| **Recent developments** | `"artificial intelligence" 2024 2025 recent developments` |
| **Critical analysis** | `"artificial intelligence" challenges problems issues` |
| **Applications** | `"artificial intelligence" applications uses examples` |

### Search Best Practices Applied

- ✅ Uses **OR operators** for synonyms: `"climate change" OR "global warming"`
- ✅ **Quotation marks** for exact phrases
- ✅ **Both singular/plural** forms
- ✅ **Time constraints** when relevant
- ✅ **Multi-perspective** approach (overview, current, critical, applications)

---

## Example Usage

```
research renewable energy
research quantum computing
research climate change impacts
research machine learning ethics
```

---

## Output Format

The skill produces a structured summary containing:

- **Key concepts and definitions**
- **Current developments and trends**
- **Different perspectives and applications**
- **Notable challenges or controversies**
- **Citations with full URLs** (primary sources always linked)

---

## Key Design Decisions

### Why 5 queries maximum?

Balances thoroughness with efficiency. Five well-crafted queries typically cover:
1. Synonym variation
2. Overview/intro
3. Recent developments
4. Critical analysis
5. Applications

This provides comprehensive coverage without excessive API calls.

### Why no sub-agents?

Lite research is designed for quick overviews. Deep research (spawned as sub-agents) is for when you need exhaustive analysis. Lite research gives you the gist in seconds.

### Why advanced search strategies?

Basic queries like `"renewable energy"` return the same Wikipedia page every time. Strategic queries like:
- `"renewable energy" OR "clean energy" OR "green energy"`
- `"renewable energy" 2024 2025 "recent developments"`
- `"renewable energy" challenges problems limitations`

Find diverse sources and perspectives, giving you a more complete picture.

---

## When NOT to Use This Skill

- ❌ User asks for "deep research" → use `deep-research-pro` skill
- ❌ You need exhaustive, multi-source analysis
- ❌ You need citations from academic papers or primary documents
- ❌ You need verification of claims with rigorous fact-checking

