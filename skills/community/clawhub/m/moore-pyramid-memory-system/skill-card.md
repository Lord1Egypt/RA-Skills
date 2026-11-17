## Description:

Provides a five-layer workspace memory structure for preserving cross-session notes, summaries, and todos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tosspi](https://clawhub.ai/user/tosspi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to maintain durable workspace memory across sessions, including daily summaries, weekly and monthly archives, and persistent cross-session todos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reloads broad conversation history automatically, which can preserve sensitive or unwanted information across sessions.

Mitigation: Use explicit opt-in, retention, deletion, review, and sensitive-data redaction rules before enabling durable memory.

Risk: Loaded memory could be mistaken for authoritative instructions during future sessions.

Mitigation: Treat loaded memory as reference material that cannot override the current user request, applicable policies, or higher-priority instructions.

## Reference(s):

- [Moore Pyramid Memory System on ClawHub](https://clawhub.ai/tosspi/skills/moore-pyramid-memory-system)
- [tosspi publisher profile](https://clawhub.ai/user/tosspi)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance]

**Output Format:** [Markdown instructions with file structure, rules, and schedules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable artifact files were included in the release evidence; the skill describes memory files, startup loading behavior, todo handling, and archive schedules.]

## Skill Version(s):

1.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
