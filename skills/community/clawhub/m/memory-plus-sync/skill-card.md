## Description:

Memory Plus Sync synchronizes Feishu, WeChat, Telegram, and voice conversation memories into OpenClaw SQLite, with MCP tools, validation, deduplication, batch processing, version history, monitoring, alerts, and automatic recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lewistouchtech](https://clawhub.ai/user/lewistouchtech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to consolidate multi-channel conversation history into a shared memory store, operate on memories through MCP tools, and monitor the health of the underlying memory database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly handles private memories across configured channels and memory stores.

Mitigation: Review and narrow which channels and memories it may read, store, export, and delete before enabling synchronization.

Risk: Installer, cleanup, and automation behavior may alter local state or remove memory data.

Mitigation: Avoid sudo installation, require backups, and confirm dry-run behavior before enabling cleanup or cron-style automation.

Risk: Credential-bearing configuration or API keys could be exposed through source files or logs.

Mitigation: Keep secrets out of source files, use environment or secret-manager configuration, redact logs, and rotate any exposed credentials.

Risk: MCP server and command execution surfaces can expand local access if exposed broadly.

Mitigation: Bind services to trusted interfaces, restrict network access, and review command paths before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lewistouchtech/skills/memory-plus-sync)
- [README](artifact/README.md)
- [Skill Documentation](artifact/SKILL.md)
- [Release Notes](artifact/PUBLISH.md)
- [Skill Manifest](artifact/skill.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python examples, and JSON/API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read, write, export, delete, and synchronize memory records across configured channels and local services.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact/skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
