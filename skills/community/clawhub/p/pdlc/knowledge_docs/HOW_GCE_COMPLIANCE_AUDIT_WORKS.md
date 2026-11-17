# How AI-GCE Compliance Audit Works

**Purpose:** Explains the internal mechanics of AI-GCE's compliance audit process — how it scans a workspace against active rules, calculates compliance scores, detects drift, produces audit reports, and maintains the audit trail for certification evidence.

---

## What a Compliance Audit Is

A compliance audit is a structured scan of the workspace against all active governance rules at the current tier. It produces: a compliance score, a findings list (violations categorized by severity), drift detection (rules that no longer match steering), and an audit report suitable for stakeholders or certification bodies.

```
WORKSPACE STATE (code + steering + hooks)
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  AI-GCE COMPLIANCE AUDIT                                             │
│                                                                      │
│  RULE SCAN     →    SCORE      →    DRIFT CHECK   →    REPORT        │
│  (apply each     (calculate      (rules vs.        (findings +       │
│   rule to code)   compliance %)   current steering)  evidence)        │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼
AUDIT REPORT + UPDATED .compliance-state.json + COMPLIANCE LOG ENTRIES
```

---

## The Audit Engine (3 Layers)

### Layer 1: Rule Coverage Scan

For each active rule in `.governance/rules/`:

| Check | Question Answered |
|-------|-------------------|
| Derivability | Is this rule still derivable from current steering? (stale rule detection) |
| Enforcement | Is the corresponding hook active and firing? (enforcement gap detection) |
| Activity | Has this rule been triggered in the audit period? (dead rule detection) |
| Status | Is the rule enabled, disabled, or overridden? |

**Output:** Rule coverage percentage — how many rules are properly active and enforceable.

### Layer 2: Compliance Scan

For each enforceable rule, scan the codebase:

```
For rule ARCH-01 (module boundaries):
  1. Parse module-structure.md for defined boundaries
  2. Scan all import statements in source files
  3. Compare imports against boundary rules
  4. Flag violations (file, line, import that crosses boundary)
  5. Compare against baseline (existing vs. new violations)
  
Result: {total_checked: 847, violations: 12, new_since_baseline: 2}
```

**Scoring formula:**
```
Category Score = (checked - violations) / checked × 100
Overall Score = weighted average of all category scores
Weight = rule severity (Critical: 3x, High: 2x, Medium: 1x)
```

### Layer 3: Drift Detection

Drift occurs when the governance layer no longer matches the current workspace:

| Drift Type | Detection Method | Implication |
|-----------|-----------------|-------------|
| **Steering-rule drift** | Rule references steering file that's been modified | Rule may enforce outdated patterns |
| **Architecture-steering drift** | AP changed but steering wasn't reconciled | Steering describes old architecture |
| **Hook-rule mismatch** | Rule exists but no hook enforces it | Rule is documentation-only, not automated |
| **Dead rules** | Rule never triggers (zero events in audit window) | Rule may be too broad or irrelevant |
| **Orphaned hooks** | Hook exists but no corresponding rule | Enforcement without documented justification |

---

## Audit Types

| Type | Scope | When | Duration |
|------|-------|------|----------|
| **Quick pulse** | Score + top violations only | Weekly / on-demand | 2-5 minutes |
| **Standard audit** | Full scan + drift + findings | Monthly | 15-30 minutes |
| **Deep audit** | Full scan + evidence collection + tier readiness | Quarterly / pre-certification | 30-60 minutes |
| **Focused audit** | Single category (e.g., SEC-* only) | After security change / incident | 5-15 minutes |
| **Regression audit** | Compare current vs. previous audit | After score drops | 10-20 minutes |

---

## The Compliance Score

