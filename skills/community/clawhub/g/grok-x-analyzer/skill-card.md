## Description:

Analyzes X (Twitter) posts, threads, trends, user activity, and related data to produce concise structure, engagement, and insight summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igorganapolsky](https://clawhub.ai/user/igorganapolsky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users can use this skill to inspect X/Twitter URLs, posts, threads, trends, and engagement signals and receive concise summaries or structured analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch X or web content without clear user-facing confirmation.

Mitigation: Require explicit user approval before external fetches when silent network access is not acceptable.

Risk: The skill can spawn subagents for deeper analysis without clear user control.

Mitigation: Require explicit user approval before delegating deep-dive analysis to subagents.

Risk: X/Twitter retrieval may require user-authenticated xurl access.

Mitigation: Use manual xurl authentication only and avoid exposing or reading local credential files.

## Reference(s):

- [xurl CLI Reference](references/xurl.md)
- [ClawHub Skill Page](https://clawhub.ai/igorganapolsky/skills/grok-x-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output may depend on availability of X/Twitter content, web fallback results, and user-authenticated xurl access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
