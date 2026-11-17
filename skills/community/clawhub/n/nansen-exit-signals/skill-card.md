## Description:

Is smart money exiting a token I hold? Net flow direction, seller breakdown by label, and recent SM trades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Crypto token holders and analysts use this skill to review smart-money flows, seller labels, and recent trades for signs that traders may be exiting a token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A supported HTTP 402 response can spend funds from the configured wallet, and each research call, including calls in loops, can incur a payment.

Mitigation: Check wallet authorization, payment policy, and spending limits before running; keep research calls bounded because each call may incur a payment.

## Reference(s):

- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Guidance]

**Output Format:** [Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Token and chain values are supplied to research commands; calls may incur payments under the configured wallet policy.]

## Skill Version(s):

0.1.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
