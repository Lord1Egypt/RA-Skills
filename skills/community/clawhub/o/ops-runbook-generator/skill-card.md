## Description:

Generate operational runbooks by scanning project infrastructure files and producing start, stop, restart, deploy, rollback, troubleshooting, and monitoring procedures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and operations engineers use this skill to generate draft operational runbooks from Docker, Docker Compose, systemd, Makefile, package.json, environment, and nginx configuration files. The generated runbook helps document deployment, lifecycle, health check, rollback, troubleshooting, monitoring, and contact procedures for review and customization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads operational configuration from the target project and generated output may expose sensitive configuration details.

Mitigation: Run it on trusted repositories, replace live .env files with examples before generation, and review Markdown or JSON output for secrets before sharing.

Risk: Generated runbooks can include privileged shell commands such as sudo and systemctl commands, and scanner-derived names may be unsafe to execute blindly.

Mitigation: Treat every shell block as a draft, validate project names and service names, and review privileged commands before use in production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/ops-runbook-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown runbook by default, with optional structured JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May be written to a file with the -o flag; generated commands and configuration findings require human review before operational use.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
