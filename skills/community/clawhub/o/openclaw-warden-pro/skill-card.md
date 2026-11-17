## Description:

Full workspace security suite: detect unauthorized modifications, scan for prompt injection patterns, and automatically respond with countermeasures - snapshot restore, skill quarantine, git rollback, and automated protection sweeps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaspa](https://clawhub.ai/user/atlaspa)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent-workspace operators use this skill to check local workspace files for integrity changes and prompt-injection patterns, then run remediation commands such as snapshot restore, git rollback, and skill quarantine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated remediation can overwrite monitored instruction or configuration files.

Mitigation: Run baseline, full, restore, and protect commands only after reviewing the target workspace path and keeping independent backups of critical files.

Risk: Skill quarantine disables skills by renaming their directories.

Mitigation: Review scan results before quarantine actions and verify quarantined skills before using unquarantine.

Risk: Startup hooks or heartbeat automation can run destructive remediation without an interactive review step.

Mitigation: Keep startup automation disabled until restore paths are confined, symlinks are rejected, and destructive actions require explicit approval.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/atlaspa/skills/openclaw-warden-pro)
- [Publisher profile](https://clawhub.ai/user/atlaspa)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [OpenClaw Warden](https://github.com/AtlasPA/openclaw-warden)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs local command guidance for a Python standard-library tool; commands may modify monitored workspace files or rename skill directories when remediation is enabled.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
