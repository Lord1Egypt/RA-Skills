## Description:

A real-time monitoring dashboard for OpenClaw agents that tracks agents, sub-agents, cron jobs, costs, project progress, memory files, logs, and session replay in a browser UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrpixelraf](https://clawhub.ai/user/mrpixelraf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor local OpenClaw agent activity, costs, cron runs, project state, memory files, logs, and session history from a dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local dashboard exposes sensitive OpenClaw data over an unauthenticated Express server bound to all network interfaces.

Mitigation: Run only on a trusted local machine, avoid exposing port 3721 to LAN, VPN, or container networks, and prefer binding the server to 127.0.0.1 with authentication before using real data.

Risk: Memory files, session replays, logs, and Claude Code usage may contain secrets, private prompts, or operational details.

Mitigation: Treat displayed data as sensitive, restrict browser and network access, and review files before sharing screenshots, logs, or exported dashboard output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mrpixelraf/skills/oc-dashboard)
- [OpenClaw](https://openclaw.ai)
- [OpenClaw Dashboard Demo](https://openclaw-dashboard-demo.vercel.app)
- [Artifact README](README.md)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JavaScript, React, Express, Vite, Tailwind CSS, and package configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installs and runs a local web dashboard that reads OpenClaw files from the user's machine.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
