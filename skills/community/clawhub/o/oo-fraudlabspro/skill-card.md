## Description:

Use FraudLabs Pro to screen orders, retrieve screening results, and submit approve or reject feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can screen order transactions for fraud risk, retrieve screening results, and submit approve or reject feedback through an OOMOL-connected FraudLabs Pro account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Order submissions may be treated as reads, and a missing CLI can trigger automatic execution of an unverified installer.

Mitigation: Review action effects and approve screening payloads, customer-data sharing through OOMOL, and credit use. Install a reviewed, fixed CLI release separately and check its automatic skill synchronization settings.

## Reference(s):

- [FraudLabs Pro](https://www.fraudlabspro.com/)
- [FraudLabs Pro API documentation: Screen Order](https://www.fraudlabspro.com/developer/api/screen-order)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-fraudlabspro)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Markdown instructions with shell command examples, JSON payloads, and connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions use the connected FraudLabs Pro account; action schemas should be checked before payloads are sent.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
