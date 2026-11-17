## Description:

Provides a web interface to monitor OpenClaw nodes, manage agent configurations, oversee resource usage, security policies, and review system logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wufan2026](https://clawhub.ai/user/wufan2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to administer OpenClaw Gateway deployments through a dashboard for nodes, agents, sessions, models, channels, skills, logs, and resource monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard exposes high-impact host control and administrative features.

Mitigation: Install only in a tightly controlled local or isolated environment, avoid exposing the backend port to a network, and avoid running it as root or administrator.

Risk: Weak authentication defaults could leave the admin interface exposed.

Mitigation: Set strong AUTH_USERNAME and AUTH_PASSWORD before starting the backend.

Risk: Backups may contain secrets, including environment configuration.

Mitigation: Treat backups as secret-bearing artifacts and restrict their storage, download, upload, and restore paths to trusted administrators.

Risk: The security scan flags npm update handling, file API scoping, media authentication, token storage, and archive dependencies as areas needing review.

Mitigation: Review and fix these areas before production use.

## Reference(s):

- [OpenClaw Admin Main on ClawHub](https://clawhub.ai/wufan2026/skills/openclaw-admin-main)
- [OpenClaw Gateway releases](https://github.com/openclaw/openclaw/releases)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and configuration-oriented guidance with code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes administrative setup, troubleshooting, and operational guidance for an OpenClaw web dashboard.]

## Skill Version(s):

0.2.8 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
