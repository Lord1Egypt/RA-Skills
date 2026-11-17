## Description:

Comprehensive diagnostic, error-fixing, and skill recommendation tool for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phenixstar](https://clawhub.ai/user/phenixstar)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to diagnose OpenClaw issues, inspect logs and configuration, apply guided fixes, run health checks, set up OpenClaw, refresh local references, and find relevant ClawHub skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup and repair flows can expose credentials or weaken host security.

Mitigation: Review before installing; use diagnostic and read-only commands first, and avoid the setup wizard until credential storage and gateway defaults are fixed.

Risk: Some guidance can install mutable software or change host state.

Mitigation: Require explicit approval before package installs, Docker pulls, remote installer scripts, log deletion, or cache updates.

Risk: Docker socket permission changes can weaken host isolation.

Mitigation: Do not follow Docker socket chmod guidance; use safer Docker access controls approved by the deployment owner.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phenixstar/skills/openclaw-doctor-pro)
- [OpenClaw Project](https://github.com/openclaw/openclaw)
- [Error Catalog](references/error-catalog.md)
- [Auto-Fix Capabilities](references/auto-fix-capabilities.md)
- [Diagnostic Commands](references/diagnostic-commands.md)
- [Troubleshooting Workflow](references/troubleshooting-workflow.md)
- [Authentication Errors](references/authentication-errors.md)
- [Rate Limiting Errors](references/rate-limiting-errors.md)
- [Gateway Errors](references/gateway-errors.md)
- [Channel Errors](references/channel-errors.md)
- [Sandbox Errors](references/sandbox-errors.md)
- [Configuration Errors](references/configuration-errors.md)
- [Installation Errors](references/installation-errors.md)
- [ClawHub Integration](references/clawhub-integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, optional JSON from diagnostic tools, and report templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can propose or execute local diagnostic, setup, update, and auto-fix commands; review security guidance before applying changes.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
