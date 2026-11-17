## Description:

Google Workspace Enterprise License Manager: Manage product licenses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:


## Use Case:

Administrators and developers use this skill to guide Google Workspace Enterprise License Manager operations through the gws CLI, including assigning, revoking, listing, and updating product license assignments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: License assignment, revocation, patch, and update commands can change or remove user access.

Mitigation: Review proposed gws licensing commands before approving execution, and inspect method parameters with gws schema before building params or JSON flags.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-licensing)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and shared Google Workspace authentication prerequisites.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
