## Description:

Provides enterprise-oriented security configuration, OpenClaw permission checks, token-usage monitoring, and compliance reporting guidance for OpenClaw deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2389275723](https://clawhub.ai/user/2389275723)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, security engineers, and OpenClaw administrators use this skill to inspect OpenClaw security posture, monitor token usage, and generate remediation-oriented compliance reports for enterprise or financial-industry deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent monitoring and optional system-wide service setup can run with elevated privileges.

Mitigation: Prefer a least-privilege user service, avoid running the monitor as root, and review service files before enabling them.

Risk: Reports and log output may include credential fragments, token usage, or raw OpenClaw log lines.

Mitigation: Store generated reports and logs with restricted permissions and review them before sharing outside the operating team.

Risk: Manual wget/tar installation depends on the downloaded release being authentic.

Mitigation: Prefer the ClawHub install path or verify downloaded release hashes before manual installation.

Risk: Webhook alerts can send token-usage details to an external endpoint.

Mitigation: Use only trusted webhook destinations, protect webhook secrets, and keep the default log-only mode unless external alerting is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2389275723/skills/openclaw-security-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/2389275723)
- [Artifact README](artifact/README.md)
- [Artifact installation guide](artifact/INSTALL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and generated text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-stream agent guidance; executing the bundled scripts may create local configuration files, logs, PID files, and text reports.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact package metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
