## Description:

Runs a continuous static market-making loop for Polymarket 5-minute crypto markets by placing fixed-price limit sell orders on both UP and DOWN tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thony32](https://clawhub.ai/user/thony32)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to start a Polymarket 5-minute crypto market-making bot, choose the asset scope, and set the initial share allocation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real-money Polymarket orders continuously when run with a funded wallet.

Mitigation: Review before installing or running with funds, use strict share and notional caps, and keep active monitoring in place.

Risk: Background execution may continue until manually stopped.

Mitigation: Prefer foreground or bounded execution for review, and define clear stop and monitoring commands before use.

Risk: The advertised 8% stop-loss should not be treated as account-level protection.

Mitigation: Use independent account controls and authenticated fill and balance reconciliation.

Risk: Dependencies are version-ranged rather than pinned.

Mitigation: Pin dependencies and review updates before running the skill in a live trading environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thony32/skills/polymarket-maker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON runtime status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can initiate a continuous trading loop and requires operator-controlled allocation and monitoring.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
