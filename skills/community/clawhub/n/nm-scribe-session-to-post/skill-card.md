## Description:

Converts a Claude Code session into a blog post, case study, or Reddit post

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to turn a Claude Code work session into a blog post, case study, social thread, or Reddit post that explains the work and its results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to run project tests and builds.

Mitigation: Review the source-discovery behavior and project commands first, and proceed only when you trust the project being tested.

Risk: Session-derived recordings or posts may expose sensitive information when published.

Mitigation: Review recordings and drafts for sensitive information before sharing or publishing them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-scribe-session-to-post)
- [Scribe plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scribe)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown posts or plain-text social content, shaped to the selected format]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Narrative content based on the session context and evidence supplied; review before publication.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
