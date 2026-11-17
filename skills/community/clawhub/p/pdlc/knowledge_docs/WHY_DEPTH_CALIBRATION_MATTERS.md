# Why Depth Calibration Matters

**Purpose:** Explains why adapting process depth to project complexity (rather than one-size-fits-all) prevents both over-engineering simple projects and under-specifying complex ones.

---

## The Practice

Depth calibration means choosing how much process rigor to apply based on project complexity, risk, and team size — ranging from minimal (proof-of-concept: fast, light, essentials only) to comprehensive (enterprise system: thorough, detailed, all stages active). The same workflow serves both by adapting its depth, not by being different workflows.

---

## What Happens When You Skip It

1. **The over-engineered prototype.** A 2-week proof-of-concept goes through 13 stages of architecture design, produces 25 deliverables, and generates full governance. The overhead exceeds the implementation time. The team abandons the process and vibe-codes the prototype — learning nothing from the tool.

2. **The under-specified enterprise system.** A mission-critical system with 8 integrations and 5 teams gets the same lightweight treatment as a single-developer tool. Feasibility isn't assessed. Risks aren't identified. Architecture is "figure it out as we go." The discovery of unbounded complexity happens mid-delivery at maximum cost.

3. **The process-fits-nobody middle ground.** A single depth level that's "medium" — too heavy for small projects (developers resent the ceremony), too light for complex ones (stakeholders get insufficient analysis). No one is served well.

4. **The false equivalence.** A team treats every initiative as equal: same number of stages, same deliverable depth, same governance level. A 1-person internal tool gets a full stakeholder register. An 8-team platform gets the same stakeholder register format as the 1-person project. Neither is appropriate.

5. **The depth misalignment cascade.** Project starts at "minimal" depth because it seems simple. Mid-way, complexity is discovered (integrations, regulatory requirements, multi-team coordination). But the light-touch initiation didn't capture constraints, risks, or stakeholder landscape. Catching up mid-project is 5x more expensive than starting at the right depth.

---

## Real-World Impact

| Dimension | Impact |
|-----------|--------|
| Cost | Over-engineering simple projects wastes 40-60% of process investment on deliverables no one reads. Under-specifying complex ones creates 2-5x rework. Right-sizing eliminates both failure modes. |
| Timeline | Minimal depth on a simple project saves days of ceremony. Comprehensive depth on a complex project saves weeks of mid-project discovery. Calibration optimizes both directions. |
| Quality | Complex projects at insufficient depth produce architectures with gaps. Simple projects at excessive depth produce governance without substance. Calibration ensures depth matches need. |
| Team | Developers respect process that's proportional to complexity. They reject process that feels like bureaucracy for its own sake (over-engineering) or dangerous shortcuts (under-specifying). |
| Risk | The risk profile should determine the depth. High-risk = more analysis, more gates, more governance. Low-risk = fast path with essentials. Uniform depth ignores risk signals. |

---

## How the AI-* Family Prevents This

| Package | Feature | Prevention Mechanism |
|---------|---------|---------------------|
| **All packages** | Three depth levels | Minimal / Standard / Comprehensive — every stage adapts behavior, deliverable detail, and gate rigor to the chosen depth. |
| **AI-PILC** | Depth selection at Stage 2 | After reading the input, AI-PILC recommends a depth level based on complexity signals (team size, integrations, risk indicators, regulatory mentions). User confirms or overrides. |
| **All packages** | Depth cascading | Depth chosen at entry point cascades through the entire chain. A Minimal project stays minimal across PILC → POLC → UXD → ADLC → DWG → GCE. No manual re-selection per package. |
| **AI-ADLC** | Stage skipping at Minimal | Minimal depth skips detailed design stages (9-12) and produces L1-L2 architecture only. Appropriate for simple systems. |
| **AI-GCE** | Tier alignment with depth | Minimal projects start (and may stay) at Tier 1 governance. Comprehensive projects can immediately adopt Tier 2-3. Governance weight matches project weight. |
| **All packages** | Depth override | Any package can override inherited depth upward (a Minimal project discovers complexity) or downward (a phase is simpler than expected). Recalibration is always available. |

---

## Severity: Medium

Depth miscalibration doesn't cause catastrophic failure — it causes chronic waste (too heavy) or chronic gaps (too light). The cumulative effect over a project lifecycle is significant: 20-40% of effort either wasted on unnecessary ceremony or spent on rework that proper depth would have prevented.

---

## Related Documents

| Document | Location |
|----------|----------|
| How Depth Levels Work | `knowledge_docs/HOW_DEPTH_LEVELS_WORK.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |
| How to Initiate a Project | `knowledge_docs/HOW_TO_INITIATE_A_PROJECT.md` |
| How Gates and Approvals Work | `knowledge_docs/HOW_GATES_AND_APPROVALS_WORK.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
