## Description:

Provides guidance and a small Python helper for joining text files, with release evidence noting that the bundled helper currently concatenates corresponding lines rather than performing field-based joins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to request guidance or commands for combining records from two text files. Users should verify behavior before relying on it for field-based joins because release security evidence says the bundled helper only concatenates matching line numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation describes SQL-like field joins, while the bundled script only concatenates corresponding lines from two files.

Mitigation: Confirm the installed implementation supports the requested join options, or correct the skill to describe simple line concatenation before using it for relational data operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/join-tool)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include join commands or helper-code guidance; verify against the installed implementation before use on relational data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
