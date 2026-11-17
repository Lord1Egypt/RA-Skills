## Description:

Which of these addresses are smart money? Batch-profile a list in one call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers can batch-profile selected blockchain wallet addresses with Nansen and identify addresses labeled as smart money or funds. The skill also explains authentication, per-address errors, and possible payment behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitting selected wallet addresses to Nansen may reveal private research interests or associations.

Mitigation: Before running, consider whether you are comfortable sending each selected address to Nansen and whether the list could reveal private research interests or associations.

Risk: A supported HTTP 402 challenge can spend funds from the configured wallet, and each call in a batch or loop can incur a payment.

Mitigation: Review the configured wallet authorization, payment policy, and spending limits before running; account for possible charges on each call.

## Reference(s):

- [Nansen browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)
- [Nansen Wallet Batch on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-wallet-batch)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON]

**Output Format:** [Markdown with shell commands and JSON response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch address input; results may include per-address errors, and supported calls may incur a payment.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
