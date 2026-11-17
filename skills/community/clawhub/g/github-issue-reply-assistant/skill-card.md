## Description:

Free basic version that drafts a structured GitHub issue response and triage checklist. Reserves premium upgrade hooks for multilingual replies and fix-draft generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wingogx](https://clawhub.ai/user/wingogx)

### License/Terms of Use:


## Use Case:

Developers and maintainers use this skill to draft initial GitHub issue replies, assign a suggested label, and generate a short triage checklist from an issue title and body.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill always returns a premium upgrade object with a payment link, which may be unexpected in a GitHub issue reply workflow.

Mitigation: Review the monetization behavior before installation and use only when payment-link presentation is intended.

Risk: The payment URL can be configured through environment variables and includes the user identifier.

Mitigation: Restrict allowed payment hosts, encode user identifiers, and avoid exposing payment links without user confirmation.

Risk: Premium behavior is reserved and currently returns an upgrade-required response rather than generating premium outputs.

Mitigation: Treat premium features as unavailable unless a later release documents and implements them clearly.

## Reference(s):

- [SkillPay API Contract](references/skillpay-api-contract.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON response with reply text, suggested label, checklist, issue context preview, and upgrade metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free-tier output includes a premium upgrade object with price, payment URL, and reserved premium feature names.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
