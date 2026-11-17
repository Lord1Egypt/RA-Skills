## Description:

Installs, starts, repairs, and smoke-tests a Windows QQ bridge built with NTQQ, NapCat, WSL, Docker, and OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyspot114514](https://clawhub.ai/user/sunnyspot114514)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical operators use this skill to install or repair a local Windows QQ bot bridge that connects NapCat message events to an OpenClaw agent. It is intended for controlled local automation, health checks, and smoke tests, not official QQ APIs or hosted bot platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports unauthenticated local or network services that can read logs and configuration or send QQ messages.

Mitigation: Use only on a controlled Windows machine, isolate it from untrusted networks, and harden or restrict access to bridge and management endpoints before broader use.

Risk: The skill installs software, starts services, stores QQ chat logs, and can invoke OpenClaw from QQ messages.

Mitigation: Review the generated runtime configuration, token handling, log storage location, and QQ account scope before installation or repair.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunnyspot114514/skills/napcat-qq-bridge-installer)
- [NapCat latest release API](https://api.github.com/repos/NapNeko/NapCatQQ/releases/latest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with PowerShell and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include local configuration values, install or repair actions, health-check results, and smoke-test steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
