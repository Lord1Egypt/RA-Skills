## Description:

Helps keep the OpenClaw gateway running persistently on Windows, Linux, and macOS with service setup, monitoring, restart, sleep-prevention, and troubleshooting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgy2020](https://clawhub.ai/user/lgy2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when they need an OpenClaw gateway to survive reboot, terminal closure, sleep, crashes, or network interruptions on a workstation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent power and startup changes can alter host-wide behavior, especially on shared, managed, or battery-powered machines.

Mitigation: Install only when the machine is intended to act as an always-on OpenClaw gateway, and avoid disabling sleep or hibernation unless the user knows how to restore the prior settings.

Risk: Startup tasks or external process supervisors may run with broader privileges than necessary or call an unexpected executable.

Mitigation: Prefer the built-in OpenClaw service command first, avoid highest-privilege startup tasks unless required, and use absolute executable paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lgy2020/skills/keepalive)
- [ClawHub publisher profile](https://clawhub.ai/user/lgy2020)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, PowerShell, and cmd code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OS-specific service setup, power-management, supervisor, troubleshooting, and healthcheck examples.]

## Skill Version(s):

1.0.0 (source: server evidence release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
