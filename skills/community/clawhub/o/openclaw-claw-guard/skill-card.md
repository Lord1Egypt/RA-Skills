## Description:

System-level watchdog for OpenClaw gateway restarts and sub-agent task PIDs that monitors registered PIDs and optional log or directory freshness, auto-reverts config on failed gateway restarts, and requires explicit registration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camopel](https://clawhub.ai/user/camopel)

### License/Terms of Use:


## Use Case:

Developers and operators use ClawGuard to monitor long-running OpenClaw tasks and gateway restarts, receive alerts when registered work stalls or exits, and recover from failed gateway restarts by restoring saved OpenClaw configuration backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an always-on watchdog in the user's session.

Mitigation: Review the generated systemd or launchd service files before enabling the service and keep the disable or unload command available before installation.

Risk: The watchdog can automatically rewrite OpenClaw configuration when recovering from a failed gateway restart.

Mitigation: Review the config backup and rollback behavior before use, and verify restored configuration after any recovery event.

Risk: Alerts may include local service diagnostics sent through OpenClaw notification targets.

Mitigation: Use trusted notification targets and avoid registering tasks where diagnostic excerpts could expose sensitive operational details.

## Reference(s):

- [ClawGuard on ClawHub](https://clawhub.ai/camopel/skills/openclaw-claw-guard)
- [camopel publisher profile](https://clawhub.ai/user/camopel)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and bundled Python and shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an installer, a CLI, and a persistent watchdog service for Linux systemd user services and macOS launchd agents.]

## Skill Version(s):

1.1.0 (source: server release evidence, created 2026-03-02)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
