# How to Adopt Governance on a Project

**Purpose:** Practical guide for using AI-GCE to bring automated compliance enforcement to a project — whether it's a freshly generated workspace from AI-DWG or an existing codebase that needs governance added progressively.

---

## Who This Is For

Tech leads, DevOps engineers, or engineering managers who want automated governance on their project. You're past the "we have coding standards in a wiki" stage and want machine-enforced rules that catch violations at development time — not during quarterly audits.

---

## Before You Start

**You need:**
- AI-GCE installed in your AI workspace (see `ai-gce/setup/INSTALL.md`)
- A workspace with `.kiro/steering/` files (from AI-DWG, or manually created)

**Two entry paths:**

| Path | Your Situation | What AI-GCE Does |
|------|---------------|-----------------|
| **Chain path** | AI-DWG generated your workspace | Reads all steering files, derives comprehensive governance |
| **Standalone path** | Existing codebase, no AI-DWG | You create/provide steering files, AI-GCE derives from whatever exists |

**You do NOT need:**
- All steering files perfectly written (AI-GCE works with whatever exists)
- The full chain to have run (standalone works fine)
- All governance active on day one (progressive tiers handle this)

---

## The Three-Tier Model

AI-GCE doesn't dump all rules on your team at once. It uses progressive tiers:

### Tier 1 — Foundational (Start Here)

**What's enforced:**
- Author ≠ approver (no self-merging)
- Spec before implementation (session discipline)
- Naming conventions (consistent codebase)
- Basic security (no secrets in code, input validation)
- Session governance (structured development, no vibe-coding)

**Team impact:** Minimal friction. These are the "of course we should do that" rules that no reasonable developer objects to.

**Activate when:** Immediately — these apply to any project from day one.

### Tier 2 — Standard (Graduate When Ready)

**What's enforced (adds to Tier 1):**
- Architecture boundary enforcement (module structure rules)
- API contract compliance (no endpoints without specs)
- Full PR governance (required reviewers, description templates)
- Test coverage thresholds (minimum coverage per component)
- Documentation requirements (public interfaces must be documented)

**Team impact:** Moderate structure. Requires the team to be comfortable with Tier 1 first.

**Activate when:** Team has been on Tier 1 for 2+ weeks, Tier 1 compliance is >90%, team is stable.

### Tier 3 — Advanced (Mature Projects)

**What's enforced (adds to Tier 2):**
- Performance budgets (bundle size, response time limits)
- Accessibility compliance (WCAG enforcement)
- Cross-service contract testing (consumer-driven contracts)
- Deployment governance (blue-green, canary rules)
- Observability standards (logging, metrics, tracing requirements)

**Team impact:** Full governance. Appropriate for production systems with real users.

**Activate when:** Project approaching or in production, team has maintained Tier 2 at >85% compliance.

---

## The Derivation Process

### What AI-GCE Reads

AI-GCE reads your workspace from two sources:

**Source 1: Steering Files (project-specific)**
```
.kiro/steering/
├── tech-stack.md         → Technology-specific rules
├── api-standards.md      → API contract enforcement
├── security-rules.md     → Security governance
├── module-structure.md   → Architecture boundary rules
├── naming-conventions.md → Naming enforcement
├── testing-strategy.md   → Test coverage rules
├── role-isolation.md     → Team topology rules
├── session-governance.md → Session discipline
└── ... (all available steering files)
```

**Source 2: Built-In Baseline (methodology floor)**
- 10 universal rules that apply to ANY project, regardless of steering content
- Covers: separation of duties, spec-first, session structure, review requirements
- Active even if no steering files mention these topics

### What AI-GCE Produces

```
{your-workspace}/
├── .kiro/
│   ├── hooks/                          ← Automated enforcement (14+ hooks)
│   │   ├── pre-commit-validation.json
│   │   ├── pr-governance.json
│   │   ├── session-discipline.json
│   │   ├── naming-enforcement.json
│   │   └── ...
│   └── agents/                         ← Process governance agents
│       ├── architecture-review.md
│       ├── compliance-check.md
│       └── ...
├── .governance/
│   ├── rules/                          ← Numbered rule files
│   │   ├── ARCH-01_module-boundaries.md
│   │   ├── ARCH-02_dependency-direction.md
│   │   ├── SEC-01_no-secrets-in-code.md
│   │   ├── GOV-01_author-ne-approver.md
│   │   └── ...
│   ├── compliance-log/                 ← Audit trail schema
│   │   └── .gitkeep
│   ├── COMPLIANCE_README.md            ← Guide for the team
│   ├── AGENT-GUIDE.md                  ← How governance agents work
│   └── AGENT_REGISTRY.md              ← Registry of all governance agents
└── .compliance-state.json              ← Tier tracking + readiness
```

