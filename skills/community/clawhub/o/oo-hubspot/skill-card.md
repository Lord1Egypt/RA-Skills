## Description:

Supports reading, creating, and updating HubSpot CRM data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to inspect HubSpot CRM records and properties, search CRM data, and perform supported create or update actions through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute remote software and install additional agent skills; the remote installer and live connector code were not available in the reviewed artifact.

Mitigation: Review and explicitly approve a verified CLI release before setup, including any additional skill installation.

Risk: Connecting HubSpot authorizes OOMOL-mediated account access, and CRM changes can alter business records.

Mitigation: Grant only the permissions needed and retain confirmation for the exact CRM changes.

## Reference(s):

- [HubSpot API documentation](https://developers.hubspot.com/docs/api/overview)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [HubSpot skill listing](https://clawhub.ai/oomol/skills/oo-hubspot)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown instructions with shell commands and JSON inputs and responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read or change CRM records; write actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
