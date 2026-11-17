## Description:

Nummo connects AI agents to the user's bank accounts via Plaid, enabling financial insights through natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nummo-ai](https://clawhub.ai/user/nummo-ai)

### License/Terms of Use:


## Use Case:

External users and their agents use this skill to authenticate with Nummo, connect bank accounts through Plaid, review accounts and transactions, summarize spending and income, and manage Nummo subscriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install instructions use an unverified remote shell installer for a CLI that can access bank-account and transaction data.

Mitigation: Review the installer before running it; prefer a versioned release, checksum or signature verification, or a download-then-inspect flow; connect bank accounts only with explicit user consent and trust in Nummo.

## Reference(s):

- [Nummo skill page](https://clawhub.ai/nummo-ai/skills/nummo)
- [Install instructions](reference/install.md)
- [Nummo installer](https://nummo.ai/install)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and user-facing URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May present Plaid Link, Stripe checkout, or subscription-change URLs for the user to open in a browser.]

## Skill Version(s):

0.1.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