---

## Step-by-Step Adoption

### Step 1: Run Initial Derivation

1. Point AI-GCE at your workspace
2. It scans `.kiro/steering/` and identifies all derivable rules
3. Select starting tier (Tier 1 recommended)
4. AI-GCE generates rules, hooks, and agents for that tier
5. Review everything before activation

### Step 2: Review Generated Governance

**Check each hook:**
- Does it fire on the right event? (file edit, pre-commit, PR submission)
- Is the enforcement appropriate? (blocking vs. advisory)
- Are there false-positive risks?

**Check each rule:**
- Is the rule clear and binary? (pass/fail, no ambiguity)
- Does it match your team's actual practice?
- Is the verification method realistic?

### Step 3: Activate and Observe

- Activate Tier 1 governance
- Monitor for 1–2 weeks
- Track compliance score in `.compliance-state.json`
- Collect team feedback on friction points

### Step 4: Tune and Graduate

- Adjust rules that cause false positives
- Disable rules that don't fit your context (with documented rationale)
- When Tier 1 compliance is stable at >90% → consider Tier 2 activation
- Repeat: activate → observe → tune → graduate

---

## Standalone Adoption (No AI-DWG)

If you have an existing codebase without AI-DWG-generated steering:

1. **Create minimal steering files:**
   ```
   .kiro/steering/
   ├── workspace-rules.md      ← Required (AI-GCE's marker detection)
   ├── tech-stack.md           ← Your technology choices
   └── naming-conventions.md   ← Your naming standards
   ```

2. **Run AI-GCE** — it derives from whatever steering exists + built-in baseline
3. **Add more steering files over time** — each addition triggers re-derivation with richer rules
4. **Progressive enrichment:** start thin, add depth as governance matures

The minimum viable governance is just `workspace-rules.md` + built-in baseline. You get meaningful enforcement even with one steering file.

---

## Re-Derivation (When Things Change)

AI-GCE re-derives when:
- Architecture changes (AI-DWG reconciles workspace → signals AI-GCE)
- You add/modify steering files manually
- You request tier upgrade
- A compliance audit identifies gaps

Re-derivation is **non-destructive:**
- Generated rules are overwritten (updated to match new steering)
- Custom content in `<!-- custom -->` blocks is preserved
- Team-edited files with `ownership: hybrid` keep their edits
- Compliance log is append-only (history never lost)

---

## Tips for Successful Adoption

1. **Start with Tier 1, always.** Even if you think your team is ready for Tier 3, the progressive approach builds buy-in. A team that's never had automated governance needs to experience the value before accepting the constraints.

2. **Make governance visible.** Share the `.governance/COMPLIANCE_README.md` with the team. Transparency about what's enforced and why prevents "where did this rule come from?" frustration.

3. **Tune, don't disable.** When a rule causes friction, ask "is the rule wrong, or is our practice wrong?" Often the friction reveals a real problem. Disable only when the rule genuinely doesn't apply to your context.

4. **Use compliance score as a team metric.** The score in `.compliance-state.json` tracks improvement over time. Share it in retrospectives. Celebrate improvement rather than punishing violations.

5. **Let AI-GCE re-derive after architecture changes.** If AI-ADLC adds a new container or changes an ADR, the downstream chain (DWG → GCE) should run to keep governance aligned. Stale governance is worse than no governance — it creates a false sense of compliance.

---

## What Governance Looks Like in Practice

**A developer's daily experience with Tier 2 active:**

1. Opens a new AI session → session governance hook reminds: "Reference your spec before implementing"
2. Writes code → naming hook validates conventions in real-time
3. Creates a PR → PR governance hook enforces: required reviewers, description template, linked issue
4. Modifies API → API contract hook checks: does the OpenAPI spec reflect this change?
5. Attempts to merge own PR → separation-of-duties rule blocks: different approver required

**None of this requires meetings, audits, or manual checklists.** The governance is embedded in the workflow — it happens automatically, consistently, every time.

---

## Related Documents

| Document | Location |
|----------|----------|
| How GCE Derivation Pipeline Works | `knowledge_docs/HOW_GCE_DERIVATION_PIPELINE_WORKS.md` |
| How GCE Rederivation Works | `knowledge_docs/HOW_GCE_REDERIVATION_WORKS.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |
| Why Governance Automation Matters | `knowledge_docs/WHY_GOVERNANCE_AUTOMATION_MATTERS.md` |
| How Gates and Approvals Work | `knowledge_docs/HOW_GATES_AND_APPROVALS_WORK.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
