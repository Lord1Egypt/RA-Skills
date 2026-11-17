# How To Skip or Reorder Packages

**Purpose:** Shows how to use AIFLC's AI-* PDLC Family when you *don't* want to run every package in the default order — entering the chain partway, skipping packages you don't need, feeding a package only part of its inputs, and changing the sequence to fit your project. The family is built so you can do all of this without fighting it; this guide is the practical how-to.

---

## The Principle You're Relying On

Every package works alone. The chain is an **enrichment layer, not a hard dependency** — running the package before it makes a package's job easier and richer, but no package *requires* its predecessor. Each one looks for its predecessor's **marker file**; if the marker is there it reads that rich input, and if it isn't, it switches to **standalone mode** and asks you structured questions instead. There is deliberately no "you must run package X first" error anywhere in the family.

That single design choice is what makes skipping and reordering safe.

---

## Skipping: Three Ways

### Way 1 — Enter the chain at the package you need

Install and run only the package that does the job you want, and give it your own input instead of the skipped package's output.

| Enter at | You skip | You provide instead |
|----------|----------|---------------------|
| **AI-ADLC** | Initiation (AI-PILC) | Requirements + constraints directly |
| **AI-DWG** | Initiation + design | Architecture docs in any format |
| **AI-GCE** | Everything upstream | Any workspace with a `.kiro/steering/` folder |
| **AI-POLC** | Initiation | A product vision or feature list |
| **AI-UXD** | Initiation + backlog | A product brief or feature list to design around |

When you enter standalone, the package detects what kind of input you gave it — a structured document, a verbal description, or an existing (brownfield) codebase — and adapts its questions accordingly.

### Way 2 — Feed AI-DWG only part of its inputs

AI-DWG composes a development workspace from up to three inputs — the Architecture Package, the Product Backlog Package, and the UX Design Package. It accepts **any non-empty subset (one, two, or all three)**. It generates only the output clusters whose input is present, and for every absent input it shows a **quality-impact disclosure and asks for your approval** before proceeding.

So you can run `AI-ADLC → AI-DWG` and skip UX and backlog entirely — DWG builds the architecture-derived workspace and tells you what the missing inputs would have added.

### Way 3 — Go hybrid

You don't have to pick one mode for the whole project. Mix chain and standalone per package:

| Example | What you do |
|---------|-------------|
| Structured front, governance later | Run AI-PILC → AI-POLC → AI-ADLC → AI-DWG as a chain, then install AI-GCE standalone on the workspace whenever you're ready. |
| Bring-your-own architecture | You already have architecture docs → enter at AI-DWG, then let AI-DWG → AI-GCE chain forward from there. |
| Partial chain entry | You already have a Project Initiation Package → enter at AI-POLC and let the sequence flow forward. |

---

## Reordering: Two Levers

### Lever 1 — Provide inputs in the order you actually have them

Because every package accepts raw input, you are not locked into the default `AI-POLC → AI-UXD → AI-ADLC` order. For a backend-heavy or API-first product where the architecture should lead, running `AI-POLC → AI-ADLC → AI-UXD` is a legitimate variant. The family optimizes for the product-led default but does not forbid context-sensitive reordering — you simply run each package with whatever inputs you have on hand.

### Lever 2 — Drive a custom flow with AI-FLO

AI-FLO is the family's router. It supports configurable topology modes and an exceptions/overrides path, so you can override the default routing and tell it the sequence you want. When a step's required inputs aren't ready yet, AI-FLO flags the conflict (flag-and-hold) rather than dispatching blindly — so you reorder intentionally, not by accident.

---

## What It Costs You

Skipping and reordering are allowed, but the family surfaces the trade-off rather than hiding it. None of these block you — they're the price of stepping off the golden path:

| Trade-off | What happens |
|-----------|--------------|
| **More questions** | A standalone package must extract context the skipped predecessor would have handed over, so intake is longer. |
| **Less traceability** | You lose the lineage that lets a governance rule trace back to an architecture decision back to a requirement. |
| **No depth inheritance** | You choose the depth level per package instead of setting it once and letting it cascade. |
| **Quality-impact disclosure** | Whenever an expected input is missing (most visibly at AI-DWG), the package tells you what quality you're giving up and asks for approval. |
| **Recorded path** | Each package writes its input mode to its state file (`Standalone` vs `Full handoff`), so any package you add later knows exactly what it's inheriting. |

---

## Quick Decision Aid

| Your situation | Do this |
|----------------|---------|
| Already have requirements, no architecture | Enter at AI-ADLC standalone |
| Already have architecture from another source | Enter at AI-DWG standalone |
| Existing codebase, just need governance | Enter at AI-GCE standalone |
| Want only a UX design, no backlog yet | Enter at AI-UXD standalone |
| Backend/platform product, architecture should lead | Reorder to AI-POLC → AI-ADLC → AI-UXD |
| Want maximum traceability and least effort per step | Run the full chain in default order |
| Coordinating several packages out of order | Configure AI-FLO with an override flow |

**Rule of thumb:** Skip when you already hold the input a package would have produced. Reorder when your product type genuinely changes which decision should lead. Run the full default chain when traceability and inherited context matter more than speed.

---

## Related Documents

| Document | Location |
|----------|----------|
| When to Use Standalone vs Chain | `knowledge_docs/WHEN_TO_USE_STANDALONE_VS_CHAIN.md` |
| Pattern: Graceful Standalone | `knowledge_docs/PATTERN_GRACEFUL_STANDALONE.md` |
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| How the Flow Orchestrator Works | `knowledge_docs/HOW_FLOW_ORCHESTRATOR_WORKS.md` |
| Why the Lifecycle Sequence Matters | `knowledge_docs/WHY_LIFECYCLE_SEQUENCE_MATTERS.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |

*Knowledge Document | Created: 2026-06-22 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
