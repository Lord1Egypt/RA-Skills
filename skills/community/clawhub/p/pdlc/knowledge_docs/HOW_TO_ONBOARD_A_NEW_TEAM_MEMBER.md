# How to Onboard a New Team Member

**Purpose:** Practical guide for onboarding a new developer into a project that uses the AI-* Family — what they need to know, what the workspace gives them automatically, and how governance helps rather than hinders their ramp-up.

---

## Who This Is For

Tech leads or team members welcoming a new developer to a project that already has AI-DWG workspace generation and AI-GCE governance active. You want the new person productive fast — with guardrails that teach rather than punish.

---

## What the New Member Gets (Automatically)

A project built with the AI-* Family already provides most onboarding infrastructure:

| Artifact | What It Does for Onboarding |
|----------|----------------------------|
| `PROJECT_INSTRUCTIONS.md` | Full project context — every AI session starts with this, so the new dev gets instant context |
| `.kiro/steering/workspace-rules.md` | Project conventions, architecture overview, team norms — readable in 5 minutes |
| `.kiro/steering/tech-stack.md` | Technology choices with rationale — no guessing "why did we pick X?" |
| `.kiro/steering/naming-conventions.md` | How to name things — no learning by osmosis |
| `.kiro/steering/module-structure.md` | Where code goes — prevents "I put it in the wrong folder" |
| `DEFINITION_OF_DONE.md` | What "done" means — clear expectations from day one |
| `TEAM_AGREEMENTS.md` | How the team works — review process, communication norms |
| `CODEOWNERS` | Who owns what — know who to ask |
| `.governance/COMPLIANCE_README.md` | What governance exists, why, and how it works |
| Governance hooks | Catch mistakes in real-time with explanations (teaching, not blocking) |

**Key insight:** In a governed workspace, the new member doesn't need to memorize standards — the hooks catch violations and explain the rule. They learn conventions by building, not by reading a wiki first.

---

## The Onboarding Path (Day by Day)

### Day 1: Orientation (2 hours)

**New member reads:**
1. `PROJECT_INSTRUCTIONS.md` — 10 min (project context, architecture summary)
2. `.kiro/steering/workspace-rules.md` — 5 min (high-level conventions)
3. `TEAM_AGREEMENTS.md` — 5 min (how the team collaborates)
4. `DEFINITION_OF_DONE.md` — 3 min (quality expectations)
5. `.governance/COMPLIANCE_README.md` — 5 min (what governance does, tier level, what to expect)

