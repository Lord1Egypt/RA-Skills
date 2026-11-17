## Description:

Polymarket Alpha Suite provides Node.js tools for scanning Polymarket prediction markets for arbitrage, latency, BTC momentum, universe, and edge signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiagent234-bit](https://clawhub.ai/user/aiagent234-bit)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading analysts use this skill to run Node.js-based public market scans, dry-run signal monitoring, and local exports for Polymarket opportunity research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for sensitive trading and wallet credentials.

Mitigation: Use public-data scans and dry-run modes only; do not provide wallet private keys or live trading credentials to this version.

Risk: The release advertises live automation that the reviewed code does not actually implement.

Mitigation: Treat generated signals as informational output that requires manual review, not as verified automated trade execution.

Risk: Continuous monitoring commands can keep running and write local JSON files under the skill directory.

Mitigation: Run watch, cron, or nohup modes only when continuous monitoring is intentional, and review or clean local data files as needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiagent234-bit/skills/polymarket-alpha-suite)
- [Publisher profile](https://clawhub.ai/user/aiagent234-bit)
- [Polymarket](https://polymarket.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, JSON files]

**Output Format:** [Markdown instructions with bash commands, terminal output, and optional JSON export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+; public-data scans can run without credentials; dry-run and export modes may write local JSON files under data/.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
