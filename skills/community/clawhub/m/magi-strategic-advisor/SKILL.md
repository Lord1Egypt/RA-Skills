# MAGI Strategic Advisor

## Trigger Conditions

| Scenario | Activation Signal | Action |
|----------|------------------|--------|
| Multi-option selection | User provides 2+ candidate options | Load references/decision-matrix.md |
| Major decision | Significant resource investment or irreversible consequences | Load references/magi-framework.md |
| Risk evaluation | User requests risk assessment or high-risk signals present | Load references/decision-matrix.md |
| Multi-angle analysis | User requests analysis from different perspectives | Load references/magi-framework.md |
| Conflict tradeoff | Obvious stakeholder conflicts or goal contradictions | Load references/decision-matrix.md |

## Capability Index

| Capability | Description | Reference File | Optional User Prompt |
|-----------|-------------|---------------|----------------------|
| Strategic Analysis | Decompose complex problems, build multi-dimensional frameworks | references/magi-framework.md | User may copy prompts/01-implement-method.md |
| Risk Assessment | Six-domain risk scanning with probability-impact matrix | references/decision-matrix.md | User may copy prompts/02-robustness-checks.md |
| Multi-option Comparison | Systematic side-by-side evaluation of competing proposals | references/method-patterns.md | User may copy prompts/01-implement-method.md |

## Quick-Reference: Output Format

```
## Conclusion and Recommendation
[One-sentence conclusion + recommended option]

## MELCHIOR Judgment
[Rational analysis content]

## BALTHASAR Judgment
[Risk assessment content]

## CASPER Judgment
[Intuitive insight content]

## Comprehensive Verdict
Vote result: [X:Y:Z]
Final recommendation: [Specific action]
Prerequisites: [Under what conditions this recommendation holds]
Monitoring indicators: [What signals to watch after execution]
```

## Quick-Reference: Voting Rules

| Vote Pattern | Verdict | Action |
|-------------|---------|--------|
| 3:0 unanimous | High confidence | Execute immediately |
| 2:1 majority | Conditional | Execute with reservations and monitoring indicators |
| 1:1:1 split | Insufficient information | Suspend decision, gather more information |
| Veto triggered | Mandatory reject | Reject regardless of other votes |

## Quick-Reference: Veto Conditions

- Irreversible legal or compliance risk exists
- Worst-case scenario exceeds organizational tolerance threshold
- Core assumptions unverified and verification cost is prohibitively high
- Key stakeholders explicitly oppose and positions cannot be reconciled
- Time window has closed or resource gap cannot be bridged

## File Routing Map

| User Intent | Primary File | Secondary Files |
|------------|-------------|----------------|
| Strategic analysis | references/magi-framework.md | references/decision-matrix.md |
| Risk assessment | references/decision-matrix.md | references/magi-framework.md, scripts/risk-matrix-gen.py |
| Multi-option comparison | references/decision-matrix.md | references/method-patterns.md, scripts/weighted-scoring.py |
| General framework reference | references/magi-framework.md | — |
| Scoring templates | references/decision-matrix.md | — |
| Code patterns | references/method-patterns.md | scripts/*.py |
