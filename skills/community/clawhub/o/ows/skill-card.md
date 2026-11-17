## Description:

Guides agents in using a pre-installed OWS CLI for local-first multi-chain wallet management, balance checks, transaction and message signing, x402 payments, and wallet information queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rhlsthrm](https://clawhub.ai/user/rhlsthrm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to guide agents through local wallet balance checks, wallet information queries, transaction or message signing, and x402 payments with a user-installed OWS CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet signing or x402 payment actions can transfer value or authorize messages if approved without review.

Mitigation: Before signing or payment, require the agent to show the wallet name, chain, destination or URL, amount, fees, and exact transaction or message for explicit user approval.

Risk: Raw private keys could expose wallet funds if requested, copied, or stored outside the wallet tool.

Mitigation: Do not provide raw private keys; use OWS internal signing only.

Risk: Installing or updating wallet packages during task execution can change the trusted wallet environment.

Mitigation: Use only a user-installed OWS CLI and do not install or update OWS packages during the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rhlsthrm/skills/ows)
- [Open Wallet Standard website](https://openwallet.sh)
- [Open Wallet Standard core repository](https://github.com/open-wallet-standard/core)
- [@open-wallet-standard/core npm package](https://www.npmjs.com/package/@open-wallet-standard/core)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and TypeScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a pre-installed local OWS CLI; wallet actions require user review and approval.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
