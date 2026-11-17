## Description:

Use Close to read, create, and update CRM data through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users use this skill to retrieve or manage Close leads, contacts, opportunities, and tasks through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: When the CLI is missing, setup instructions can lead to running unverified third-party installation code without separate approval.

Mitigation: Verify the CLI source, then review and explicitly approve the installation and any bundled-skill changes before setup.

Risk: Connecting Close gives OOMOL access to CRM requests and credentials.

Mitigation: Review the account access before connecting and retain the required confirmation for all write actions.

## Reference(s):

- [Close](https://www.close.com)
- [Close API documentation](https://developer.close.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-close)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns Close CRM records or action results; write actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
