## Description:

Lean Context helps agents reduce token usage by applying context compression, selective loading, prompt deduplication, caching, and efficient tool definitions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awalesagar](https://clawhub.ai/user/awalesagar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent builders use Lean Context to audit and reduce token usage in prompts, skills, tool outputs, and agent workflows while preserving task quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill suggests disabling agent approval controls, which can increase exposure during file writes, command execution, credential access, network calls, deployments, or public-facing actions.

Mitigation: Keep approval controls enabled for normal use; only disable them in disposable, tightly scoped environments with no secrets, production access, or destructive permissions.

## Reference(s):

- [Compression Deep Dive](references/compression-deep-dive.md)
- [Lean Context ClawHub Release](https://clawhub.ai/awalesagar/skills/lean-context)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline checklists, tables, and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include token audits, compression recommendations, configuration snippets, and cost-saving formulas.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
