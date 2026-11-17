## Description:

Analyze crypto wallet holdings, P&L, win rate, trading history, token balances, and developer-created tokens through GMGN portfolio CLI workflows across Solana, BSC, Base, and Ethereum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmgnai](https://clawhub.ai/user/gmgnai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run GMGN portfolio analysis for wallet due diligence, copy-trading research, token balance checks, and developer-created token reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install an unpinned global gmgn-cli package.

Mitigation: Pin and verify the CLI package before installation, and prefer an isolated environment for execution.

Risk: The skill handles GMGN API keys and private keys, including persistent local configuration.

Mitigation: Avoid sending secrets in chat, use a secure secret store or non-logged prompt, restrict local config permissions, and rotate or delete keys written to files or temporary paths.

Risk: Wallet-analysis requests expose GMGN portfolio data to the execution environment.

Mitigation: Run the skill only in environments approved for the wallet-analysis data being queried.

## Reference(s):

- [GMGN Skill Portfolio on ClawHub](https://clawhub.ai/gmgnai/skills/gmgn-portfolio)
- [GMGN API key setup](https://gmgn.ai/ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses parsed GMGN CLI results and avoids raw JSON dumps unless further command-line processing is needed.]

## Skill Version(s):

1.4.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
