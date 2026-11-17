## Description:

Secure multi-account management for NEAR Protocol with encrypted credential storage, account switching, and balance aggregation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaiss](https://clawhub.ai/user/shaiss)

### License/Terms of Use:

MIT

## Use Case:

Developers, organizations, traders, DeFi users, and advanced NEAR users use this skill to manage multiple NEAR accounts, switch active accounts, check balances, transfer NEAR, and summarize account holdings from one agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release bundles unrelated authenticated marketplace deliverable/job scripts and an exposed token.

Mitigation: Remove the bundled deliverable/job scripts and exposed token before installation or release.

Risk: Private-key storage has weak safeguards if the built-in default encryption key is used.

Mitigation: Require a real user-provided or OS-backed secret for key storage and verify local storage permissions before storing keys.

Risk: The skill can initiate real NEAR mainnet transfers.

Mitigation: Add clear mainnet transfer confirmations and declare the needed filesystem, environment, network, and wallet-operation capabilities.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shaiss/skills/near-multi-account-manager)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [NEAR Mainnet RPC](https://rpc.mainnet.near.org)
- [NEAR Explorer](https://explorer.mainnet.near.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured JSON-like operation results with JavaScript usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute NEAR account operations, local encrypted account storage updates, balance queries, transaction lookups, imports, exports, and mainnet transfers.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact package manifests report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
