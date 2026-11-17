## Description:

Deploy OpenClaw on AWS with a single command that creates an EC2-hosted gateway, Telegram channel access, SSM-only administration, and configurable Bedrock, Gemini, or other model support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godwinbabu](https://clawhub.ai/user/godwinbabu)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to provision, validate, smoke test, and tear down a self-hosted OpenClaw agent on AWS. It is intended for AWS deployments that need no inbound SSH, Telegram-based access, and selectable AI model providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad cloud permissions can create, modify, or delete AWS infrastructure.

Mitigation: Review and narrow the generated IAM policy before use, prefer an assumed role or AWS SSO, and avoid creating IAM user access keys unless there is no safer option.

Risk: Long-lived cloud, Telegram, or model-provider secrets may be exposed through local environment files or generated runtime files.

Mitigation: Use SSM Parameter Store where possible, apply restrictive permissions to generated secret files, rotate credentials after testing, and keep secrets out of source control.

Risk: The deployment installs mutable OpenClaw package code as root during instance bootstrap.

Mitigation: Pin the OpenClaw package version, review the deployment and startup scripts before execution, and rebuild only from trusted package sources.

Risk: Heartbeat behavior may inspect email, calendar, repositories, or memory if enabled by the deployed agent configuration.

Mitigation: Explicitly opt in to each heartbeat integration, scope accessible accounts and repositories, and document what the agent is allowed to check.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/godwinbabu/skills/openclaw-aws-deploy)
- [Troubleshooting Guide](references/TROUBLESHOOTING.md)
- [Gemini OpenClaw Configuration Template](references/config-templates/gemini-flash.json)
- [Gemini Auth Profile Template](references/config-templates/auth-profiles-gemini.json)
- [OpenClaw Systemd Service Template](references/config-templates/openclaw.service.txt)
- [OpenClaw Startup Script Template](references/config-templates/startup.sh)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Telegram BotFather](https://t.me/BotFather)
- [Google AI Studio API Keys](https://aistudio.google.com/apikey)

## Skill Output:

**Output Type(s):** [shell commands, configuration, code, guidance]

**Output Format:** [Markdown with inline bash commands, JSON configuration snippets, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce deployment, teardown, IAM setup, preflight, smoke-test, and troubleshooting steps; execution may create AWS resources and recurring cloud costs.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/CHANGELOG.md, released 2026-02-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
