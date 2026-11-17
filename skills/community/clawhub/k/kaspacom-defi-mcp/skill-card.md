## Description:

KaspaCom DeFi MCP exposes an MCP server and CLI for querying and transacting across KaspaCom DEX, Lending, and LFG Launchpad on IGRA and Kasplex mainnet/testnet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marciano147](https://clawhub.ai/user/marciano147)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to connect Claude, Cursor, Codex, or a CLI workflow to KaspaCom DeFi for protocol queries, DEX data, lending positions, launchpad activity, and wallet-enabled transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path uses an unpinned global npm package.

Mitigation: Review the package source and version before installation, and avoid global installation where possible.

Risk: Wallet-enabled operation can sign financial transactions.

Mitigation: Test on igra-testnet or kasplex-testnet first, use a dedicated low-value wallet, and keep primary private keys out of MCP server configuration.

Risk: Write actions may execute swaps, lending operations, liquidity changes, or launchpad buys.

Mitigation: Run read-only tools unless a transaction preview clearly shows what will be signed and the user explicitly approves it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marciano147/skills/kaspacom-defi-mcp)
- [ClawHub publisher profile](https://clawhub.ai/user/marciano147)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include read-only protocol queries or wallet-enabled transaction guidance depending on user configuration.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
