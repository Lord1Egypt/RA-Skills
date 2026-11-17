## Description:

Cluster and attribute related wallets — funding chains, shared signers, CEX deposit patterns. Use when tracing wallet ownership, comparing two wallets, finding wallet relationships, governance voters, or related address clusters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users can use this skill to investigate wallet ownership and relationships, compare addresses, and summarize attribution signals with confidence and role information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses and query details sent to Nansen may reveal which wallets or relationships are being investigated.

Mitigation: Before querying, consider whether you are comfortable sharing the target addresses and investigation details with Nansen; follow the documented expansion protocol and ask before querying newly discovered addresses.

Risk: Research calls, including calls in loops, can incur x402 payments from the configured wallet under its existing authorization and spending limits.

Mitigation: Check the selected authentication method, wallet authorization, payment policy, and spending limits before research; minimize calls and keep trace width at 3 or less.

## Reference(s):

- [Wallet Attribution — Reference](artifact/REFERENCE.md)
- [Browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)
- [Nansen Wallet Clustering on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-wallet-clustering)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Shell commands]

**Output Format:** [Markdown attribution summary with address, owner, confidence, signals, and role; CLI commands as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Attribution is organized around wallet addresses and confidence levels.]

## Skill Version(s):

0.1.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
