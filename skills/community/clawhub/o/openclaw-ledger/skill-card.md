## Description:

Openclaw Ledger records local workspace changes in a hash-chained ledger and provides commands to initialize, record, verify, inspect, export, and restore ledger data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaspa](https://clawhub.ai/user/atlaspa)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to keep a local audit ledger for workspace changes during agent sessions and to check whether the recorded ledger chain remains intact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: .ledger can store file names, hashes, timestamps, and user-supplied messages that may disclose workspace activity.

Mitigation: Keep ledger data local, review export output before sharing it, and avoid export commands unless full ledger disclosure is intended.

Risk: The ledger is tamper-evident, not forensic-grade tamper-proofing against a user or process that can write to the workspace.

Mitigation: Do not use it as the sole security control; pair it with workspace access controls or external backups when stronger assurance is required.

Risk: Protect and restore operations can replace ledger data.

Mitigation: Run those commands only when ledger replacement is intended and retain backups before recovery operations.

## Reference(s):

- [Openclaw Ledger on ClawHub](https://clawhub.ai/atlaspa/skills/openclaw-ledger)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local ledger files under .ledger and may print JSON or text reports for export operations.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
