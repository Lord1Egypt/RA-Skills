## Description:

Especialista em Obsidian com dominio em Zettelkasten, PARA, BASB, MOCs, Dataview, Templater e organizacao estruturada de vaults.

This skill is ready for commercial/non-commercial use.

## Publisher:

[playandogamer150-commits](https://clawhub.ai/user/playandogamer150-commits)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Obsidian users can use this skill to manage a personal knowledge vault with note creation, search, frontmatter editing, daily notes, Canvas, Dataview, templates, tasks, and vault health workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read, reorganize, overwrite, and delete content across an Obsidian vault.

Mitigation: Use a dedicated test vault first and keep independent backups or version control before granting access to important notes.

Risk: Delete, folder move, rename, and archive operations may permanently lose or misplace notes if executed without sufficient review.

Mitigation: Require manual review outside the skill before approving destructive or bulk organization actions.

Risk: Sensitive note contents may be exposed through broad vault access.

Mitigation: Avoid connecting vaults that contain sensitive notes until scoped controls are added.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and structured text responses, with configuration guidance for Obsidian Local REST API environment variables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and updates Obsidian vault content through local REST API tools when configured with user-provided API credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
