## Description:

macOS-native web dashboard for monitoring and controlling your OpenClaw agent. Live chat, cron management, task workshop, scout engine, cost tracking, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzineldin](https://clawhub.ai/user/jzineldin)

### License/Terms of Use:

BSL 1.1 (converts to MIT 2030)

## Use Case:

Developers and OpenClaw operators use Mission Control to monitor agent activity, manage conversations and scheduled jobs, coordinate task workflows, track usage costs, and adjust agent settings from a local dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup fetches and runs unpinned remote code.

Mitigation: Review the external repository before installing, prefer a pinned release or commit, and use lockfiles with npm ci where available.

Risk: The dashboard uses OpenClaw gateway credentials.

Mitigation: Use a dedicated least-privilege OpenClaw token rather than a primary gateway credential.

Risk: The installation path includes root-level persistent service setup.

Mitigation: Do not enable the system service until the service file is reviewed and confirmed to run as an unprivileged local-only service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jzineldin/skills/openclaw-mission-control)
- [Mission Control GitHub Homepage](https://github.com/Jzineldin/mission-control)
- [Brave Search API](https://brave.com/search/api/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides setup and operation of a local dashboard that uses OpenClaw gateway credentials and optional external service configuration.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
