## Description:

Scan a resolved Polymarket market for wallets exhibiting suspicious trading patterns: fresh funding, single-market focus, extreme ROI, late entry at high prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to examine a resolved Polymarket market and identify wallets whose funding age, market focus, returns, entry prices, position size, or labels match suspicious-pattern indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research calls can trigger supported x402 payments from the configured wallet, and calls in a loop can each incur a payment.

Mitigation: Use the configured wallet's payment policy and spending limits, and account for per-call costs before scanning multiple wallets.

Risk: Wallet flags indicate suspicious patterns and may be mistaken for proof of misconduct.

Mitigation: Review the underlying market and wallet data before drawing conclusions from a score or flag.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nansen-devops/skills/nansen-polymarket-insider-scan)
- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell command examples and a scoring table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
