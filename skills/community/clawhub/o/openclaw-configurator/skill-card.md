## Description:

A smart assistant specialized in helping users configure OpenClaw by clarifying vague requirements through multi-round dialogue and generating AGENTS.md, SOUL.md, IDENTITY.md, USER.md, TOOLS.md, HEARTBEAT.md, MEMORY.md, and the one-time BOOTSTRAP.md ritual.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qomob](https://clawhub.ai/user/qomob)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and OpenClaw users use this skill to gather assistant requirements through dialogue and generate an OpenClaw configuration package for persona, identity, user profile, tools, heartbeat, memory, security, and onboarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing OpenClaw as a persistent background service without enough user-facing safeguards.

Mitigation: Review generated files before use, especially public-channel settings and daemon setup; run the background-service command only after verifying the executable, service account, permissions, logs, and uninstall path.

## Reference(s):

- [OpenClaw Official Site](https://openclaw.ai)
- [OpenClaw Documentation](https://openclaw.ai/docs)
- [OpenClaw Security Guide](https://openclaw.ai/docs/security)
- [OpenClaw CLI Reference](https://openclaw.ai/docs/cli)
- [OpenClaw Configurator on ClawHub](https://clawhub.ai/qomob/skills/openclaw-configurator)
- [Output Schema](schemas/output-schema.json)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance, Shell commands]

**Output Format:** [Markdown configuration package with eight named .md files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files are intended for ~/.openclaw/workspace/ and should conform to schemas/output-schema.json.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter and README report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