```
.compliance-state.json (updated after each audit):
{
  "complianceTier": 2,
  "score": 87,
  "scoreHistory": [82, 83, 85, 86, 87],
  "lastAudit": "2026-06-12T14:30:00Z",
  "categoryScores": {
    "ARCH": 92,
    "SEC": 95,
    "API": 84,
    "NAME": 91,
    "TEST": 78,
    "GOV": 88,
    "SESSION": 85
  },
  "findings": {
    "critical": 0,
    "high": 2,
    "medium": 5,
    "low": 8
  },
  "drift": {
    "staleRules": 1,
    "orphanedHooks": 0,
    "deadRules": 2
  },
  "baselineViolations": 47,
  "currentViolations": 15,
  "newViolations": 2,
  "nextTierReadiness": {
    "tier3": {
      "complianceThreshold": true,
      "teamStability": true,
      "overallReady": false
    }
  }
}
```

---

## Baseline vs. New Violations

The audit distinguishes between pre-existing and new violations:

| Category | Definition | Treatment |
|----------|-----------|-----------|
| **Baseline violations** | Present when governance was first adopted (`enforceFrom` date) | Tracked but not counted against score |
| **New violations** | Introduced AFTER governance adoption | Full severity, counted against score |
| **Resolved baseline** | Baseline violation that was fixed | Positive signal, reduces baseline count |
| **Regression** | Previously-fixed violation reintroduced | Flagged as high priority (something broke) |

**Score calculation uses new violations only** — ensuring the team isn't penalized for historical debt while maintaining accountability for forward progress.

---

## Audit Evidence (Certification Support)

For SOC 2, ISO 27001, and similar certifications, the audit produces:

| Evidence Type | Source | Proves |
|--------------|--------|--------|
| Continuous enforcement log | `.governance/compliance-log/` | Controls are active, not periodic |
| Audit history | `.compliance-state.json` scoreHistory | Sustained compliance over time |
| Violation-resolution trail | Log entries with `resolution` + `resolvedAt` | Corrective action is timely |
| Rule coverage report | Layer 1 output | All required controls are implemented |
| Hook execution count | Hook event logs | Automation is running, not just configured |
| Tier progression record | State file tier changes | Governance matures with the project |

---

## Audit Triggers

| Trigger | Audit Type | Automatic? |
|---------|-----------|:----------:|
| Scheduled cadence (weekly/monthly) | Standard | ✅ (if hook configured) |
| User request ("run an audit") | Any type | Manual |
| Score drops below threshold | Regression | ✅ |
| Architecture change reconciled | Focused (affected categories) | ✅ (via downstream signal) |
| Tier graduation request | Deep (readiness assessment) | Manual |
| Pre-release gate | Standard | ✅ (if CI/CD hook configured) |
| New team member (after 2 weeks) | Quick pulse | Manual |

---

## The Audit Report Structure

```markdown
# Compliance Audit Report — {date}

## Executive Summary
Score: {N}% | Tier: {N} | Trend: {↑↓→}
Critical: {N} | High: {N} | Medium: {N} | Low: {N}

## Score Breakdown
{category table with scores and trends}

## Findings
### Critical (fix immediately)
{rule ID, description, affected files, recommended action}

### High (fix this sprint)
...

## Drift Analysis
{stale rules, dead rules, orphaned hooks}

## Baseline Progress
Started: {N} violations | Current: {N} | Resolved: {N} | New: {N}

## Tier Readiness
{assessment for next tier if applicable}

## Recommendations
1. {prioritized actions}
```

---

## Related Documents

| Document | Location |
|----------|----------|
| How GCE Derivation Pipeline Works | `knowledge_docs/HOW_GCE_DERIVATION_PIPELINE_WORKS.md` |
| How GCE Rederivation Works | `knowledge_docs/HOW_GCE_REDERIVATION_WORKS.md` |
| How to Run a Compliance Audit | `knowledge_docs/HOW_TO_RUN_A_COMPLIANCE_AUDIT.md` |
| How to Scale Governance as Project Matures | `knowledge_docs/HOW_TO_SCALE_GOVERNANCE_AS_PROJECT_MATURES.md` |
| Why Governance Automation Matters | `knowledge_docs/WHY_GOVERNANCE_AUTOMATION_MATTERS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
