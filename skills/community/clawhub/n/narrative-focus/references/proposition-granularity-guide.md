# Proposition Granularity Guide

## The Problem

The same technical detail can be read at different granularities, and different granularities produce different substitution test results.

**Example — Positional Encoding in a Transformer article:**

| Granularity | Proposition | Substitution Test | Role |
|-------------|-------------|-------------------|------|
| Conceptual | "Positional encoding provides sequence order information" | Replacing with "no position info" breaks the model entirely | Architectural |
| Mathematical | "Sine/cosine functions implement position encoding" | Replacing with learned embeddings or RoPE changes implementation but not core behavior | Configurable |

Both readings are valid. The question is: **which one is the article actually asserting?**

## The Rule: Match the Article's Elaboration Depth

The correct granularity is determined by **how the article treats the detail**, not by the detail's inherent nature.

1. **If the article devotes a full section to the math** → read at the mathematical level. The article is asserting the math matters.
2. **If the article mentions the concept and moves on** → read at the conceptual level. The article is asserting the concept matters.
3. **If the article explains both** → read at the level it spends more time on.

## Decision Flowchart

```
How does the article treat this detail?
│
├─ Full section with code/formulas/diagrams
│  → Read at the elaborated level
│  → Apply substitution test to the elaborated proposition
│
├─ One paragraph, then moves on
│  → Read at the conceptual level
│  → Apply substitution test to the conceptual proposition
│
├─ Mentioned in a list or table only
│  → Read at the conceptual level
│  → Likely Configurable regardless of result
│
└─ Unclear / mixed signals
   → Default to the conceptual level
   → If ambiguous, flag for human review
```

## Worked Examples

### Example 1: JSX Compilation (React article)

**Detail**: "JSX is `React.createElement()` syntax sugar"

**Article A** — devotes a full section to Babel transformation, shows before/after code:
- Granularity: compilation level
- Proposition: "JSX compiles to specific function calls, not a template language"
- Substitution: Replace with "JSX compiles to a virtual DOM builder" → user writes JSX the same way → **Transport**
- This article is telling the reader about the **compilation mechanism**

**Article B** — one paragraph, uses JSX to explain component model:
- Granularity: conceptual level
- Proposition: "JSX has no independent runtime semantics, it's just JS"
- Substitution: Replace with "JSX has its own directive system" → changes how reader thinks about components → **Architectural**
- This article is telling the reader about **what JSX means for the programming model**

### Example 2: Fiber Tree Traversal (React event system)

**Detail**: Fiber nodes are traversed during event dispatch

**Article A** — shows Fiber node data structure, walks through traversal algorithm:
- Granularity: implementation level
- Proposition: "Events are dispatched by walking Fiber child/sibling/return pointers"
- Substitution: Replace with "Events dispatched via DOM tree walk" → Fragments/Providers lose handlers → **Architectural**

**Article B** — mentions Fiber traversal in a flow chart step:
- Granularity: conceptual level
- Proposition: "React walks its internal tree, not the DOM, to find handlers"
- Substitution: Same result → **Architectural**

In this case, both granularities give the same result. That's fine — it means the concept is robustly Architectural regardless of how you read it.

### Example 3: Write Barrier / Card Marking (V8 GC article)

**Detail**: V8 uses card marking (512-byte cards) to track cross-generational references

**Article A** — full section on card marking internals:
- Granularity: implementation level
- Proposition: "V8 uses 512-byte card granularity for cross-gen ref tracking"
- Substitution: Replace with "remembered sets with pointer-level granularity" → GC behavior changes in edge cases but user code unaffected → **Transport**

**Article B** — one sentence: "V8 tracks cross-generational references via write barriers":
- Granularity: conceptual level
- Proposition: "Cross-generational references need explicit tracking for GC correctness"
- Substitution: Replace with "No cross-gen tracking" → GC becomes incorrect → **Architectural**

Here the granularity difference **changes the result**. The article's own treatment is the tiebreaker.

## When Granularity Ambiguity Persists

If you genuinely cannot determine the article's intended granularity:

1. **Check the title/abstract**: If they promise "deep dive" or "internals", lean toward implementation level. If they promise "understanding" or "explained", lean toward conceptual level.
2. **Check the audience**: Beginner-oriented → conceptual level. Expert-oriented → implementation level.
3. **Default to conceptual**: When in doubt, read at the conceptual level. It's safer to over-detect misalignment than to miss it.
4. **Flag for human review**: Mark the item as `⚠️ Granularity Ambiguous` in the detection report and present both readings.
