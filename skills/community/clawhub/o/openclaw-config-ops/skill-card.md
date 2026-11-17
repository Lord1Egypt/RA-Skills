## Description:

Safe OpenClaw gateway configuration operations. Use when reading, analyzing, or modifying openclaw.json. Enforces schema validation + official documentation verification before every change.

This skill is ready for commercial/non-commercial use.

## Publisher:

[astralwaveorg](https://clawhub.ai/user/astralwaveorg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect, troubleshoot, and safely modify OpenClaw gateway configuration in openclaw.json with schema checks, documentation verification, backups, validation, and change logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required plaintext change log can preserve sensitive configuration values such as credentials.

Mitigation: Review the skill before installing when OpenClaw config contains secrets, and redact sensitive values or avoid recording raw values in the change log.

## Reference(s):

- [OpenClaw Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference)
- [OpenClaw Configuration Examples](https://docs.openclaw.ai/gateway/configuration-examples)
- [OpenClaw Models](https://docs.openclaw.ai/models/)
- [OpenClaw Plugins](https://docs.openclaw.ai/plugins/)
- [OpenClaw Channels](https://docs.openclaw.ai/channels/)
- [OpenClaw Tools](https://docs.openclaw.ai/tools/)
- [OpenClaw MCP](https://docs.openclaw.ai/tools/mcp)
- [OpenClaw CLI](https://docs.openclaw.ai/cli/)
- [OpenClaw Security](https://docs.openclaw.ai/gateway/security)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include schema evidence, documentation evidence, change proposals, verification results, and change-log entries.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
