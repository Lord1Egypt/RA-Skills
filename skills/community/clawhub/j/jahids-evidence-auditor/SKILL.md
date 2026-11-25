---
name: jahids-evidence-auditor
description: Check whether mission claims and deliverables are supported by reproducible evidence and explicit verification results.
---

# JAHIDS Evidence Auditor

## Use when
Reviewing mission completion, repository changes, test results, or claims about external actions.

## Procedure
1. Map each acceptance criterion to an evidence item.
2. Check evidence source, timestamp, identity, scope, and integrity.
3. Re-run safe tests when the environment permits.
4. Distinguish observed facts from assumptions and recommendations.
5. Mark each criterion PASS, FAIL, BLOCKED, or NOT_TESTED.
6. Report missing evidence and unresolved risks.
7. Do not claim a commit, merge, deployment, or deletion without a confirming result.

## Output
An evidence ledger, verification summary, and explicit unresolved items.

## Authority boundary
An audit report cannot approve the action it reviews.
