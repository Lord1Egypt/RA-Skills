## Description:

Behavioral adaptation for AI agents. Builds a lightweight user profile from interaction history and adapts response style, topic focus, timing, and recovery when replies stop landing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pablothethinker](https://clawhub.ai/user/pablothethinker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to generate local behavioral profiles from interaction history and adapt agent response style, topic focus, timing, and recovery behavior for a user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps local behavioral profile data across sessions.

Mitigation: Install only when persistent profiling is acceptable, and periodically inspect or delete the skill data directory if retention is not desired.

Risk: The setup script installs mutable global npm code.

Mitigation: Review or pin the npm dependency before running setup.

Risk: Generated USER.md or SOUL.md content can alter future agent behavior.

Mitigation: Read generated profile text before appending it to persistent agent memory files.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/pablothethinker/skills/lineage-mini)
- [npm package](https://www.npmjs.com/package/lineage-code-mini)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON profile output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local behavioral profile data and SOUL.md or USER.md text snippets for review before use.]

## Skill Version(s):

0.1.3 (source: frontmatter and evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
