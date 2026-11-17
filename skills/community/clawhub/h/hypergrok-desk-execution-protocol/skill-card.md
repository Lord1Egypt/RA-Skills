## Description:

The Execution Trader's procedure for turning an approved ticket into one Hyperliquid action and reconciling it, including the pre-send checklist, order construction rules, single-send discipline, unknown-result handling, and the execution report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Execution Traders use this procedure to validate approved Hyperliquid tickets, send a single action, handle uncertain results, and reconcile orders and account exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides live trading actions, where incorrect ticket details, account or network selection, approval coverage, or reconciliation could cause unintended exposure or leave an outcome unresolved.

Mitigation: Before use, verify the mandate, account, network, native approval gate, Risk PASS, and user approval checks. Reconcile each send and treat an unknown result as possibly executed.

Risk: Some referenced files were missing from the partial security scan, so the security evidence is incomplete.

Mitigation: Review the full skill and its referenced files and confirm the checks fit the intended desk setup before installing or using it.

## Reference(s):

- [HyperGrok Desk Execution Protocol release](https://clawhub.ai/galleonlabs/skills/hypergrok-desk-execution-protocol)
- [Project link cited in ATTRIBUTION.md](https://github.com/galleonlabs/hypergrok-trading-desk)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls]

**Output Format:** [Markdown checklists and execution reports, with instructions for a single exchange action]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an approved ticket, risk checks, and current account and order state.]

## Skill Version(s):

1.9.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
