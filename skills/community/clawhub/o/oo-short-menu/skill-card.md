## Description:

Short Menu (shortmenu.com). Use this skill for ANY Short Menu request — reading, creating, updating, and deleting data. Whenever a task involves Short Menu, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents use this skill to read, create, update, and delete Short Menu links through an OOMOL-connected account. It provides CLI guidance for checking action schemas and sending JSON payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may direct the agent to run a remote oo CLI installer, which can make changes on the local system.

Mitigation: Review and install the oo CLI separately before enabling this skill, including its effects on other installed agent skills.

Risk: Connector requests are processed by OOMOL, and create, update, or delete actions can change Short Menu data.

Mitigation: Connect only the intended Short Menu account, inspect the action schema, and retain confirmation for changes and deletions.

## Reference(s):

- [Short Menu API documentation](https://docs.shortmenu.com/api-reference/introduction)
- [Short Menu homepage](https://shortmenu.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Short Menu ClawHub release page](https://clawhub.ai/oomol/skills/oo-short-menu)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Guidance]

**Output Format:** [Markdown instructions with shell command examples and JSON payloads; connector responses in JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can create, update, or delete Short Menu links; write and destructive actions require confirmation.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
