## Description:

Query live Hedera blockchain data including token prices, whale movements, HCS topics, governance proposals, identity/KYC screening, and smart contract analysis through pay-per-call HBAR micropayments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mountainmystic](https://clawhub.ai/user/mountainmystic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent query Hedera network data, inspect tokens, monitor HCS topics, check identity and governance signals, and perform paid or on-chain HederaToolbox MCP operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The billing identifier is a public Hedera account ID, which evidence.security identifies as a real authorization concern.

Mitigation: Use only a small prepaid HBAR balance unless the publisher documents stronger account-ownership verification or revocable credentials.

Risk: Paid or on-chain write operations can consume remote balance or create records through the platform account.

Mitigation: Review planned tool calls before execution, keep prepaid balances limited, and require user confirmation for paid or HCS write workflows.

Risk: Tool calls and query details are sent to HederaToolbox.

Mitigation: Avoid sending sensitive identifiers or confidential query details unless the deployment has reviewed the service privacy and retention posture.

## Reference(s):

- [HederaToolbox website](https://hederatoolbox.com)
- [HederaToolbox MCP endpoint](https://api.hederatoolbox.com/mcp)
- [HederaToolbox GitHub repository](https://github.com/mountainmystic/hederatoolbox)
- [Payment watcher source](https://github.com/mountainmystic/hederatoolbox/blob/master/src/watcher.js)
- [Hashscan platform account](https://hashscan.io/mainnet/account/0.0.10309126)
- [ClawHub skill page](https://clawhub.ai/mountainmystic/skills/hederatoolbox)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON tool-call examples and environment configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May lead the agent to call a remote MCP service that returns live Hedera data, consumes prepaid HBAR balance, or creates HCS records through the platform account.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
