## Description:

Moesif (moesif.com). Use this skill for ANY Moesif request — searching and reading data. Whenever a task involves Moesif, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill to inspect a Moesif workspace and list apps, workspace templates, and workspaces through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions run remote CLI installers whose effects and any resulting skill changes have not been verified.

Mitigation: Review the installer through a separate trusted process, check for changes to other agent skills, and explicitly authorize those changes before proceeding.

Risk: Using the connector gives OOMOL-mediated access to the user's Moesif account.

Mitigation: Confirm that OOMOL should mediate this account access before connecting or running actions.

## Reference(s):

- [Moesif API documentation](https://www.moesif.com/docs/api)
- [Moesif homepage](https://www.moesif.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Text]

**Output Format:** [Shell commands and JSON connector responses, summarized as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include result data and an execution ID.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
