## Description:

MoltGuard is an OpenClaw security guard that helps protect agents and users from prompt injection, data exfiltration, credential theft, command injection, and malicious commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaslwang](https://clawhub.ai/user/thomaslwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install and operate MoltGuard security guardrails for detecting prompt injection, data exfiltration, credential exposure, command injection, and other risky agent behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security verdict is suspicious because setup and credential handling are broad enough to require review before installation.

Mitigation: Install only with explicit human approval after confirming the publisher handle, ClawHub skill page, version 6.8.16, and license evidence.

Risk: Security-relevant content may be processed by Core during detection.

Mitigation: Review data-handling expectations before use, especially for sensitive files, PII, credentials, or enterprise environments.

Risk: The skill can display API keys and agent-claiming credentials through its status and claim flows.

Mitigation: Avoid displaying or sharing API keys unless rotation is understood and available; rotate credentials after accidental exposure.

## Reference(s):

- [MoltGuard ClawHub skill page](https://clawhub.ai/thomaslwang/skills/moltguard)
- [MoltGuard homepage](https://github.com/openguardrails/openguardrails/tree/main/moltguard)
- [Publisher profile](https://clawhub.ai/user/thomaslwang)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and OpenClaw slash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation, status, dashboard, account-claiming, enterprise enrollment, update, and uninstall guidance.]

## Skill Version(s):

6.8.16 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
