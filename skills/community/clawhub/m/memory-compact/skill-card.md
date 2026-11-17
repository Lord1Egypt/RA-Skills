## Description:

Automatically processes daily OpenClaw memory files, extracts a small set of key points, appends them to long-term memory, and backs up the source memory file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garryfan-ai](https://clawhub.ai/user/garryfan-ai)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users can use this skill to compact daily conversation-derived memory into a persistent MEMORY.md file and archive the original dated memory file. It is intended for recurring local memory maintenance, including scheduled execution through cron.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can promote sensitive conversation-derived memory into persistent MEMORY.md.

Mitigation: Review extracted key points before or after each run, and delete any sensitive or incorrect retained memory.

Risk: The optional cron setup can create recurring agent runs that process memory automatically.

Mitigation: Enable the cron job only after review, keep the schedule visible to operators, and remove or disable it when automatic memory compaction is no longer wanted.

Risk: Processed source memory files are moved into backups and may remain available indefinitely.

Mitigation: Apply a retention policy for backup/memory/ and periodically remove backups that should not persist.

Risk: Path checks rely on local filesystem behavior while the skill processes workspace memory files.

Mitigation: Add symlink-safe path validation and review workspace permissions before deploying in shared or sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/garryfan-ai/skills/memory-compact)
- [Publisher profile](https://clawhub.ai/user/garryfan-ai)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration]

**Output Format:** [Markdown files and console text with optional cron configuration commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes selected memory lines to MEMORY.md, moves processed dated memory files into backup/memory/, and emits status messages.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
