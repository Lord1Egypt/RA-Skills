# How the AI-GCE Derivation Pipeline Works

**Purpose:** Explains how AI-GCE reads a development workspace and derives a tailored compliance enforcement layer — the two-source model, four operating modes, three-tier progressive compliance, and how steering files become automated hooks and rules.

---

## What AI-GCE Does

AI-GCE is an adaptive governance engine. It reads the development workspace produced by AI-DWG (or any workspace with `.kiro/steering/` files) and generates:
- **Rules** (`.governance/rules/`) — numbered, binary-enforceable compliance rules
- **Hooks** (`.kiro/hooks/`) — automated enforcement triggers that fire on IDE events
- **Agents** (`.kiro/agents/`) — process governance agents triggered at workflow milestones
- **Compliance logging** (`.governance/compliance-log/`) — append-only audit trail

```
DEVELOPMENT WORKSPACE (from AI-DWG)
├── .kiro/steering/ (19+ steering files)
├── DEFINITION_OF_DONE.md
├── TEAM_AGREEMENTS.md
├── CODEOWNERS
├── docker-compose.yml
└── {source structure}
        │
        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  AI-GCE DERIVATION ENGINE                                                │
│                                                                          │
│  ┌──────────────────────────┐    ┌───────────────────────────────────┐  │
│  │  SOURCE 1: Steering      │    │  SOURCE 2: Built-In Baseline      │  │
│  │  (project-specific)      │    │  (AI-DLC v1 methodology floor)       │  │
│  │                          │    │                                    │  │
│  │  Read .kiro/steering/*   │    │  10 universal rules that apply    │  │
│  │  Derive tailored rules   │    │  to ANY project regardless of     │  │
│  │  for THIS project        │    │  what steering says               │  │
│  └────────────┬─────────────┘    └──────────────┬────────────────────┘  │
│               │                                  │                       │
│               └──────────── COMBINE ─────────────┘                       │
│                              │                                           │
│                              ▼                                           │
│               Rules + Hooks + Agents + Compliance Log                    │
└─────────────────────────────────────────────────────────────────────────┘
        │
        ▼
COMPLIANCE ENFORCEMENT LAYER (installed into workspace)
├── .kiro/hooks/ (14+ automated hooks)
├── .kiro/agents/ (process governance agents)
├── .governance/rules/ (numbered rule files)
├── .governance/compliance-log/ (audit trail schema)
├── .governance/COMPLIANCE_README.md
├── .governance/AGENT-GUIDE.md
├── .governance/AGENT_REGISTRY.md
└── .compliance-state.json (tier tracking)
```

---

## The Two-Source Derivation Model

AI-GCE generates rules from TWO sources that combine:

### Source 1: Steering Files (Project-Specific)

The `.kiro/steering/` files + operational docs produced by AI-DWG. These are the primary input — rules derived from them are TAILORED to this project's architecture decisions, technology, and team agreements.

**If steering is silent on a topic:** That category gets baseline-only rules.
**If steering contradicts baseline:** Steering WINS (the project has authority).

### Source 2: Built-In Governance Baseline (Universal)

Ten methodology constants that apply to ANY AI-DLC v1 project regardless of steering content:

| Baseline Rule | Category | Always Enforced |
|--------------|----------|:---------------:|
| Spec/design must exist before implementation code | GOV-SESSION | ✅ |
| Never "vibe code" — all code follows steering | GOV-SESSION | ✅ |
| Author ≠ Approver for code review | GOV-ROLE | ✅ |
| No direct push to main/protected branches | GOV-DEVOPS | ✅ |
| Tests must pass before merge | GOV-CICD | ✅ |
| No hardcoded secrets in source | SEC | ✅ |
| Database migration must have rollback method | GOV-DEVOPS | ✅ |
| One task at a time in AI sessions | GOV-SESSION | ✅ |
| Compliance log is append-only | GOV-LOG | ✅ |
| Critical exception bypass requires different person | GOV-LOG | ✅ |

**Why two sources:** Architecture rules are 100% steering-derived (no steering = no rule). But governance rules have universal minimums — "never push to main" is true for ANY project. A team that didn't run the full chain still gets governance value from the baseline floor.

### Resolution Rule

```
IF steering provides SPECIFIC rules → Derive from steering (overrides baseline)
IF steering is SILENT                → Apply baseline only
IF steering CONTRADICTS baseline     → Steering WINS
IF steering is ABSENT entirely       → Baseline only (universal governance floor)
```

---

## Four Operating Modes

| Mode | Trigger | What Happens |
|------|---------|-------------|
| **1. Full Generation** | No `.kiro/hooks/` exists; user requests compliance | Read workspace → derive all rules + hooks + agents |
| **2. Re-Derivation** | Hooks exist; steering updated | Diff → selectively regenerate affected rules/hooks |
| **3. Brownfield Adoption** | `brownfield-patterns.md` exists; no baseline yet | Scan existing code → baseline violations → enforce on new code only |
| **4. Tier Activation** | `.compliance-state.json` exists; readiness criteria met | Activate next compliance tier → expand enforcement scope |

Mode is detected automatically from workspace state and user intent.

---

## The Three-Tier Progressive Compliance Model

