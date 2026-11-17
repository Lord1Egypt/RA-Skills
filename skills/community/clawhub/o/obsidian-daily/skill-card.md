## Description:

Manage Obsidian Daily Notes through obsidian-cli by creating and opening daily notes, appending journal, log, task, and link entries, reading notes by date, and searching vault content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bastos](https://clawhub.ai/user/bastos)

### License/Terms of Use:


## Use Case:

Obsidian users and developers use this skill to have an agent prepare daily-note workflows, including creating notes, appending entries, reading dated notes, and searching vault content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell command templates may mix journal entries, search terms, vault names, or paths directly into commands.

Mitigation: Review and quote user-provided values before execution, avoid pasting arbitrary text into shell templates, and prefer safe argument passing.

Risk: The artifact manifest contains unresolved merge-conflict markers.

Mitigation: Resolve the manifest conflict markers and verify frontmatter before broad use or redistribution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires obsidian-cli and an accessible Obsidian vault configured by the user.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
