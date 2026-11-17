# When to Use Standalone vs. Chain Mode

**Decision:** Should I run the full AI-* Family chain, or just use the one package I need?

**Derived from:** Pattern: Graceful Standalone + Pattern: Marker File Detection

---

## The Decision at a Glance

| Your Situation | Recommendation |
|---------------|----------------|
| Starting from scratch, no existing artifacts | Run the chain (PILC → POLC → UXD → ADLC → DWG → GCE) |
| Have requirements but no architecture | Enter at AI-ADLC standalone |
| Have architecture docs from another source | Enter at AI-DWG standalone |
| Have existing codebase, need governance only | Enter at AI-GCE standalone |
| Need to evaluate an idea before committing | Start at AI-ILC standalone |
| Want maximum quality and traceability | Full chain |
| Want speed over completeness | Standalone at the package you need |

---

## Full Chain: When and Why

**Use the full chain when:**
- The project is new (no existing artifacts from any source)
- Multiple teams will use the output (consistency matters)
- Audit trail / traceability is required (certification, compliance)
- You want depth inheritance (one depth choice flows through all packages)
- The project is complex enough to justify structured initiation

**What you gain:**
- Each package reads rich context from its predecessor (fewer questions, better output)
- Depth cascades automatically (Standard everywhere, no per-package decision)
- Traceability: every governance rule traces back to an architecture decision, which traces back to a requirement
- Project ID correlation across all artifacts

**What it costs:**
- More time upfront (15-25 hours across 1-2 weeks for Standard depth)
- Requires running packages in sequence (some parallelism possible)
- Overkill for small/simple projects

---

## Standalone: When and Why

**Use standalone when:**
- You have existing artifacts from another source (consultant architecture, PRD from product team, etc.)
- You only need ONE capability (just governance, just architecture, just initiation)
- The project is simple and full chain is disproportionate
- You're retrofitting governance onto an existing project
- Speed matters more than traceability

**What you gain:**
- Start immediately with whatever input you have
- No dependency on running prior packages
- Faster time-to-value (one package, one session)

**What it costs:**
- More questions during intake (package must extract context that predecessor would have provided)
- No automatic depth inheritance (you choose per-package)
- Limited traceability (can't trace governance rules back to requirements if PILC never ran)
- Successor packages get less context (if you later add them)

---

## The Hybrid Approach

You don't have to choose one or the other for all packages:

| Approach | Example |
|----------|---------|
| Chain for initiation + design, standalone for governance | Run PILC → POLC → UXD → ADLC → DWG (chain), then install AI-GCE standalone on any workspace |
| Standalone design, chain for everything else | Have architecture from another source → enter at AI-DWG, let DWG → GCE chain from there |
| Partial chain entry | Already have a PIP → enter at AI-POLC, let the sequence flow POLC → UXD → ADLC → DWG |

---

## Decision Matrix

| Factor | Favors Chain | Favors Standalone |
|--------|:---:|:---:|
| No existing artifacts | ✅ | |
| Existing requirements doc | | ✅ |
| Existing architecture | | ✅ |
| Existing codebase | | ✅ |
| Need audit trail | ✅ | |
| Solo developer | | ✅ |
| Enterprise / multi-team | ✅ | |
| Regulated industry | ✅ | |
| Proof of concept | | ✅ |
| Production system | ✅ | |
| Time pressure | | ✅ |

**Rule of thumb:** If ≥3 factors favor chain → use chain. If ≥3 favor standalone → use standalone. Mixed → hybrid approach.

---

## Related Documents

| Document | Location |
|----------|----------|
| Pattern: Graceful Standalone | `knowledge_docs/PATTERN_GRACEFUL_STANDALONE.md` |
| Pattern: Marker File Detection | `knowledge_docs/PATTERN_MARKER_FILE_DETECTION.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
