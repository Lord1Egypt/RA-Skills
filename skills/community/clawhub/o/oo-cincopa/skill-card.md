## Description:

Cincopa (cincopa.com). Use this skill for ANY Cincopa request — searching and reading data. Whenever a task involves Cincopa, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to search and read assets, galleries, tags, and gallery items in a Cincopa account connected through OOMOL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup commands download and execute an installer, and the installer and hosted connector implementation were not verified in the supplied evidence.

Mitigation: Review the setup steps, use a verified fixed CLI release, and require approval before installing it locally.

Risk: Automatic skill synchronization could let Cincopa-related requests change other agent skills.

Mitigation: Consider disabling automatic skill synchronization.

Risk: Connecting Cincopa entrusts credentials and requested account access to OOMOL.

Mitigation: Review the requested access and connect only when you are comfortable entrusting that access to OOMOL.

## Reference(s):

- [Cincopa API documentation](https://developer.cincopa.com/apis)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Cincopa](https://www.cincopa.com/)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only connector actions; returned data is provided as JSON.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
