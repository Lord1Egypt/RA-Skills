## Description:

Archives local documents into a knowledge base with AI-assisted categorization, batch processing, full-text indexes, search, and statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[141553](https://clawhub.ai/user/141553)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to organize work documents into local categories, build searchable indexes, and query or report on archived files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processing crafted or untrusted Office documents or directories may trigger unsafe command execution paths.

Mitigation: Review before installing, avoid untrusted inputs, and replace shell-based extraction paths with argument-based subprocess calls before broader deployment.

Risk: AI classification and optional cloud upload can expose document names, excerpts, summaries, or full files outside the local machine.

Mitigation: Keep AI classification and cloud upload disabled unless the endpoint, destination, credentials, and data-sharing approval have been validated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/141553/skills/kb-archiver)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local archive folders, copied files, text indexes, and manifest records when its bundled script is executed.]

## Skill Version(s):

1.1.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
