## Description:

Automatically redacts API keys, tokens, and secrets from workspace logs and memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heather-herbert](https://clawhub.ai/user/heather-herbert)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to find and redact secrets from OpenClaw workspace logs, memory directories, and MEMORY.md before those files are shared, archived, or used by agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying redaction modifies workspace logs and memory files in place.

Mitigation: Run dry-run first and review the reported file list before running the write mode.

Risk: Backup files can retain the original secrets after redaction.

Mitigation: Remove or protect generated .bak files after confirming the redacted files are usable.

Risk: Recursive file processing can follow symlinks outside the intended workspace.

Mitigation: Run only in trusted workspaces and avoid running where untrusted users or tools can create symlinks under logs or memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/heather-herbert/skills/log-scrubber)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run mode reports affected file paths; apply mode writes redacted files and may create .bak backups containing original content.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
