# Why Separation of Duties Matters

**Purpose:** Explains why requiring different people for creation, review, and approval prevents the most dangerous software failures — unchecked changes that bypass quality gates.

---

## The Practice

Separation of duties means that the person who writes code cannot be the same person who approves it for merge. The person who designs a change cannot be the sole person who validates it. Every consequential action has at least two sets of eyes — one to do, one to verify.

---

## What Happens When You Skip It

1. **The unchecked commit.** A senior developer merges their own PR on a Friday afternoon. No review. A subtle auth bypass ships to production. Discovered 3 weeks later by a security researcher — data exposed for 21 days.

2. **The rubber-stamp culture.** One person writes code, reviews it themselves (or gets a teammate who always approves without reading), and merges. Over months, the codebase accumulates shortcuts, tech debt, and security holes that no second perspective ever caught.

3. **The single-point-of-knowledge failure.** One developer owns a module completely — writes, reviews, deploys. They leave the company. No one else has ever read that code critically. The module becomes untouchable because no one understands it well enough to change it safely.

4. **The accidental privilege escalation.** A developer adds themselves to CODEOWNERS for a security-sensitive module, then approves their own changes to that module. Without segregation, there's no circuit breaker between intent and execution.

5. **The audit gap.** Compliance auditor asks: "Who verified this production change?" Answer: the same person who made it. Audit finding. Certification at risk. Remediation costs more than the review would have.

---

## Real-World Impact

| Dimension | Impact |
|-----------|--------|
| Cost | Security breaches from unchecked code average $4.5M per incident (IBM Cost of a Data Breach). A 15-minute code review costs $50 in developer time. |
| Timeline | Incidents from unchecked changes take 2-4x longer to detect and resolve because there's no reviewer who remembers what the change was supposed to do. |
| Quality | Codebases without review accumulate 3-5x more defects per KLOC. Every unchecked merge is a roll of the dice. |
| Team | When one person can do everything alone, knowledge silos form. When departure happens, the team loses capability proportional to that person's unchecked scope. |
| Risk | Regulatory frameworks (SOC 2, ISO 27001, PCI-DSS, HIPAA) REQUIRE separation of duties. Non-compliance = certification failure = business impact. |

---

## How the AI-* Family Prevents This

| Package | Feature | Prevention Mechanism |
|---------|---------|---------------------|
| **AI-GCE** | GOV-01: Author ≠ Approver | Tier 1 (foundational) rule — active from day one. Hook blocks self-merge on any PR. |
| **AI-GCE** | Role isolation rules | Derives role-based access rules from `role-isolation.md` steering file. Enforces who can approve what. |
| **AI-DWG** | CODEOWNERS generation | Generates code ownership mapping from architecture — ensures appropriate reviewers are assigned per module. |
| **AI-DWG** | `role-isolation.md` steering | Creates steering file defining team topology, ownership boundaries, and review requirements per component. |
| **AI-GCE** | PR governance hooks | Enforces: minimum reviewer count, required reviewers for security-sensitive paths, description requirements. |
| **AI-GCE** | Session governance | Prevents "vibe-coding" sessions where a developer implements without spec or review checkpoint. |

---

## Severity: Critical

Separation of duties is not bureaucracy — it's the single cheapest control that prevents the most expensive failures. A 15-minute review catches what a 3-week incident investigation discovers too late. Every major software security breach post-mortem includes "change was not reviewed" as a contributing factor.

---

## Related Documents

| Document | Location |
|----------|----------|
| How GCE Derivation Pipeline Works | `knowledge_docs/HOW_GCE_DERIVATION_PIPELINE_WORKS.md` |
| How to Adopt Governance on a Project | `knowledge_docs/HOW_TO_ADOPT_GOVERNANCE_ON_A_PROJECT.md` |
| Why Governance Automation Matters | `knowledge_docs/WHY_GOVERNANCE_AUTOMATION_MATTERS.md` |
| Why Security Gates Matter | `knowledge_docs/WHY_SECURITY_GATES_MATTER.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
