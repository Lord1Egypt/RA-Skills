## Description:

Operate Polymarket from terminal with the `polymarket` Rust CLI (v0.1.5), including market discovery, CLOB queries, wallet and approval management, order placement and cancellation, portfolio data, CTF operations, rewards, bridge deposits, sports metadata, API key management, and JSON output for automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seandong](https://clawhub.ai/user/seandong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate the Polymarket CLI from an agent, including read-only market research, account checks, and carefully confirmed trading or wallet actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial or account-control commands can place orders, cancel orders, change approvals, manage API keys, reset wallets, or initiate bridge deposits.

Mitigation: Require the agent to show the exact command, parameters, wallet context, and expected effect, then wait for explicit user confirmation before execution.

Risk: The skill includes curl-to-shell installation guidance.

Mitigation: Prefer Homebrew or a pinned, verifiable release; if using a script, inspect and pin the downloaded content before execution.

Risk: Passing private keys on the command line can expose secrets through shell history, process listings, or logs.

Mitigation: Avoid command-line private keys when possible and use a reviewed secret-management path; redact secrets from displayed commands and logs.

Risk: Incorrect market, token, side, price, amount, signature type, or bridge address can cause unintended financial actions.

Mitigation: Run preflight checks, echo critical parameters before writes, start with small test amounts, and verify results immediately after execution.

## Reference(s):

- [Command Reference](references/commands.md)
- [Troubleshooting](references/troubleshooting.md)
- [Polymarket CLI repository](https://github.com/Polymarket/polymarket-cli)
- [ClawHub skill page](https://clawhub.ai/seandong/skills/poly-cli)
- [Publisher profile](https://clawhub.ai/user/seandong)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON-output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose executable Polymarket CLI commands; programmatic workflows should request CLI JSON output with `-o json`.]

## Skill Version(s):

0.1.5 (source: server release metadata and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
