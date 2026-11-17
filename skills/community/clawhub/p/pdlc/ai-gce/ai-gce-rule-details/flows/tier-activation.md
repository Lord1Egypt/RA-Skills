<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mode 4: Tier Activation (Compliance Tier Upgrade) — Full Flow

## Purpose

This file holds the complete **Mode 4 (Tier Activation)** flow: when triggered, the interaction model, the tier-specific questions, and the 9-step activation flow. The tier model and readiness criteria themselves live in `common/process-overview.md` ("Three-Tier Progressive Compliance" + "Tier Readiness Criteria"); the activation FLOW lives here.

The Mode 4 entry (purpose + trigger) lives in `core-generator.md` (the always-loaded dispatcher). Load this file when Mode 4 is detected.

---

## When Triggered

Mode 4 is triggered when a project is ready to advance from its current compliance tier to the next. It is NOT a new derivation — it is a progressive activation of rules and hooks that were deferred at initial generation time.

**Trigger signals:**
- User says "activate tier 2" / "activate next tier" / "upgrade compliance"
- `.compliance-state.json` shows all `nextTierReadiness.criteria` as true
- PM runs the tier activation accelerator

## Interaction Model

1. **User invokes:** "Activate next compliance tier"
2. **AI reads** `.compliance-state.json` → determine current tier and next tier
3. **AI verifies** all readiness criteria for the next tier (checks actual workspace state)
4. **AI asks** tier-specific questions (2-4 per tier — see below)
5. **AI activates** new rules and hooks for this tier
6. **AI runs** compliance audit with newly activated rules
7. **AI presents** new score, gap report, and next actions

## Tier-Specific Questions

**Activating Tier 2 (3 questions):**
- What CI pipeline type is in use? (GitHub Actions / GitLab CI / Azure DevOps / Other)
- Are all team members listed in CODEOWNERS? (If no — prompt to update first)
- Which modules have active development? (Determines domain-specific rule activation)

**Activating Tier 3 (4 questions):**
- What is the release version/tag?
- Who are the external stakeholders for sign-off?
- Which compliance frameworks apply? (SOX / GDPR / ISO 27001 / None)
- Target deployment environment? (Cloud / On-Premise / Hybrid)

## Tier Activation Flow

```
STEP 1: READ CURRENT STATE
───────────────────────────
Read .compliance-state.json:
• Current tier (1, 2, or 3)
• Tier history
• Next tier readiness criteria and their status
• Last audit score

STEP 2: VERIFY READINESS CRITERIA
────────────────────────────────────
For each criterion in nextTierReadiness.criteria:
• Check actual workspace state (don't trust cached values in state file)
• Report: "Criterion X: ✅ Met / ❌ Not met — {reason}"
• If any criteria unmet: warn but allow PM to override (full activation mode)

STEP 3: ASK TIER-SPECIFIC QUESTIONS
──────────────────────────────────────
Ask the 2-4 questions specific to this tier upgrade.
Derive everything else from workspace state — no unnecessary questions.

STEP 4: ACTIVATE NEW RULES
────────────────────────────
Load rules that belong to this tier (tagged in rule files with tier number).
For Tier 2: governance-checklist, role-isolation, steering-governance, devops-deployment
For Tier 3: security-compliance, change-management, full phase-gates

STEP 5: INSTALL NEW HOOKS
───────────────────────────
Install hooks that belong to this tier.
For Tier 2: post-task-governance, segregation-check, security-gate-check,
            enforce-module-structure, cross-module-reference-check, 
            steering-quality-check, auto-run-tests
For Tier 3: change-readiness-gate, exception-expiry-check

STEP 6: RUN COMPLIANCE AUDIT WITH NEW RULES
─────────────────────────────────────────────
Run full audit with all activated rules (Tier 1 + newly activated Tier N).
Expected: score will dip as new rules expose new gaps — this is expected and healthy.

STEP 7: UPDATE STATE FILE
───────────────────────────
Update .compliance-state.json:
• Set complianceTier to new tier number
• Add tierHistory entry with date, activatedBy, scoreAtActivation
• Update nextTierReadiness for the NEXT tier
• Update complianceScore with new audit result

STEP 8: REGENERATE COMPLIANCE DASHBOARD
─────────────────────────────────────────
Regenerate management_framework/dashboards/compliance-dashboard.md with new tier state:
• Tier progress bars updated
• New rules inventory showing newly activated rules
• New hooks roadmap showing what was installed and what's next
• Gap report for newly discovered violations
• Updated score history

STEP 9: OUTPUT — Tier Activation Summary
──────────────────────────────────────────
"⬆️ COMPLIANCE TIER {N} ACTIVATED

Active rules:    {list of newly activated rule categories}
Active hooks:    {list of newly installed hooks}
New audit score: {score}% ({rating}) — was {previous score}%
Score delta:     {+/- change} (dip is expected as new rules expose gaps)

Top gaps from new rules:
  🔴 {critical finding 1}
  🟠 {high finding 2}
  🟡 {important finding 3}

Next tier ({N+1}) readiness: {criteria met count}/{total} criteria
Blockers: {list}

Updated: .compliance-state.json | management_framework/dashboards/compliance-dashboard.md"
```
