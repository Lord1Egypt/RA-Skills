# Pattern: Graceful Standalone (OR-Input)

**Purpose:** Documents the reusable design pattern where every package in the chain works independently — accepting EITHER its predecessor's structured output OR raw equivalent input directly from the user — so the chain enriches quality without mandating full traversal.

---

## The Pattern

```
PACKAGE INPUT
        │
        ├── Path A: Predecessor output detected (rich, structured)
        │   └── Read state file, read guaranteed files, minimal questions
        │
        └── Path B: No predecessor detected (standalone mode)
            └── Accept raw input, ask structured questions to fill gaps
```

**One sentence:** Every package works alone — the chain is an enrichment layer, not a dependency chain.

---

## Where It's Used

| Package | With Predecessor (Path A) | Without Predecessor (Path B) |
|---------|--------------------------|------------------------------|
| **AI-PILC** | Reads AI-ILC Idea Brief (evaluation already done) | Accepts raw requirements in any format |
| **AI-ADLC** | Reads PIP from AI-PILC (requirements, constraints, risk captured) | Accepts requirements + charter directly |
| **AI-DWG** | Reads AP from AI-ADLC (full architecture) | Accepts any structured architecture docs |
| **AI-GCE** | Reads workspace from AI-DWG (full steering) | Reads any workspace with `.kiro/steering/` |
| **AI-TGE** | Reads AP + DW (full context) | Works with whatever exists (even just test files) |
| **AI-POLC** | Reads PIP and/or AP (requirements + architecture) | Accepts raw product vision or feature list |

---

## Why This Pattern Exists

**The problem it solves:** If packages REQUIRE their predecessor's output, then:
- Users can't enter the chain mid-way ("I already have architecture docs — I just need DWG")
- A missing package blocks the entire downstream chain
- Teams that don't need full initiation are forced through it anyway
- Adoption barrier is "run ALL packages" instead of "run the ONE you need"

**The anti-pattern it prevents:** Hard dependencies between packages that force sequential execution. Real teams have existing artifacts from various sources — specs from product managers, architecture from consultants, requirements from contracts. The chain shouldn't ignore those.

**The test:** "Can a user install ONLY this package and get value from it without running any other AI-* package first?" If no → standalone mode is missing.

---

## How the Two Paths Differ

### Path A: Predecessor Detected

```
1. Scan for marker file → FOUND
2. Read state file (depth, status, configuration)
3. Read guaranteed output files (requirements, architecture, etc.)
4. Inherit depth level
5. Ask MINIMAL clarifying questions (most context already captured)
6. Proceed with rich input
```

**Advantage:** Faster, richer context, fewer questions, better output quality.

### Path B: Standalone Mode

```
1. Scan for marker file → NOT FOUND
2. Detect input mode (structured doc? verbal? brownfield?)
3. Ask STRUCTURED questions to capture context the predecessor would have provided
4. User selects depth level (no inheritance)
5. Build internal model from answers
6. Proceed (may need more interaction to reach same quality)
```

**Advantage:** Works without prerequisites; user enters with whatever they have.

---

## Quality Difference Between Paths

| Dimension | Path A (chain) | Path B (standalone) |
|-----------|:---:|:---:|
| Questions asked | Fewer (context inherited) | More (must capture from scratch) |
| Output quality | Higher (richer input context) | Good (but may miss nuances) |
| Session time | Shorter | Longer (more interaction needed) |
| Consistency with prior stages | Guaranteed (same data) | Depends on user input accuracy |
| Traceability | Full chain lineage | Starts fresh from this package |

**Key insight:** Standalone mode works — it just requires more user interaction to reach the same quality level. The chain is an efficiency multiplier, not a correctness prerequisite.

---

## The Input Mode Detection Pattern

When a package starts in standalone mode, it detects what kind of input the user provides:

| Input Mode | Detection Signal | Adaptation |
|-----------|-----------------|-----------|
| **Structured document** | User provides a formatted file (markdown, PDF, spreadsheet) | Parse structure, ask gap-filling questions |
| **Raw/verbal** | User describes in conversation | Ask structured questions to extract key elements |
| **Brownfield** | User says "extending existing system X" | Focus on delta, existing constraints, extend-vs-replace |
| **Partial predecessor** | Some predecessor artifacts exist but incomplete | Use what's available, supplement with questions |

---

## Implementation Rules

1. **Detection before prompting** — always try to find the predecessor's marker before asking the user for input. Don't assume standalone.

2. **Graceful degradation, not failure** — if predecessor output is found but INCOMPLETE (partial PIP, incomplete AP), use what's available and supplement with questions. Don't reject partial input.

3. **Never require the chain** — no error message should say "you must run AI-PILC first." Instead: "I'll ask some additional questions to capture the context that AI-PILC would normally provide."

4. **Document the delta** — in standalone mode, document what additional questions were asked that wouldn't have been needed with the predecessor. This helps users understand the value of the chain.

5. **State file records the path** — `Input Mode: Full PIP Handoff` vs. `Input Mode: Standalone (raw requirements)` — downstream packages know which path was taken.

---

## Entry Points (Chain Position → Standalone Capability)

| Entry Point | What You Skip | What You Provide Instead |
|-------------|--------------|--------------------------|
| Start at AI-ADLC | Skip initiation (PILC) | Provide requirements + constraints directly |
| Start at AI-DWG | Skip initiation + architecture | Provide architecture docs in any format |
| Start at AI-GCE | Skip everything upstream | Create minimal steering + let GCE derive from baseline |
| Start at AI-POLC | Skip initiation | Provide product vision or feature list directly |

---

## When to Apply This Pattern

Apply when:
- [ ] The package is part of a chain (has a predecessor)
- [ ] Users legitimately have input from sources other than the predecessor
- [ ] Forcing the full chain would be an adoption barrier
- [ ] The package CAN produce useful output without predecessor context (just with more questions)

Don't apply when:
- The predecessor's output is technically necessary (can't generate without it)
- Standalone mode would produce dangerously incomplete output
- The domain genuinely requires sequential progression (rare)

---

## Related Documents

| Document | Location |
|----------|----------|
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| Pattern: Marker File Detection | `knowledge_docs/PATTERN_MARKER_FILE_DETECTION.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
