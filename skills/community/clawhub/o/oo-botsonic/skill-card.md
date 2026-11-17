## Description:

Botsonic (botsonic.com). Use this skill for ANY Botsonic request — reading, creating, and updating data. Whenever a task involves Botsonic, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate Botsonic responses and retrieve conversations or FAQs through a connected Botsonic account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute remote installer code that has not been verified.

Mitigation: Review and approve the CLI installation before running setup.

Risk: Startup synchronization may add persistent agent skills without clearly disclosing those changes.

Mitigation: Disable startup skill synchronization when only the Botsonic integration is needed.

Risk: Hosted connector behavior has not been verified, and connected access may allow writes.

Mitigation: Connect only the account access needed and retain confirmation for write actions.

## Reference(s):

- [Botsonic REST API documentation](https://docs.botsonic.com/docs/rest-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Shell commands, Guidance]

**Output Format:** [JSON action payloads and returned Botsonic data; Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action payloads follow the live schema for the selected Botsonic action.]

## Skill Version(s):

1.0.6 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
