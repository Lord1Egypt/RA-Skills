## Description:

Provides essential safety rules and tools for managing OpenClaw configs, backups, auth troubleshooting, and recovery to prevent system failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayrizz](https://clawhub.ai/user/jayrizz)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill when changing OpenClaw configuration, troubleshooting authentication failures, creating backups, or recovering from configuration incidents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can copy and modify sensitive OpenClaw authentication files.

Mitigation: Install only after reviewing the scripts, keep verified backups, and run them only on systems where you accept the auth-file impact.

Risk: reset_cooldowns.sh contains unsafe auth-state handling, including a hard-coded auth profile path and cooldown/error-state resets.

Mitigation: Fix the target path and review the intended state changes before use; do not run it as-is on a shared or privileged machine.

Risk: Auth troubleshooting sources ~/.openclaw/.env and writes status output to a fixed /tmp path.

Mitigation: Confirm local environment-file and temporary-file handling are acceptable before running the auth checker.

## Reference(s):

- [Recovery Procedures](references/recovery.md)
- [OpenClaw Sacred Rules on ClawHub](https://clawhub.ai/jayrizz/skills/openclaw-sacred-rules)
- [Publisher Profile: jayrizz](https://clawhub.ai/user/jayrizz)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code, configuration]

**Output Format:** [Markdown guidance with inline shell commands and script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes recovery procedures and helper scripts for backup, configuration validation, cooldown reset, and auth troubleshooting.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
