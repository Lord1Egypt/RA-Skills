## Description: <br>
Operate Polymarket from terminal with the `polymarket` Rust CLI (v0.1.5), covering market, event, tag, and series discovery; CLOB queries; wallet and approval management; order placement and cancelation; portfolio and on-chain data; CTF operations; rewards; bridge deposits; sports metadata; API key management; and JSON output for automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seandong](https://clawhub.ai/user/seandong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate the Polymarket CLI for market discovery, CLOB queries, wallet setup, approvals, trading actions, bridge deposits, and automation-friendly JSON workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through live trading, approvals, bridge deposits, wallet resets, and credential actions. <br>
Mitigation: Use a separate low-balance wallet and require manual confirmation before every trade, approval, bridge action, API-key change, bulk cancel, or wallet reset. <br>
Risk: Private keys and API credentials may be exposed if supplied in chat or shell arguments. <br>
Mitigation: Do not put private keys in chat or command arguments; prefer reviewed local configuration or environment handling and redact secrets from logs. <br>
Risk: Installation paths include fetching or building external CLI code before use. <br>
Mitigation: Use a pinned and reviewed install method before enabling the skill to operate a wallet. <br>


## Reference(s): <br>
- [Command reference](references/commands.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports default table output for human review and `-o json` output for automation.] <br>

## Skill Version(s): <br>
0.1.5 (source: release evidence and skill description) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
