## Description:

Monitor and discuss research papers from one Paperzilla project using the `pz` CLI inside OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pors](https://clawhub.ai/user/pors)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and teams use this skill to triage recent Paperzilla project feed items, inspect selected papers, summarize markdown-backed paper content, explain relevance to current work, and produce recurring weekday research briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an already-authenticated Paperzilla CLI and may access project paper feeds and markdown.

Mitigation: Install only when the user is comfortable with authenticated Paperzilla access; the skill is limited to Paperzilla read and triage workflows and explicitly avoids unrelated files, environment variables, and credentials.

Risk: Recurring briefs can be delivered through the configured chat surface.

Mitigation: Send externally only for scheduled/profile-required delivery or when the user explicitly requests it, and confirm ambiguous destinations before sending.

Risk: Weekday briefs keep a small per-project history of proposed paper IDs to avoid repeats.

Mitigation: Persist only the exact Paperzilla IDs needed for deduplication in profile-owned state and allow revisiting papers when the user asks.

## Reference(s):

- [Paperzilla CLI Guide](https://docs.paperzilla.ai/guides/cli)
- [ClawHub skill page](https://clawhub.ai/pors/skills/paperzilla-research-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and concise chat text, with inline Paperzilla CLI commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send scheduled or explicitly requested research briefs through the configured OpenClaw chat surface.]

## Skill Version(s):

1.1.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
