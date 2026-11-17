## Description:

OpenBytes provides end-to-end network API workflows for wallet signature-based authentication, on-chain top-up monitoring, consumer API key management, model inference, and balance or usage queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viyozc](https://clawhub.ai/user/viyozc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate or debug OpenBytes API workflows, including wallet authentication, top-up verification, API key lifecycle management, model calls, and balance or usage checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated wallet private keys, API keys, session tokens, or unredacted API responses could be exposed in chat or logs.

Mitigation: Do not let an agent generate or display wallet private keys, keep API responses redacted, and store credentials only in user-controlled secure storage.

Risk: API-key creation, revocation, on-chain top-up, or parent-wallet linking commands can affect account access or funds.

Mitigation: Require explicit user confirmation before running any credential lifecycle, top-up, or wallet-linking command.

Risk: Wallet signature flows can fail or bind the wrong relationship if message contents, casing, timestamp, or signer are incorrect.

Mitigation: Have the user perform signatures in their wallet and verify exact message text, normalized addresses, and timestamp window before submission.

## Reference(s):

- [OpenBytes Gateway API](https://gateway.openbytes.ai)
- [ethers.js Wallet.createRandom](https://docs.ethers.org/v6/api/wallet/#Wallet-createRandom)
- [viem createWallet](https://viem.sh/docs/actions/wallet/createWallet.html)
- [Base Sepolia RPC](https://sepolia.base.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl commands, JSON examples, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command templates containing placeholders for user-provided wallet addresses, session tokens, API keys, and base URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
