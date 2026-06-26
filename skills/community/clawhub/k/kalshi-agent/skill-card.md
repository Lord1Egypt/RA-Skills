## Description: <br>
Kalshi prediction market agent - analyzes markets and executes trades via the Kalshi v2 API <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JThomasDevs](https://clawhub.ai/user/JThomasDevs) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to browse Kalshi markets, inspect market details and order books, review portfolio state, and prepare or execute trades through the Kalshi CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use stored credentials to place real-money trades on a funded Kalshi account. <br>
Mitigation: Require explicit human approval before any buy, sell, or cancel command is executed, and review the market, side, quantity, price, and account impact before approval. <br>
Risk: The `--force` option can bypass trade confirmation prompts. <br>
Mitigation: Disallow `--force` unless a human explicitly approves bypassing the confirmation step for the specific trade. <br>
Risk: Kalshi credentials and RSA private keys are stored in local files or shell configuration. <br>
Mitigation: Restrict permissions on `~/.kalshi` and `~/.kalshi/private_key.pem`, verify the upstream `kalshi-cli` package before installation, and avoid exporting credentials through shell configuration unless reviewed. <br>


## Reference(s): <br>
- [Kalshi API Reference](https://docs.kalshi.com/api-reference/) <br>
- [kalshi-cli](https://github.com/JThomasDevs/kalshi-cli) <br>
- [Kalshi API Credentials](https://kalshi.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include market analysis, portfolio status summaries, and trade commands that can affect a funded Kalshi account.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
