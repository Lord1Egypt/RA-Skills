## Description:

Trade on Hyperliquid DEX with simple commands. Place market/limit orders on perps, or run automated bots (market making, grid trading) with a web dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thisnewmark](https://clawhub.ai/user/thisnewmark)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to manage Hyperliquid perpetual futures trades and configure automated market-making or grid-trading bots through agent-issued shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to run trading commands, approve fees, and start automated bots against accounts holding user funds.

Mitigation: Require explicit confirmation before fee approvals, trades, bot starts, and emergency-stop actions; start with small amounts and use a limited-funds subaccount.

Risk: The skill asks users to run remote trading code with wallet credentials and limited integrity controls.

Mitigation: Verify the upstream repository and dependencies before installation, avoid main-wallet credentials, and keep private keys out of chat and command output.

Risk: Automated strategies can accumulate inventory, exceed intended exposure, or lose funds during trending or volatile markets.

Mitigation: Configure max exposure, leverage, drawdown, volatility, and emergency-stop settings before running bots, and monitor logs and positions after startup.

## Reference(s):

- [Perp Lobster skill page](https://clawhub.ai/thisnewmark/skills/perp-lobster)
- [Publisher profile](https://clawhub.ai/user/thisnewmark)
- [Project homepage](https://github.com/ThisNewMark/perplobster)
- [Config Parameter Reference](references/CONFIG_REFERENCE.md)
- [Strategy Selection Guide](references/STRATEGIES.md)
- [Troubleshooting Guide](references/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trading warnings, setup steps, bot configuration guidance, and commands that require explicit user confirmation before execution.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
