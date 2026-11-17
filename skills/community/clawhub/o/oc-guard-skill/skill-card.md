## Description:

Safe OpenClaw config planning/apply workflow with bilingual execution receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edmond-ai](https://clawhub.ai/user/edmond-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to plan, validate, and apply OpenClaw configuration changes with receipts, confirmation gates, backups, rollback behavior, and post-apply checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change high-impact OpenClaw settings and may affect tools, plugins, commands, channels, models, agents, and bindings.

Mitigation: Review generated plans and exact diffs before apply, use `apply --confirm` only after validation, and rely on documented backup, rollback, and canary checks.

Risk: Sensitive proposal, config, or runtime data may be exposed through proposal files or temporary diagnostic files.

Mitigation: Use only trusted sanitized proposal files, avoid real tokens and app secrets in proposals, and do not publish local OpenClaw config, logs, backups, or `/tmp/oc-guard-*` data.

Risk: Server security evidence marks the release as suspicious and recommends review before multi-user or production installation.

Mitigation: Perform installation review before use on shared or production hosts and verify changes under high-impact OpenClaw paths before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/edmond-ai/skills/oc-guard-skill)
- [README](README.md)
- [Safety Notes](docs/SAFETY.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and bilingual execution receipts with command examples and JSON proposal files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, openclaw, and opencode; guarded apply operations require explicit confirmation.]

## Skill Version(s):

1.1.2 (source: server release evidence and CHANGELOG, released 2026-03-06)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
