## Description:

Real-time knowledge base synchronization for AI assistants, including inotifywait file monitoring, Git auto-push and pull, Nutstore sync, and multi-device consistency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alfredming-2026](https://clawhub.ai/user/alfredming-2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to keep AI assistant knowledge files synchronized across a server workspace, Nutstore, Git, and local Obsidian-style workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Continuous synchronization can copy, delete, commit, and upload workspace content with limited guardrails.

Mitigation: Use a narrowly scoped workspace with no secrets or private credentials, and inspect all sync destinations before enabling the skill.

Risk: Automated Git operations may publish unintended files.

Mitigation: Replace broad Git staging with an allowlist, remove hook bypasses, and add dry-run or confirmation steps before scheduled pushes.

Risk: Systemd services or cron jobs can run synchronization unattended.

Mitigation: Do not enable persistent services or jobs until the Git remote, Nutstore destination, Obsidian destination, and deletion behavior are reviewed.

## Reference(s):

- [Knowledge Sync ClawHub Release](https://clawhub.ai/alfredming-2026/skills/knowledge-sync)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and shell configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational guidance for systemd services, cron jobs, Git synchronization, and file sync destinations.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
