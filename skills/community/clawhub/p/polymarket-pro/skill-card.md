## Description: <br>
Use the official Polymarket CLI to browse markets, trade on CLOB, manage positions, and analyze on-chain data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liwagu](https://clawhub.ai/user/liwagu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to research Polymarket prediction markets, manage wallet and portfolio workflows, and prepare or execute direct CLOB and CTF trading operations through the official CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support live trading and order cancellation workflows involving real funds. <br>
Mitigation: Use a dedicated low-balance wallet and manually confirm token, side, price, size, approvals, and cancellation scope before each transaction. <br>
Risk: Wallet private keys may be supplied through CLI flags, environment variables, or config files. <br>
Mitigation: Avoid passing private keys on the command line, restrict config file permissions, and keep trading credentials separate from primary wallets. <br>
Risk: The documented shell-script installation path executes a remote installer. <br>
Mitigation: Prefer Homebrew or a verified pinned release, and review installer contents before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liwagu/polymarket-pro) <br>
- [Polymarket CLI repository](https://github.com/Polymarket/polymarket-cli) <br>
- [Polymarket CLI install script](https://raw.githubusercontent.com/Polymarket/polymarket-cli/main/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-output CLI examples intended for jq or automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
