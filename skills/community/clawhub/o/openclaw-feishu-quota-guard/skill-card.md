## Description:

Use when a user wants OpenClaw itself to diagnose or fix Feishu/Lark quota burn caused by heartbeats, health checks, webhook probes, or overly expensive background runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[herbertwyt](https://clawhub.ai/user/herbertwyt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to diagnose and reduce Feishu/Lark quota burn caused by frequent heartbeats, health checks, webhook probes, or expensive background runs. It guides safe OpenClaw heartbeat configuration changes and flags custom gateway or webhook code for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The diagnostic scanner can read broad personal folders and print sensitive matching lines from logs or configuration files.

Mitigation: Run scanner commands with explicit workspace roots when possible, review output as sensitive, and avoid sharing scanner output that may contain tokens or private configuration.

Risk: The bundled fixer can edit OpenClaw heartbeat configuration.

Mitigation: Run with --dry-run first, pass explicit --config and --workspace paths when possible, and review the planned heartbeat changes before allowing writes.

Risk: The installer overwrites an existing installed copy of this skill.

Mitigation: Confirm the destination skill directory before installation and keep any local customizations backed up outside the target directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/herbertwyt/skills/openclaw-feishu-quota-guard)
- [Source notes](references/source-notes.md)
- [OpenClaw heartbeat docs](https://docs.openclaw.ai/heartbeat)
- [OpenClaw gateway heartbeat docs](https://docs.openclaw.ai/gateway/heartbeat)
- [OpenClaw Feishu channel docs](https://docs.openclaw.ai/channels/feishu)
- [Bilibili quota-burn source video](https://www.bilibili.com/video/BV1fvcuzVEsc/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run local scripts that inspect OpenClaw workspace files and edit OpenClaw heartbeat configuration after a dry run.]

## Skill Version(s):

0.2.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
