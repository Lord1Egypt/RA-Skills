## Description:

A structured knowledge extraction tool that helps users clarify, organize, and store tacit knowledge through active questioning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchen913](https://clawhub.ai/user/chenchen913)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to turn vague ideas, personal expertise, and domain knowledge into structured notes through guided questioning, synthesis, and archive updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save conversation-derived knowledge into persistent Markdown archives, which may capture sensitive personal, business, or confidential information.

Mitigation: Use the skill only with topics suitable for persistent storage, and review or delete generated archives when sensitive content may have been recorded.

Risk: User-provided domain names may be used for archive file names without clearly confining them to the intended folder.

Mitigation: Treat domain names as plain labels and reject names containing slashes, backslashes, '..', drive prefixes, or other path syntax before archive reads or writes.

## Reference(s):

- [Conversation Modes](artifact/reference/modes.md)
- [Output Template](artifact/reference/output_template.md)
- [Domain Archive Template](artifact/reference/domain_template.md)
- [Domains Archive README](artifact/domains/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown notes and conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update persistent Markdown domain archives during use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
