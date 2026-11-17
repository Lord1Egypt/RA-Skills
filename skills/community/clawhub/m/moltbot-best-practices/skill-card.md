## Description:

Best practices for AI agents - Cursor, Claude, ChatGPT, Copilot. Avoid common mistakes. Confirms before executing, drafts before publishing. Vibe-coding essential.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextfrontierbuilds](https://clawhub.ai/user/nextfrontierbuilds)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI-agent users use this skill to guide coding and automation agents toward safer collaboration habits, including confirming ambiguous tasks, seeking approval before publishing, stopping on user cancellation, and escalating repeated tool failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended memorySearch/sessionMemory configuration can expose past session transcripts in shared, sensitive, or client-work environments.

Mitigation: Avoid enabling broad persistent memory globally; prefer narrowly scoped opt-in memory with clear deletion and rollback controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nextfrontierbuilds/skills/moltbot-best-practices)
- [Publisher profile](https://clawhub.ai/user/nextfrontierbuilds)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with inline JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes behavioral rules and an optional memory configuration example for agents.]

## Skill Version(s):

1.1.3 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
