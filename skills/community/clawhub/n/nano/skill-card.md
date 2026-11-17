## Description:

Helps an assistant operate Nano (XNO) wallets, check transactions and balances, validate addresses, and look up ledger activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casualsecurityinc](https://clawhub.ai/user/casualsecurityinc)

### License/Terms of Use:

MIT-0

## Use Case:

People and developers with configured Nano wallets use this skill to send and receive XNO, inspect balances and transaction history, create payment requests, and answer Nano protocol questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real XNO transfers or refunds can send funds to the wrong recipient or exceed intended spending.

Mitigation: Before each send, independently confirm the source wallet, full destination address, amount, and spending limit; require explicit authorization before changing the limit.

Risk: Unpinned package execution can run a different version than the reviewed release.

Mitigation: Avoid the unpinned `npx -y xno-skills mcp` fallback; use a version-pinned installation.

Risk: Sharing private keys or mnemonics with an assistant can expose wallet secrets.

Mitigation: Never paste private keys or mnemonics into the assistant; perform any raw-key operation locally outside the conversation.

## Reference(s):

- [Nano (XNO) ClawHub release](https://clawhub.ai/casualsecurityinc/skills/nano)
- [Nano protocol](https://nano.org)
- [Wallet sending](artifact/references/send.md)
- [Payment refunds](artifact/references/payment.refund.md)
- [MCP setup](artifact/references/mcp.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Text, Markdown, and structured JSON tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide full wallet addresses, transaction details, and payment QR codes.]

## Skill Version(s):

5.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
