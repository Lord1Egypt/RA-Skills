## Description:

Safety coach for OpenClaw users that refuses harmful, illegal, or unsafe requests and provides practical guidance to reduce ecosystem risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justindobbs](https://clawhub.ai/user/justindobbs)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw operators and developers use the coach to review security settings, respond safely to risky requests, and harden gateways, messaging, tools, and agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configuration examples may not match the installed OpenClaw version.

Mitigation: Check each example against documentation for your OpenClaw version before applying it.

Risk: Logs or transcripts may expose sensitive information when shared.

Mitigation: Redact credentials and sensitive content before sharing logs or transcripts.

Risk: Conservative refusals may block legitimate requests.

Mitigation: Review the refusal and use the suggested safe alternative where it meets the task need.

## Reference(s):

- [OpenClaw Security Guide](https://docs.openclaw.ai/gateway/security)
- [OpenClaw Security Audit Checks](https://docs.openclaw.ai/gateway/security/audit-checks)
- [OpenClaw Safety Coach on ClawHub](https://clawhub.ai/justindobbs/skills/openclaw-safety-coach)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with prose, CLI commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conversational security coaching with refusals, risk explanations, and safer alternatives.]

## Skill Version(s):

1.0.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
