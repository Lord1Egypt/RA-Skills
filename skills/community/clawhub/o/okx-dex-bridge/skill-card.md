## Description:

Helps agents bridge tokens across supported chains using OKX OnchainOS by checking routes, comparing fees, preparing approvals or swap calldata, executing confirmed transfers, and tracking status until funds arrive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ok-james-01](https://clawhub.ai/user/ok-james-01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to guide agent-assisted cross-chain token transfers, including route discovery, quote comparison, approval handling, execution with confirmation gates, and status tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move real cross-chain assets and approvals can expand a bridge router's spending authority.

Mitigation: Require explicit user confirmation before approvals, execution, route pinning, force mode, skip-approve, or any non-default receive address.

Risk: Wrong token, chain, route, or destination address can cause permanent fund loss.

Mitigation: Resolve token addresses per chain, show quote and route details before execution, and require a second confirmation when the receive address differs from the sender wallet.

Risk: The pre-flight flow downloads and executes an updatable installer.

Mitigation: Prompt visibly before install or update, verify downloaded installer checksums, and verify the installed binary checksum before use.

## Reference(s):

- [OKX Web3](https://web3.okx.com)
- [OKX OnchainOS DEX Cross-Chain API Reference](https://web3.okx.com/onchainos/dev-docs/trade/cross-chain-api-reference)
- [CLI Command Reference](artifact/references/cli-reference.md)
- [Cross-Chain Troubleshooting](artifact/references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/ok-james-01/skills/okx-dex-bridge)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with CLI commands, tables, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include route comparison tables, approval instructions, transaction status summaries, and risk-gate prompts.]

## Skill Version(s):

3.1.3 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