Enforcement is never big-bang. Every deployment follows progressive activation:

```
TIER 1 (Day 0)               TIER 2 (Sprint 2+)          TIER 3 (Pre-Release)
──────────────                ──────────────────           ────────────────────
Structure & naming            Governance & roles           Full audit & security
Basic phase gates             Steering quality             Change management
Project-init agent            DevOps rules                 All phase gates
Starter hooks (4-6)           Full hook set (10+)          Compliance reporting

Score target: 60-70%          Score target: 80-90%         Score target: 92%+
Effort: 30 min                Effort: 1 hour              Effort: 2 hours
```

### Tier Readiness Criteria

**Tier 2 requires:** Tier 1 active, ≥1 sprint completed, CI pipeline exists, ≥2 contributors, ≥4 steering files, Tier 1 audit score ≥ 70%

**Tier 3 requires:** Tier 2 active, release candidate exists, deployment target defined, external stakeholders identified, Tier 2 audit score ≥ 85%, no open 🔴 Critical remediations

---

## Full Generation Flow (Mode 1)

### Step 1: Read Workspace

Load ALL steering files + supporting artifacts. Catalog:
- Technology stack (from `tech-stack.md`)
- Module paths (from `module-structure.md` + folder scan)
- API style (from `api-standards.md`)
- Security model (from `security-rules.md`)
- Test expectations (from `testing-strategy.md`)
- Multi-tenant status (presence/absence of `multi-tenancy.md`)
- Extensions active (presence of `event-sourcing.md`, `feature-flags.md`, etc.)

### Step 2: Determine Applicable Rules

Map each steering file to its rule category. The engine generates rules in two groups:

**Always-generated (architectural):** Architecture compliance, API-first, Security, Data governance, Module boundaries, Naming, Error handling, Logging, Sensitive data, Domain context

**Always-generated (non-architectural):** Phase gates, Sprint governance, Session methodology, PR governance, CI/CD gates, Role isolation, Team topology, DevOps, Steering governance, Compliance log

**Conditionally-generated:** Tenant isolation, API versioning, Resilience, Tracing, Performance, Workflow, Frontend, Event sourcing, Feature flags, MCP governance

### Step 3: Generate Rules (Two-Source Combined)

For each rule category:
1. Apply baseline rules (universal floor)
2. Read relevant steering file(s)
3. Extract decisions, constraints, patterns, paths, agreements
4. Translate into numbered rules with severity, verification steps, file patterns
5. Tag each rule with its compliance tier (1, 2, or 3)

### Step 4: Generate Hooks

For each hook, populate templates with:
- File patterns derived from `tech-stack.md` (technology-specific globs)
- Folder paths from `module-structure.md` (actual project paths)
- Rule IDs from Step 3
- DoD criteria from `DEFINITION_OF_DONE.md`
- Module ownership from `CODEOWNERS`

**Hook debounce strategy:**
- **Tier A (fileEdited):** Security-critical — fire immediately on every save (secrets, tenant isolation, migrations)
- **Tier B (agentStop):** Advisory — fire only on final state (naming, coverage, documentation)

### Step 5: Install Output

All output installed into the workspace:
- `.kiro/hooks/` — automated enforcement hooks
- `.kiro/agents/` — process governance agents
- `.governance/rules/` — full rule set
- `.governance/compliance-log/` — logging infrastructure
- `.compliance-state.json` — tier tracking

---

## Key Design Principles

| Principle | Implementation |
|-----------|---------------|
| Silent when compliant | Zero output on success — noise kills adoption |
| Every action logged | JSONL compliance events with timestamp, rule, result, evidence |
| Technology-specific hooks | File globs derived from actual tech stack, not generic `*.*` |
| Phase-aware enforcement | Rules only fire when applicable to current project phase |
| Customizations survive | `<!-- custom -->` markers preserved during re-derivation |
| Brownfield first-class | Baseline existing violations as tech debt; enforce on new code only |
| Enforceable or not a rule | MUST/NEVER with binary pass/fail — no "consider" or "should" |

---

## Re-Derivation (Mode 2)

When steering files are updated (e.g., after AI-DWG reconciliation):

1. Detect which steering files changed
2. Map changes to affected rule categories
3. Regenerate ONLY affected rules and hooks
4. Preserve team customizations (`<!-- custom -->`)
5. Signal completion (no further downstream — AI-GCE is the terminal node)

---

## Related Documents

| Document | Location |
|----------|----------|
| Core generator | `ai-gce/ai-gce-rules/core-generator.md` |
| Workspace reading guide | `ai-gce/ai-gce-rule-details/common/workspace-reading-guide.md` |
| Generator files (23) | `ai-gce/ai-gce-rule-details/generators/` |
| Re-derivation logic | `ai-gce/ai-gce-rule-details/re-derivation/` |
| Hook templates | `ai-gce/ai-gce-rule-details/templates/hooks/` |
| Agent templates | `ai-gce/ai-gce-rule-details/templates/agents/` |
| Agent Governance Contract | `contracts/AGENT_GOVERNANCE_CONTRACT.md` |
| Family Structure | `FAMILY_STRUCTURE.md` |

*Knowledge Document | Created: 2026-06-11 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
