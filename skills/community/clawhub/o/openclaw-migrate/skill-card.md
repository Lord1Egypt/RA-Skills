## Description:

Migrate OpenClaw configuration, skills, memory, tokens, environment variables, and cron jobs to a new host over SSH with setup, test, status, and migration commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris6970barbarian-hue](https://clawhub.ai/user/chris6970barbarian-hue)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to move an OpenClaw installation from one host to another, including local configuration, skills, memory, selected tokens, and scheduled jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The migration copies OpenClaw memory, configuration, API tokens, and scheduled jobs to the destination host.

Mitigation: Install only when the destination host is trusted, review what will be copied, and rotate sensitive tokens where appropriate.

Risk: SSH target inputs and shell-command handling can expose the migration to unsafe command behavior.

Mitigation: Avoid untrusted SSH host, user, or key inputs and prefer versions that use safe argument handling.

Risk: Cron migration can transfer broad scheduled-job state rather than only OpenClaw-specific jobs.

Mitigation: Back up and inspect cron entries before migration, and prefer OpenClaw-specific cron migration instead of replacing the whole crontab.

## Reference(s):

- [Openclaw Migrate ClawHub listing](https://clawhub.ai/chris6970barbarian-hue/skills/openclaw-migrate)
- [Publisher profile](https://clawhub.ai/user/chris6970barbarian-hue)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and CLI workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, SSH connection testing, migration, status checks, and prompts for missing prerequisites.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
