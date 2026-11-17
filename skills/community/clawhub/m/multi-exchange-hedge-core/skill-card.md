## Description:

Automated funding rate arbitrage and delta-neutral hedging. Simultaneously manages positions on OKX and Binance to harvest fee premiums.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmstudio667-commits](https://clawhub.ai/user/tmstudio667-commits)

### License/Terms of Use:


## Use Case:

External developers and trading automation operators use this skill to identify funding-rate arbitrage opportunities across OKX and Binance and manage delta-neutral spot/futures positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact trading automation may create financial loss if run without clear exchange-side limits or prior testing.

Mitigation: Use sandbox or paper trading first, avoid withdrawal-enabled API keys, and set exchange-side position and IP restrictions.

Risk: The usage command invokes an unpinned runtime package.

Mitigation: Do not run the npx command unless the OpenClaw package version is pinned and verified.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/tmstudio667-commits/skills/multi-exchange-hedge-core)
- [ClawHub Publisher Profile](https://clawhub.ai/user/tmstudio667-commits)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trading automation guidance should be reviewed before execution and tested with sandbox or paper-trading accounts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
