# How to Run a Compliance Audit

**Purpose:** Practical guide for running a periodic governance health check using AI-GCE — assessing current compliance, identifying drift, verifying rule effectiveness, and producing an audit report suitable for stakeholders and certification bodies.

---

## Who This Is For

Tech leads, engineering managers, or compliance officers who need to answer: "Are we actually following our governance rules? Where have we drifted? Are our rules still relevant? What's our compliance score trend?" — whether for internal improvement, stakeholder reporting, or certification prep.

---

## When to Run an Audit

| Trigger | Audit Type | Depth |
|---------|-----------|-------|
| Quarterly schedule | Routine health check | Standard |
| Before tier graduation | Readiness assessment | Focused on next-tier criteria |
| Before certification (SOC 2, ISO 27001) | Evidence collection | Comprehensive |
| After major architecture change | Drift detection | Focused on changed areas |
| After team change (new members, reorg) | Compliance pulse | Lightweight |
| Score dropped below threshold | Regression investigation | Diagnostic |

---

## The Audit Process

### Phase 1: Preparation (5 minutes)

1. **Identify audit scope:**
   - Full audit (all tiers, all rules)
   - Focused audit (specific category: ARCH-*, SEC-*, API-*, etc.)
   - Tier-specific audit (only Tier 2 rules, for graduation readiness)

2. **Gather context:**
   - Read `.compliance-state.json` for current score and tier
   - Note last audit date and previous findings
   - Identify any recent changes (architecture, team, steering updates)

### Phase 2: Rule Coverage Scan (10-15 minutes)

AI-GCE performs an automated scan:

**For each active rule:**
1. Is the rule still derivable from current steering? (steering drift detection)
2. Is the enforcement mechanism still active? (hook still exists and fires)
3. Has the rule been triggered in the last audit period? (dead rule detection)
4. What's the violation rate? (effectiveness measurement)

**Output: Coverage Report**
```
Rule Coverage Assessment
========================
Total active rules: 28
├── Enforceable (hook active, steering aligned): 25 (89%)
├── Orphaned (steering changed, rule stale): 2 (7%)
├── Dead (never triggered — possibly too broad): 1 (4%)
└── Disabled (manually turned off): 0 (0%)
```

### Phase 3: Compliance Scan (15-30 minutes)

AI-GCE scans the codebase against all active rules:

**For each rule category:**
- Count violations in existing code
- Compare against baseline (improving or worsening?)
- Identify patterns (are violations concentrated in specific modules/teams?)
- Flag new violations introduced since last audit

**Output: Compliance Scorecard**
```
Compliance Scorecard — Q2 2026 Audit
=====================================
Overall Score: 87% (↑ from 82% last quarter)

Category Breakdown:
├── Architecture (ARCH-*):  92% ✅ (↑5%)
├── Security (SEC-*):       95% ✅ (stable)
├── API (API-*):            84% ⚠️ (↓2%)
├── Naming (NAME-*):        91% ✅ (↑3%)
├── Testing (TEST-*):       78% ⚠️ (↑1%)
├── Governance (GOV-*):     88% ✅ (↑4%)
└── Session (SESSION-*):    85% ✅ (new this quarter)

Trend: ▲ Improving (5% overall gain)
```

### Phase 4: Drift Detection (10 minutes)

Check alignment between governance and reality:

| Check | What It Detects |
|-------|-----------------|
| Steering → Rules alignment | Rules that don't match current steering (architecture changed but rules didn't update) |
| Rules → Code alignment | Code patterns that violate rules systematically (rule may be impractical) |
| Baseline → Current gap | Baseline violations that should have been fixed by now |
| Hook coverage | Governance areas without automated enforcement (manual-only) |

**Drift signals:**
- Rule derived from `tech-stack.md` but tech stack changed 3 weeks ago → stale rule
- Rule has >50% violation rate across team → rule may be wrong for this context
- Baseline violation count INCREASED → enforcement isn't working or new code violates
- Category has rules but no hooks → enforcement is documentation-only (not automated)

### Phase 5: Findings and Recommendations (10 minutes)

Categorize findings:

| Severity | Criteria | Response |
|----------|----------|----------|
| **Critical** | Active security violations; enforcement disabled on security rules | Fix immediately, escalate |
| **High** | Compliance score below tier minimum; stale rules on active code | Fix this sprint |
| **Medium** | Score declining in a category; dead rules accumulating | Schedule for next sprint |
| **Low** | Minor drift; documentation gaps; cosmetic violations | Track, fix opportunistically |

