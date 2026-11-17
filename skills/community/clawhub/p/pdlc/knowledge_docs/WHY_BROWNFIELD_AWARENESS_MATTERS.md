# Why Brownfield Awareness Matters

**Purpose:** Explains why tools and processes must explicitly handle existing systems — because most real projects extend something that already exists, and treating brownfield as "greenfield minus some stages" fails catastrophically.

---

## The Practice

Brownfield awareness means every tool, workflow, and governance package explicitly asks: "Is there something here already?" — and fundamentally changes its behavior based on the answer. It's not a flag; it's a different operating mode with different questions, different outputs, and different constraints.

---

## What Happens When You Skip It

1. **The "start from scratch" assumption.** The tool generates a full architecture, full workspace, full governance — ignoring the 200,000 lines of existing code. The generated artifacts conflict with existing conventions. The team ignores the tool output because it doesn't reflect their reality.

2. **The destructive overlay.** A workspace generator creates folder structures that conflict with existing ones. Files get overwritten. Configurations are replaced. A week of the team's customizations vanish because the tool assumed emptiness.

3. **The impossible governance gap.** Governance activates and immediately flags 500 violations in existing code. The team can't merge anything. The legitimate path — "enforce going forward, baseline existing" — wasn't designed into the system. Binary pass/fail on an existing codebase always fails.

4. **The wrong questions at intake.** "What should we build?" asks a greenfield process. The brownfield question is different: "What exists? What are we changing? What's the extend-vs-replace decision?" Asking greenfield questions of a brownfield project wastes time and produces irrelevant analysis.

5. **The hidden dependency chain.** The new feature is designed in isolation. During implementation, it discovers hard dependencies on existing subsystems — auth flows that can't change, data formats locked by external consumers, infrastructure constraints baked into the current architecture. None of this was captured because the tool didn't ask about existing context.

---

## Real-World Impact

| Dimension | Impact |
|-----------|--------|
| Cost | 80% of professional software projects are brownfield (extensions, migrations, additions). Tools that only handle greenfield serve 20% of the market effectively. |
| Timeline | Brownfield projects that use greenfield processes average 40% longer than planned because integration with existing systems wasn't scoped upfront. |
| Quality | Generated artifacts that ignore existing code create two competing sources of truth. Teams follow the existing patterns (because they work) and ignore the generated ones (because they conflict). |
| Team | Developers working on brownfield projects feel ignored by tools that only ask "what do you want to build?" without acknowledging what's already built. Trust in the tooling erodes. |
| Risk | The biggest brownfield risk is breaking existing functionality while adding new capability. Without awareness of what exists, there's no way to protect it. |

---

## How the AI-* Family Prevents This

| Package | Feature | Prevention Mechanism |
|---------|---------|---------------------|
| **AI-PILC** | Brownfield input mode | Detects "extending existing system" at Stage 2. Changes questions to: "What exists? What's changing? Extend vs. replace?" — fundamentally different intake. |
| **AI-ADLC** | Brownfield architecture mode | Loads existing architecture, identifies ONLY the delta (new components, changed integrations). Doesn't redesign what already works. |
| **AI-DWG** | Mode 3: Brownfield Overlay | Adds governance/steering to existing codebase WITHOUT touching existing code. Non-destructive. Adapts steering to actual folder structure. |
| **AI-GCE** | Baseline + enforce-forward pattern | Records existing violations as baseline. Enforces only on new code. Prevents "everything broke on day one" while still improving over time. |
| **AI-GCE** | Incremental adoption tiers | Starts with Tier 1 (minimal rules) so governance doesn't overwhelm an existing team's workflow. |
| **All packages** | State file brownfield signal | `pilc-state.md` carries `Project Type: Brownfield Extension` forward through the chain. Every downstream package adapts its behavior. |

---

## Severity: High

Brownfield is the default, not the exception. Any tool or process that assumes greenfield serves a minority of real projects. The difference between a tool that handles brownfield and one that doesn't is the difference between adoption and rejection in 80% of professional contexts.

---

## Related Documents

| Document | Location |
|----------|----------|
| How to Retrofit Governance on Existing Code | `knowledge_docs/HOW_TO_RETROFIT_GOVERNANCE_ON_EXISTING_CODE.md` |
| How DWG Generation Engine Works | `knowledge_docs/HOW_DWG_GENERATION_ENGINE_WORKS.md` |
| How to Adopt Governance on a Project | `knowledge_docs/HOW_TO_ADOPT_GOVERNANCE_ON_A_PROJECT.md` |
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
