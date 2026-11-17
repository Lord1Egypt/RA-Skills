## Description:

OpenClaw pre-deployment security checklist for firewall, SSH, API key management, data export compliance, and Mac, VPS, Docker, and enterprise deployment checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiyuanlu](https://clawhub.ai/user/yiyuanlu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, administrators, and security reviewers use this skill to check OpenClaw deployments before launch and to produce a shareable security and compliance report.

### Deployment Geography for Use:

Global, with China-specific compliance guidance for deployments operating in or serving users in China.

## Known Risks and Mitigations:

Risk: Security reports or audit output may include sensitive credentials or credential-like strings.

Mitigation: Review and sanitize reports before sharing them, and avoid running the default audit in directories that may contain live credentials unless that exposure is acceptable.

Risk: Some examples show risky credential handling, including printing API keys, appending keys to shell profiles, and storing Docker image environment values.

Mitigation: Use a secret manager or tightly permissioned environment files, avoid logging secrets, and keep credentials out of Dockerfiles and image layers.

Risk: Operational examples may replace scheduled tasks or modify local security configuration if copied without review.

Mitigation: Treat shell snippets as reviewable guidance, test them in a non-production environment, and preserve existing crontab and configuration before applying changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yiyuanlu/skills/openclaw-security-checklist)
- [README](README.md)
- [Example report](example-report.md)
- [API key management](references/api-key-management.md)
- [China compliance checklist](references/compliance-cn.md)
- [Data export checklist](references/data-border.md)
- [Personal Mac deployment checklist](references/deployment-scenarios/personal-mac.md)
- [VPS deployment checklist](references/deployment-scenarios/vps.md)
- [Docker deployment checklist](references/deployment-scenarios/docker.md)
- [Enterprise deployment checklist](references/deployment-scenarios/enterprise.md)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and generated checklist reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local OpenClaw security report files when the bundled shell scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
