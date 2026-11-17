# Pattern: Adaptive Intake

**Purpose:** Documents the reusable design pattern where a package accepts input in MULTIPLE formats and adapts its ingestion behavior accordingly — so users are never blocked by "wrong format" requirements.

---

## The Pattern

```
USER INPUT (any format)
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  INTAKE MODE DETECTION                                               │
│                                                                      │
│  Structured document? → Parse structure, fill gaps                    │
│  Raw/verbal?          → Ask structured questions                      │
│  Chain predecessor?   → Read structured output, minimal questions     │
│  Brownfield context?  → Focus on delta, existing constraints          │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼
NORMALIZED INTERNAL MODEL (same quality regardless of input mode)
```

**One sentence:** Accept whatever the user has — a polished document, a Slack message, a predecessor's output, or "we're extending system X" — and adapt ingestion to produce the same quality internal model.

---

## Where It's Used

| Package | Supported Input Modes |
|---------|----------------------|
| **AI-PILC** | Structured document / Raw verbal / ILC Idea Brief / Brownfield context |
| **AI-ADLC** | Full PIP (from AI-PILC) / Requirements + charter / Verbal description / Existing architecture (brownfield) |
| **AI-DWG** | Full AP (from AI-ADLC) / Any structured architecture docs / Existing codebase scan |
| **AI-GCE** | Full workspace (from AI-DWG) / Any workspace with `.kiro/steering/` / Minimal steering + baseline |
| **AI-ILC** | Verbal idea / One-liner / Feature request / Competitive observation / Technical improvement |
| **AI-POLC** | PIP + AP (chain) / Raw product vision / Feature list / Existing backlog |

---

## Why This Pattern Exists

**The problem it solves:** "You must provide input in format X before we can start" blocks adoption. Real users have:
- Meeting notes, not formatted requirements
- Existing docs from consultants, not AI-PILC output
- Verbal descriptions, not structured briefs
- Running systems, not blank-slate projects

**Without adaptive intake:** Users must re-format their existing materials to match tool expectations. This friction prevents adoption — especially for the first package in the chain (no predecessor output exists yet).

**With adaptive intake:** Bring whatever you have. The tool meets you where you are.

---

## Mode Detection Logic

Packages determine input mode through signals:

| Signal | Detected Mode | Package Behavior |
|--------|--------------|-----------------|
| Predecessor marker file found | Chain mode (richest) | Read structured output, ask minimal gaps |
| User provides a formatted document | Structured document mode | Parse structure, validate, ask about gaps |
| User provides conversation/notes/bullet points | Raw/verbal mode | Ask structured questions to extract requirements |
| User says "extending existing system" | Brownfield mode | Focus on what exists, what's changing, constraints |
| Mix of signals | Hybrid | Combine approaches (read what's structured, ask about what's verbal) |

---

## The Adaptation Spectrum

```
MOST STRUCTURED                                         LEAST STRUCTURED
     ←──────────────────────────────────────────────────────→

Chain predecessor  │  Formatted doc  │  Meeting notes  │  Verbal/one-liner
(full context,     │  (some structure,│  (partial info, │  (minimal info,
 minimal questions)│  some gaps)      │  many gaps)     │  full question set)
```

**Key insight:** The SAME internal model is produced regardless of input mode. What differs is:
- How much the user provides upfront
- How many questions the AI asks
- How long the ingestion stage takes

---

## Implementation Anatomy

### The Question Budget

Each input mode has a different question budget:

| Mode | Questions Asked | Why |
|------|:--------------:|-----|
| Chain predecessor | 0-3 (validation only) | Most context already captured by predecessor |
| Structured document | 5-10 (gap-filling) | Structure exists, but may have missing sections |
| Raw/verbal | 15-25 (full extraction) | Everything must be asked because nothing is pre-structured |
| Brownfield | 10-15 (context + delta) | What exists is known, what's changing must be captured |

### The Normalization Step

After intake (regardless of mode), the package normalizes into a consistent internal model:

```
AI-PILC Internal Model (after intake):
├── Requirements (functional + non-functional)
├── Constraints (technical, budget, timeline, regulatory)
├── Stakeholders (identified, even if list is short)
├── Input Quality Score (how much is verified vs. assumed)
├── Source Mode (logged in state file for downstream awareness)
└── Gaps Identified (what's still unknown, for later stages)
```

All subsequent stages work against this normalized model — they don't know or care which input mode produced it.

### The State File Records the Mode

```yaml
Source Type: structured-document  # or: chain-predecessor | verbal | brownfield
Input Quality: high  # or: medium | low (affects how many assumptions later stages can make)
```

Downstream packages see this and adapt (a low-quality verbal intake means more questions at architecture stage).

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Never reject input format | Rejection blocks adoption; always find a way to work with what's provided |
| Detect mode automatically | Don't make user choose "Mode A or Mode B?" — infer from the input itself |
| Normalize to same internal model | Downstream stages must work identically regardless of intake mode |
| Record input quality | Honesty about gaps enables better downstream decisions (ask more if input was thin) |
| Chain mode is still adaptive | Even with a predecessor, the PIP might be partial — handle gracefully |

---

## When to Apply This Pattern

Apply when:
- [ ] A package receives input from "the outside world" (not strictly from the previous chain package)
- [ ] Users will arrive with different levels of preparation
- [ ] Forcing a specific input format would block adoption
- [ ] The same quality of output is achievable regardless of input format (just with more/fewer questions)

Don't apply when:
- The package reads ONLY from a specific structured source (no human input variation)
- Input format is genuinely non-negotiable (e.g., a parser that needs valid JSON)
- The effort to support multiple modes exceeds the adoption benefit

---

## Related Documents

| Document | Location |
|----------|----------|
| Pattern: Graceful Standalone | `knowledge_docs/PATTERN_GRACEFUL_STANDALONE.md` |
| How PILC Workflow Engine Works | `knowledge_docs/HOW_PILC_WORKFLOW_ENGINE_WORKS.md` |
| How to Initiate a Project | `knowledge_docs/HOW_TO_INITIATE_A_PROJECT.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
