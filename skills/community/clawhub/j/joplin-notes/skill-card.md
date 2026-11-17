## Description:

Interface for managing Joplin notes via WebDAV. Allows listing notebooks and notes, reading content (first line = title), and creating or updating notes and notebooks. Use this skill when the user wants to access or modify their Joplin database programmatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martin004](https://clawhub.ai/user/martin004)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and update a Joplin note database synchronized through WebDAV, including listing notebooks, reading note content, and creating or updating notes and notebooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses WebDAV credentials and can modify remote Joplin notes.

Mitigation: Install only when the publisher is trusted, use an HTTPS-only WebDAV URL, restrict the WebDAV account to the Joplin directory, and keep backups before write operations.

Risk: The security scan recommends review before installation because note paths, credential handling, temporary files, and bundled script resolution need hardening.

Mitigation: Review the scripts before deployment and consider validating IDs, avoiding curl password arguments, using secure temporary files, and resolving bundled scripts relative to the skill directory.

## Reference(s):

- [Joplin Notebook IDs Reference](references/notebooks.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WebDAV connection settings and can read or write remote Joplin Markdown files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
