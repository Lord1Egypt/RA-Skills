## Description:

Openclaw Configurator helps users configure OpenClaw by clarifying requirements and generating AGENTS.md, SOUL.md, IDENTITY.md, USER.md, TOOLS.md, HEARTBEAT.md, MEMORY.md, and the one-time BOOTSTRAP.md ritual.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qomob](https://clawhub.ai/user/qomob)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and OpenClaw users use this skill to turn personal assistant requirements into a complete OpenClaw workspace configuration package. It guides users through persona, task, identity, channel, security, and memory choices before producing the required Markdown files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated profile or memory files may contain sensitive personal data if users provide it during configuration.

Mitigation: Review generated files before placing them in ~/.openclaw/workspace and avoid storing secrets in memory or profile files.

Risk: The daemon setup command can keep OpenClaw running in the background.

Mitigation: Run daemon installation only when persistent background operation is intentional.

Risk: Memory directories may expose private data if permissions are too broad.

Mitigation: Use directory-appropriate private permissions such as 700 for memory directories.

## Reference(s):

- [Server-resolved source repository](https://github.com/qomob/OpenclawConfigurator)
- [OpenClaw homepage](https://openclaw.ai)
- [OpenClaw onboarding documentation](https://openclaw.ai/docs/onboarding)
- [OpenClaw agents documentation](https://openclaw.ai/docs/agents)
- [OpenClaw security documentation](https://openclaw.ai/docs/security)
- [OpenClaw CLI documentation](https://openclaw.ai/docs/cli)
- [Output schema](artifact/schemas/output-schema.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown configuration package with eight named .md files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should conform to the bundled OpenClaw configuration package schema.]

## Skill Version(s):

0.1.1 (source: release changelog and server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
