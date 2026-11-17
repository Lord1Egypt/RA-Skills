## Description:

Practitioner cookbook for testing and monitoring agent commerce: tool contract tests, workflow saga tests, chaos injection, OpenTelemetry tracing, health checks, alerting, and CI/CD pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this guide to design tests, observability, alerting, chaos exercises, and CI/CD checks for agent commerce systems that interact with GreenHelix-style escrow, payment, and trust workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples handle API keys and payment actions and may be copied into real environments.

Mitigation: Pass secrets through environment variables, review copied templates before use, and avoid inline credentials in source or CI configuration.

Risk: Configurable endpoints and session-wide bearer headers can expose credentials if pointed at untrusted origins.

Mitigation: Restrict base URLs to trusted GreenHelix hosts and avoid reusing bearer-authenticated sessions across configurable origins.

Risk: Tracing and transaction capture can expose raw payment or request details.

Mitigation: Redact or disable raw transaction input capture in production traces.

Risk: Reusable examples may depend on unpinned packages or patterns that drift over time.

Mitigation: Pin dependencies and run review, security scanning, and sandbox tests before production use.

## Reference(s):

- [GreenHelix API Documentation](https://api.greenhelix.net/docs)
- [GreenHelix Sandbox](https://sandbox.greenhelix.net)
- [ClawHub Skill Release](https://clawhub.ai/mirni/skills/greenhelix-agent-testing-observability)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guide with Python examples, shell commands, CI configuration, and observability templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executing educational guide; referenced credentials are supplied by the user environment.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
