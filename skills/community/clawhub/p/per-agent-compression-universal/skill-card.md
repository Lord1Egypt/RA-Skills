## Description:

Zero-config memory consolidation for multi-agent OpenClaw deployments that auto-discovers agents and registers staggered cron tasks with state tracking, deduplication, and domain-aware extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bensk2001](https://clawhub.ai/user/bensk2001)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to install recurring per-agent memory consolidation jobs that extract durable facts from older daily notes and append them to each agent's long-term memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation creates recurring jobs that can process every discovered agent's private memory notes.

Mitigation: Back up memory files before installation and manually limit or remove cron tasks for agents that should not be included.

Risk: The skill appends profile-derived content to long-term memory files without a built-in review gate.

Mitigation: Review generated USER.md, IDENTITY.md, SOUL.md, and MEMORY.md entries after initial runs and remove incorrect or sensitive content manually.

Risk: Uninstall removes scheduled tasks but does not undo note moves or appended memory entries.

Mitigation: Keep pre-install backups and verify processed notes and appended memory files before relying on uninstall as cleanup.

Risk: Task summaries may be sent through configured delivery channels.

Mitigation: Review DingTalk or other delivery settings during installation and use only intended recipients.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bensk2001/skills/per-agent-compression-universal)

## Skill Output:

**Output Type(s):** [shell commands, configuration, markdown, text]

**Output Format:** [Installer-created cron tasks plus Markdown memory entries and JSON state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw CLI and jq; creates recurring per-agent cron tasks and appends to USER.md, IDENTITY.md, SOUL.md, and MEMORY.md.]

## Skill Version(s):

1.4.0 (source: frontmatter, skill.json, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
