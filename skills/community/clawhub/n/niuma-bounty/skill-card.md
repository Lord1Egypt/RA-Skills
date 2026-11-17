## Description:

Interact with the Niuma Bounty on-chain task platform on XLayer testnet to query, create, join, submit, review, bid, approve, reject, and manage bounty tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[futeyaoshi](https://clawhub.ai/user/futeyaoshi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents working with the Niuma Bounty platform use this skill to inspect XLayer testnet bounty data and prepare or execute task lifecycle transactions, including task creation, participation, submissions, review, bidding, staking, and profile binding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Executable contract addresses differ from the addresses shown in the skill documentation.

Mitigation: Review references/contracts.json and the intended XLayer testnet contracts before signing transactions; prefer read-only commands until addresses are reconciled.

Risk: Write paths can grant unlimited NIUMA allowances and can use a private key supplied through NIUMA_WALLET_SECRET.

Mitigation: Prefer the build-tx external wallet path, use testnet-only keys for direct signing, and revoke NIUMA allowances after use.

Risk: On-chain task approvals, rejections, staking, inviter binding, and submissions may be irreversible or may lock stake.

Mitigation: Run the precheck commands where available and manually verify task IDs, participants, amounts, token addresses, and contract addresses before signing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/futeyaoshi/skills/niuma-bounty)
- [Niuma Bounty Platform](https://task.niuma.works)
- [OKX Agentic Wallet documentation](https://web3.okx.com/zh-hans/onchainos/dev-docs/home/install-your-agentic-wallet)
- [XLayer testnet explorer](https://www.oklink.com/xlayer-test)
- [Contract addresses](references/contracts.json)
- [Contract ABIs](references/abis.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI output or unsigned transaction payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require XLayer testnet RPC access and a wallet secret or external wallet for write transactions; read-only queries do not require credentials.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
