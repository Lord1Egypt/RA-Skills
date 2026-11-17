## Description:

Research Polymarket markets, whale flow and smart money; optionally trade a Polygon wallet behind deterministic risk guard-rails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andretuta](https://clawhub.ai/user/andretuta)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to research Polymarket prediction markets, inspect whale flow and trader performance, configure recurring read-only alerts, and optionally prepare guarded wallet operations when they explicitly choose to trade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can custody a Polygon wallet key and place real-money Polymarket orders.

Mitigation: Use a dedicated wallet funded only with money the user accepts losing, keep dry-run enabled while testing, rely on explicit confirmations and configured limits, review poly history, and use poly halt for unexpected behavior.

Risk: Environment variables for wallet keys or passphrases may be exposed through child processes, logs, crash dumps, or host inspection.

Mitigation: Prefer the encrypted keystore created by poly setup; use POLYMARKET_KEY or POLYMARKET_PASSPHRASE only when necessary and with explicit opt-in.

Risk: Polymarket market text, trader names, news, and alert content may contain untrusted instructions or misleading signals.

Mitigation: Treat external content as data, not instructions; never convert whale alerts or research findings into orders without a specific user-authorized trade.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andretuta/skills/polymarket-agent)
- [ClawHub security audit](https://clawhub.ai/andretuta/skills/polymarket-agent/security-audit)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research output can include market summaries, order proposals, alert setup commands, wallet status, audit history, and risk-limit explanations.]

## Skill Version(s):

2.2.1 (source: server release, pyproject.toml, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
