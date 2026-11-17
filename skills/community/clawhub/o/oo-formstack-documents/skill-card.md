## Description:

Use Formstack Documents through a connected OOMOL account to read, create, copy, update, and delete templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Formstack Documents templates and inspect their merge fields through an existing OOMOL connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may make additional changes in agent directories through automatic skill synchronization, and the remote installer effects were not verified.

Mitigation: Use a verified CLI release, review its installation separately, and set OO_SKILLS_SYNC_DISABLED=1 before invoking it to disable the documented automatic synchronization.

## Reference(s):

- [Formstack Documents](https://forms.formstack.com/products/documents)
- [Formstack Documents API documentation](https://www.webmerge.me/developers)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes read, write, and destructive actions; the skill requires confirmation before writes and explicit approval before deletion.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
