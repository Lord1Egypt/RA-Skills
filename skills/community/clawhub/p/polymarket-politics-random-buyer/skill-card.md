## Description:

Randomly finds a live Polymarket politics market, checks trading context, and buys 1 USDC by default with explicit dry-run and live modes for AION Market.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssj124](https://clawhub.ai/user/ssj124)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill as an AION-compatible Polymarket trading template that discovers politics markets, checks market context, and either reports a dry-run decision or executes an explicitly enabled live trade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated or scheduled live trading can spend wallet funds or create unwanted market positions.

Mitigation: Keep the skill in dry-run mode until reviewed, require explicit --live for execution, and use only a dedicated low-balance wallet with a scoped API key.

Risk: The optional auto-redeem action is not documented in the skill description and may have SDK effects the operator has not reviewed.

Mitigation: Avoid --auto-redeem until redemption behavior is documented, gated, and tested in a controlled environment.

Risk: Unpinned dependencies can change trading or wallet behavior over time.

Mitigation: Run the skill in a locked environment with reviewed dependency versions before enabling live or scheduled operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssj124/skills/polymarket-politics-random-buyer)
- [Publisher profile](https://clawhub.ai/user/ssj124)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Console text summary with optional JSON trade result and Markdown documentation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to dry-run; live execution requires an explicit --live flag and configured AION and wallet credentials.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
