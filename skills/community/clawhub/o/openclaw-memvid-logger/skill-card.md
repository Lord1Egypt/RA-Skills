## Description:

Logs OpenClaw conversations and events with role tags, saving them to JSONL and Memvid for full-context search using monthly sharded or single-file storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stackblock](https://clawhub.ai/user/stackblock)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to maintain searchable long-term memory of agent sessions, including messages, tool activity, sub-agent interactions, and system events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill continuously records broad OpenClaw activity, including messages, tool output, and sub-agent interactions.

Mitigation: Install it only when complete conversation memory is intended and avoid using it in sessions that may expose credentials, regulated data, private files, or confidential tool output without clear consent and retention rules.

Risk: Captured logs and Memvid files may persist sensitive information with limited built-in controls.

Mitigation: Store JSONL and .mv2 files in an encrypted private directory, verify file permissions, and review retention or deletion practices before deployment.

Risk: API mode can send captured data to a third-party Memvid service.

Mitigation: Prefer local free or sharded mode for sensitive work and avoid API mode unless remote storage is acceptable.

Risk: The skill invokes the external Memvid CLI while logging.

Mitigation: Pin and review the Memvid CLI before use and keep the configured executable path under user control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stackblock/skills/openclaw-memvid-logger)
- [Memvid documentation](https://memvid.com/docs)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSONL records, Memvid .mv2 files, and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-file or monthly sharded storage modes and can call the Memvid CLI to create and append memory files.]

## Skill Version(s):

1.2.6 (source: ClawHub server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
