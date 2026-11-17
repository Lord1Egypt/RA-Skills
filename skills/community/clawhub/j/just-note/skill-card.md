## Description:

Manage personal markdown notes - search, read, create, and append to notes when the user asks to jot down an idea, find a note, list notes, or add something to an existing note.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanthar91](https://clawhub.ai/user/lanthar91)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage a local markdown notes directory, including creating notes, appending daily quick notes, listing notes, and searching by content or tag.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell examples can be unsafe with crafted note paths, search terms, titles, tags, or note bodies.

Mitigation: Review before installing; use only normalized relative note paths, quote paths, pass search terms as data, and write note content through safe stdin or filesystem APIs.

Risk: The skill manipulates persistent local notes and could alter user data if a request is ambiguous.

Mitigation: Confirm note titles, tags, destination paths, and any destructive action with the user before changing note files.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and filesystem paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and updates local markdown note files with optional YAML frontmatter.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
