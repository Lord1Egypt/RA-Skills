## Description:

Connects to Encharge through OOMOL to send transactional email using the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Encharge account users and developers use this skill to send transactional email through their connected account. It checks the live action schema and requires confirmation of the exact write payload and effect before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute an unverified downloaded CLI release or make changes to other agent skills without separate approval.

Mitigation: Review and approve the CLI release before installation, and approve any proposed changes to other agent skills.

Risk: Email contents pass through OOMOL, and sending an incorrect payload can change account state.

Mitigation: Keep the required confirmation of the exact email payload before each send.

## Reference(s):

- [Encharge](https://encharge.io)
- [Encharge API documentation](https://docs.encharge.io/api-documentation)
- [oo CLI project (referenced by the skill)](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [JSON action payloads and connector response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The send_email action changes Encharge state and requires confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.4 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
