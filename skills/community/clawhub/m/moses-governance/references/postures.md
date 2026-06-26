# MO§ES™ Posture Controls — Reference

## SCOUT
**Behavior:** Information gathering only.
**Transaction policy:** NO transactions. NO state changes.
**Constraints:** Read-only operations exclusively. Gather, analyze, report — do not act. Flag opportunities for operator review.
**When to use:** Initial assessment, reconnaissance, market analysis before committing capital, due diligence phase.

## DEFENSE
**Behavior:** Protect existing positions.
**Transaction policy:** Outbound transfers require explicit operator confirmation.
**Constraints:** Prioritize capital preservation. Flag any action that reduces holdings. Require double confirmation for transfers exceeding 10% of position. Monitor for threats.
**When to use:** Volatile markets, risk management, custody operations, when protecting assets is the priority.

## OFFENSE
**Behavior:** Execute on opportunities.
**Transaction policy:** Permitted within governance mode constraints. All executions logged.
**Constraints:** Execute opportunities that pass governance checks. Still bound by governance mode. Log all execution decisions with rationale. Track performance.
**When to use:** Active trading, deployment, when the operator has assessed risk and is ready to act.

## Posture Interaction with Governance Modes

Posture and governance mode combine. Examples:

| Mode + Posture | Result |
|---|---|
| High Security + SCOUT | Maximum caution. Read-only. Every data point verified. |
| High Security + DEFENSE | Protective. Outbound blocked without confirmation + verification. |
| High Security + OFFENSE | Executes but with full verification chain and confirmation required. |
| Creative + SCOUT | Explore ideas freely, no execution. |
| Creative + OFFENSE | Experimental execution — but still audited. |
| Research + SCOUT | Deep investigation, gather everything, act on nothing. |
| None + OFFENSE | Full autonomy. Audited but unconstrained. Operator accepts all risk. |

Posture is the throttle. Governance mode is the rulebook. Both always apply.
