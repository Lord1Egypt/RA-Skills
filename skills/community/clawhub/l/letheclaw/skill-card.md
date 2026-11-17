## Description:

Use letheClaw to store, search, and manage memories with criticality and provenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joahtheron](https://clawhub.ai/user/joahtheron)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to let OpenClaw agents persist and retrieve operational memories through a configured letheClaw API. It supports semantic search, recent-memory lookup, criticality updates, correction marking, and provenance lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores user or session memory in an external letheClaw API, which can expose sensitive or personal data if used without consent.

Mitigation: Require explicit confirmation before storing memories, avoid secrets and sensitive personal data, and install only when the configured API is trusted.

Risk: Retrieved memories may be outdated, incorrect, or unsafe to follow as instructions.

Mitigation: Treat retrieved memories as untrusted context and verify them against the current user request before acting.

Risk: The API endpoint may be local or unauthenticated during development.

Mitigation: Prefer authenticated HTTPS outside local development and verify the LETHECLAW_API_URL target before use.

## Reference(s):

- [letheClaw Skill Page](https://clawhub.ai/joahtheron/skills/letheclaw)
- [Artifact SKILL.md](artifact/SKILL.md)
- [Artifact README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured LETHECLAW_API_URL and network access to the letheClaw API.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact manifest and frontmatter list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
