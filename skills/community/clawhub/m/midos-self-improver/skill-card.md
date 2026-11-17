## Description:

Structured learning pipeline with quality-gated promotion that captures corrections, errors, and patterns, then promotes recurring learnings into project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msruruguay](https://clawhub.ai/user/msruruguay)

### License/Terms of Use:


## Use Case:

Developers and agent maintainers use this skill to capture corrections, tool errors, knowledge gaps, best practices, and recurring implementation patterns. It helps stage, score, and promote only repeated learnings into project-level agent memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to record project activity and preserve repeated user or tool output as lasting memory.

Mitigation: Use it only in trusted projects and treat learning logs as sensitive project data.

Risk: Automatic promotion into CLAUDE.md, AGENTS.md, or scheduled assessment can persist incorrect, sensitive, or personal information without enough review.

Mitigation: Require manual diff review, secret and personal-data redaction, path limits, audit history, and rollback controls before promotion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/msruruguay/skills/midos-self-improver)
- [MidOS](https://midos.dev)
- [artifact/SKILL.md](artifact/SKILL.md)
- [artifact/CHANGELOG.md](artifact/CHANGELOG.md)
- [artifact/benchmark/results.json](artifact/benchmark/results.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent memory capture guidance, rule promotion criteria, example entry schemas, and operational commands.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
