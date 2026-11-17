## Description:

Harden an OpenClaw Linux server with SSH key-only authentication, UFW firewall rules, fail2ban brute-force protection, and credential permission checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppiankov](https://clawhub.ai/user/ppiankov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when setting up, auditing, or recovering an OpenClaw Linux server that needs baseline host-hardening steps. It provides command-oriented guidance for SSH configuration, firewall defaults, fail2ban setup, credential permissions, and an optional gateway service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Administrative hardening commands can lock out server access or disrupt network connectivity if applied without preparation.

Mitigation: Confirm working SSH key-based access, review each command, and approve each administrative section before execution.

Risk: The optional OpenClaw gateway service is persistent and runs as root.

Mitigation: Enable it only when needed, review the executable path and configuration, and add least-privilege systemd hardening before production use.

Risk: The optional validator install command may execute third-party tooling.

Mitigation: Run validation as an unprivileged user and pin or review the tool before executing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ppiankov/skills/host-hardening)
- [Publisher profile](https://clawhub.ai/user/ppiankov)
- [Agent-Native CLI Convention](https://ancc.dev)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before administrative commands are run.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
