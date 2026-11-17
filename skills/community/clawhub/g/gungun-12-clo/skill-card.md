## Description:

An AI agent self-improvement skill that records learnings, detects errors, promotes knowledge, and reports learning statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alsoforever](https://clawhub.ai/user/alsoforever)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture conversation-derived lessons, error context, feature requests, and recurring patterns, then promote reviewed lessons into persistent agent knowledge files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill records interaction-derived content to persistent workspace files, which may retain conversation, customer, error, or command context.

Mitigation: Apply redaction and retention rules before deployment, and review stored learning records for sensitive content.

Risk: Promotion commands can change long-lived agent knowledge files such as SOUL.md, AGENTS.md, TOOLS.md, and MEMORY.md.

Mitigation: Require explicit human review before promoting lessons into persistent agent behavior or knowledge files.

Risk: A generic promotion path can write promoted content to broader destination files than intended.

Mitigation: Restrict promotion to approved destination files or disable the generic promote command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alsoforever/skills/gungun-12-clo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown records, command-line reports, and guidance for updating agent knowledge files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent learning, error, feature-request, statistics, and promoted-knowledge content in workspace Markdown files.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