---

## The Audit Report

Produce a structured report:

```markdown
# Compliance Audit Report — {Date}

## Executive Summary
- Overall compliance: {score}% ({trend} from last audit)
- Tier: {current tier}
- Findings: {critical} critical, {high} high, {medium} medium, {low} low

## Scope
- Audit type: {routine / focused / certification-prep}
- Rules assessed: {count}
- Code scope: {all / specific modules}

## Scorecard
{category breakdown table}

## Findings
### Critical
{list with rule ID, description, affected area, recommended action}

### High
{list}

### Medium
{list}

## Drift Analysis
{steering-to-rules alignment, dead rules, orphaned rules}

## Recommendations
1. {prioritized actions}

## Tier Readiness
{if applicable: readiness assessment for next tier}

## Evidence Artifacts
{for certification: list of logs, reports, hook configs that serve as evidence}
```

---

## Certification-Specific Audits

For formal certification prep (SOC 2, ISO 27001):

### Evidence Collection

AI-GCE compliance logging provides:

| Certification Need | AI-GCE Evidence |
|-------------------|-----------------|
| Access control verification | `GOV-01` (author ≠ approver) compliance log entries |
| Change management process | Change Register + PR governance hook logs |
| Security controls | Security rule enforcement logs, violation-free periods |
| Continuous monitoring | Hook execution logs showing ongoing enforcement |
| Corrective actions | Violation → fix → re-scan trail in compliance log |

### Audit Trail Format

`.governance/compliance-log/` contains append-only entries:

```json
{
  "timestamp": "2026-06-12T14:30:00Z",
  "rule": "SEC-01",
  "event": "violation-detected",
  "file": "src/auth/handler.ts",
  "details": "Hardcoded secret detected",
  "resolution": "fixed",
  "resolvedBy": "dev@team.com",
  "resolvedAt": "2026-06-12T14:45:00Z"
}
```

This trail provides certification auditors with continuous enforcement evidence — not just point-in-time snapshots.

---

## Audit Cadence Recommendations

| Project Stage | Audit Frequency | Focus |
|--------------|-----------------|-------|
| First month (Tier 1) | Weekly (lightweight) | Are hooks firing? Is team adapting? |
| Months 2-3 (Tier 1→2 transition) | Bi-weekly | Readiness signals for Tier 2 |
| Stable delivery (Tier 2) | Monthly | Score trends, drift detection |
| Production (Tier 3) | Monthly + quarterly deep dive | Full coverage, certification evidence |
| Pre-certification | Weekly deep dive | Evidence gaps, finding remediation |

---

## Post-Audit Actions

After every audit:

1. **Update `.compliance-state.json`** — record audit date, score, findings count
2. **Log findings in Issue Register** — tie findings to action items with owners
3. **Trigger re-derivation if needed** — stale rules require AI-GCE re-derivation
4. **Communicate results** — share scorecard with team (transparency builds buy-in)
5. **Schedule follow-up** — critical/high findings get a follow-up check within 1-2 weeks

---

## Common Pitfalls

| Pitfall | Better Approach |
|---------|-----------------|
| Auditing without acting on findings | Every finding needs an owner and a deadline |
| Only auditing before certification | Regular audits prevent surprise findings at crunch time |
| Blaming teams for low scores | Scores reflect rule-codebase fit, not team competence — tune rules if needed |
| Auditing in isolation (no context) | Always correlate with: recent architecture changes, team changes, sprint pressure |
| Keeping audit results private | Transparency drives improvement; secrecy drives resentment |

---

## Related Documents

| Document | Location |
|----------|----------|
| How GCE Derivation Pipeline Works | `knowledge_docs/HOW_GCE_DERIVATION_PIPELINE_WORKS.md` |
| How GCE Rederivation Works | `knowledge_docs/HOW_GCE_REDERIVATION_WORKS.md` |
| How to Adopt Governance on a Project | `knowledge_docs/HOW_TO_ADOPT_GOVERNANCE_ON_A_PROJECT.md` |
| How to Scale Governance as Project Matures | `knowledge_docs/HOW_TO_SCALE_GOVERNANCE_AS_PROJECT_MATURES.md` |
| Why Governance Automation Matters | `knowledge_docs/WHY_GOVERNANCE_AUTOMATION_MATTERS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
