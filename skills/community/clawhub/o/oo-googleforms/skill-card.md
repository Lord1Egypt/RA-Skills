## Description:

Use Google Forms through an OOMOL-connected account to read, create, and update forms and responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can inspect forms and responses, create forms, and update forms through a connected Google Forms account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified software whose documented behavior includes installing additional persistent agent skills.

Mitigation: Review and approve the CLI installation separately, consider disabling automatic skill synchronization, and connect only the Google Forms permissions needed.

Risk: Form write actions can change or publish form data and settings.

Mitigation: Review the exact payload and effect with the user before running a write action, and retain confirmation for changes.

## Reference(s):

- [OO CLI](https://github.com/oomol-lab/oo-cli)
- [OO CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Google Forms](https://workspace.google.com/products/forms/)
- [Google Forms API reference](https://developers.google.com/workspace/forms/api/reference/rest)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payloads; structured connector responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on the selected Google Forms action.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
