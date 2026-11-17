## Description:

Optimization suite for OpenClaw agents to prevent token leaks and context bloat through background task isolation, reset-and-summarize workflows, local RAG, transcript indexing, and hybrid search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[klautimus](https://clawhub.ai/user/klautimus)

### License/Terms of Use:

MIT

## Use Case:

Developers and external OpenClaw users use this skill to configure agent memory and background-task workflows that reduce context bloat, lower token use, and preserve searchable long-term recall.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transcript indexing can make historical OpenClaw sessions searchable, including secrets, personal data, proprietary code, or sensitive tool output.

Mitigation: Use a small allowlist of sanitized transcript paths, prefer local-only embeddings, set retention limits, and rebuild or delete indexes when source data should no longer be searchable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/klautimus/skills/openclaw-token-memory-optimizer)
- [README](README.md)
- [Skill instructions](SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown guidance with JSON configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an optional local shell status check script; review transcript indexing guidance before use with sensitive session data.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and package.json report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
