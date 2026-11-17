## Description:

Use the official Polymarket CLI to browse markets, trade on CLOB, manage positions, and analyze on-chain data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liwagu](https://clawhub.ai/user/liwagu)

### License/Terms of Use:


## Use Case:

Developers, analysts, and trading operators use this skill to issue Polymarket CLI commands for market research, order-book analysis, wallet checks, order management, portfolio review, and CTF operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands can place orders, set approvals, perform CTF operations, and otherwise affect real funds or account authority.

Mitigation: Use a dedicated low-balance trading wallet, confirm each transaction before execution, and avoid unattended use for live trading.

Risk: Wallet private keys may be exposed through chat, shell history, scripts, environment variables, or configuration files.

Mitigation: Do not paste real private keys into chats or command history; use safer wallet storage practices and rotate any credential that may have been exposed.

Risk: The shell-script installer fetches and executes remote code.

Mitigation: Prefer the package-manager install path or a pinned, verified release, and review installer contents before running them.

## Reference(s):

- [Polymarket CLI repository](https://github.com/Polymarket/polymarket-cli)
- [ClawHub skill page](https://clawhub.ai/liwagu/skills/polymarket-pro)
- [Publisher profile](https://clawhub.ai/user/liwagu)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes CLI command examples for table and JSON output modes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
