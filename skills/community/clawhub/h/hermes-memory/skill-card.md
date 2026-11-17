## Description:

Hermes Memory helps agents check local memory-file health, surface cleanup reminders, and keep memory files concise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdvrommel](https://clawhub.ai/user/jdvrommel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to monitor OpenClaw memory, profile, and state files and receive reminders when memory content should be reduced or reorganized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The health check reads sensitive OpenClaw memory, profile, and state files.

Mitigation: Review the script before installing and run it only in workspaces where reading those files is acceptable.

Risk: The script reads all top-level files in ~/self-improving during each check.

Mitigation: Limit the scan to an explicit allowlist of expected memory files before scheduling regular runs.

Risk: The cron example runs automatically on weekdays and uses hard-coded local paths.

Mitigation: Adjust paths for the deployment environment and confirm the schedule before enabling cron.

## Reference(s):

- [Hermes Memory on ClawHub](https://clawhub.ai/jdvrommel/skills/hermes-memory)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text status report with shell command examples and an optional JSON state file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May exit non-zero when cleanup is recommended.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
