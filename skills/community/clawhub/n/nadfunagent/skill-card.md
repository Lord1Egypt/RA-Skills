## Description:

Autonomous Nad.fun trading agent that scans markets via API and indexer, analyzes tokens, executes trades, and shares profits with MMIND token holders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encipher88](https://clawhub.ai/user/encipher88)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use nadfunagent to monitor Nad.fun markets, evaluate candidate tokens, manage positions, execute Monad-based trades, and prepare profit-distribution steps for MMIND token holders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for a wallet private key and may store trading configuration in agent memory or local environment files.

Mitigation: Use a disposable, low-balance wallet; do not paste a valuable private key into chat; prefer a dedicated signer or locked-down local secret store.

Risk: The skill can run unattended financial transactions, including buys, sells, approvals, and profit distributions.

Mitigation: Disable cron until every transaction path is reviewed, and require manual confirmation before executing trades or distributions.

Risk: Automated trading can act on volatile market data or incorrect token analysis.

Mitigation: Keep position limits low, review token choices before execution, and test with dry runs or manual operation before enabling automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/encipher88/skills/nadfunagent)
- [Nad.fun](https://nad.fun)
- [Nad.fun Agent API](https://api.nadapp.net)
- [README](README.md)
- [Dependencies](DEPENDENCIES.md)
- [Trading Scripts](trading/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or environment-variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to call APIs and local Node.js trading scripts after required wallet and RPC configuration is available.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