**Team lead walks through:**
- Folder structure (matches architecture — explain why things are where they are)
- Active governance tier and what it means day-to-day
- How to read hook feedback (it's guidance, not punishment)

**Total reading time:** ~30 minutes. The rest of Day 1 is environment setup and first small task.

### Day 2-5: First Tasks with Guardrails

**What happens:**
- New member picks up a small, well-scoped task
- Governance hooks fire when conventions are missed
- Hook feedback includes the rule and WHY it exists
- New member learns conventions by doing — not by memorizing upfront

**Example flow:**
```
Developer creates: src/services/UserService.ts
Hook fires: "Naming convention: service files use kebab-case (user-service.ts)"
Developer learns: naming convention — in context, immediately applicable
```

**Team lead role:** Available to answer "why" questions. The hooks catch WHAT to do; the team lead explains WHY when asked.

### Week 2: Increasing Autonomy

- New member's PRs pass governance checks more often
- Fewer hook corrections per day (learning curve visible)
- Start assigning tasks in modules the new member hasn't touched
- Module structure steering guides them to the right location

### Month 1: Full Contributor

- Governance hooks rarely fire (conventions internalized)
- New member can review others' PRs (governance gives objective criteria)
- Familiar with architecture boundaries and why they exist
- Can explain the governance model to the NEXT new member

---

## How Governance Helps Onboarding

| Traditional Onboarding | Governed Onboarding |
|----------------------|---------------------|
| "Read the wiki" (50 pages, outdated) | Steering files are the living standard (always current) |
| "Ask someone how we do things" | Hooks tell you immediately when you deviate |
| Learn by making mistakes in PR review | Learn by making mistakes at development time (faster feedback) |
| Inconsistent feedback from different reviewers | Consistent feedback from automated rules |
| Imposter syndrome: "everyone knows this but me" | Rules are explicit: no hidden knowledge |
| Weeks to understand conventions | Days — governance teaches through enforcement |

---

## Governance Sensitivity for New Members

### First Week: Advisory Mode

Consider temporarily setting new-member-facing hooks to advisory (warning, not blocking) for the first week:
- Violations still flagged (learning happens)
- Commits not blocked (frustration prevented)
- After 1 week: full enforcement (member has seen the patterns)

### Common New-Member Triggers

| Hook That Fires | What It Teaches | First-Time Guidance |
|----------------|-----------------|---------------------|
| Naming convention | How to name files/variables in this project | "We use {pattern} — here's why: consistency across 5 devs" |
| Module boundary | Where code belongs architecturally | "This service talks to {X} — put integration code in {folder}" |
| Test requirement | That tests are expected alongside code | "We require tests for new code — minimum coverage is {N}%" |
| API contract | That endpoints need specs | "Add to the OpenAPI spec before implementing" |
| Session discipline | That specs come before implementation | "Write a brief spec comment before coding the feature" |

---

## Onboarding Checklist (for the Team Lead)

```markdown
## New Member Onboarding — {Name} — {Date}

### Pre-Arrival
- [ ] Add to CODEOWNERS for their initial module
- [ ] Prepare first task (small, well-scoped, in a familiar module)
- [ ] Review current governance tier — any adjustments needed?

### Day 1
- [ ] Share reading list: PROJECT_INSTRUCTIONS, workspace-rules, TEAM_AGREEMENTS, DoD
- [ ] Walk through folder structure and architecture boundaries
- [ ] Explain governance: "Hooks will guide you — they're teachers, not police"
- [ ] Environment setup complete (all tools, access, repo clone)

### Week 1
- [ ] First PR submitted and merged
- [ ] New member encountered ≥1 governance hook (learned a convention in context)
- [ ] Answered any "why do we..." questions from hook feedback
- [ ] Check: new member knows where to find steering files

### Week 2
- [ ] Working independently on standard tasks
- [ ] Fewer hook corrections per day vs. Week 1
- [ ] Assigned work in a second module (tests navigation skills)

### Month 1
- [ ] Full contributor status
- [ ] Can review others' PRs using governance criteria
- [ ] Understands architecture boundaries (module-structure.md)
- [ ] Contributed to TEAM_AGREEMENTS or DoD update (ownership signal)
```

---

## What If There's No Governance Yet?

If the project doesn't have AI-GCE active, onboarding is harder but not impossible:

1. **Use steering files as documentation** — even without enforcement, `.kiro/steering/` files describe conventions
2. **Consider activating Tier 1** — basic governance helps new members MORE than experienced ones (they need the most guidance)
3. **At minimum, ensure `PROJECT_INSTRUCTIONS.md` exists** — this single file provides AI session context that accelerates every interaction

---

## Related Documents

| Document | Location |
|----------|----------|
| How DWG Generation Engine Works | `knowledge_docs/HOW_DWG_GENERATION_ENGINE_WORKS.md` |
| How to Adopt Governance on a Project | `knowledge_docs/HOW_TO_ADOPT_GOVERNANCE_ON_A_PROJECT.md` |
| How to Scale Governance as Project Matures | `knowledge_docs/HOW_TO_SCALE_GOVERNANCE_AS_PROJECT_MATURES.md` |
| How Depth Levels Work | `knowledge_docs/HOW_DEPTH_LEVELS_WORK.md` |
| Why Governance Automation Matters | `knowledge_docs/WHY_GOVERNANCE_AUTOMATION_MATTERS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
