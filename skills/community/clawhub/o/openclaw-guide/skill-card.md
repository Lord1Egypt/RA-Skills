## Description:

OpenClaw Guide provides authoritative OpenClaw documentation lookup and guidance about capabilities, configuration, usage, setup, troubleshooting, and related topics using official OpenClaw documentation and source code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linux2010](https://clawhub.ai/user/linux2010)

### License/Terms of Use:


## Use Case:

Developers, operators, and OpenClaw users use this skill to answer questions about OpenClaw features, setup, configuration, architecture, troubleshooting, and best practices using official documentation and source code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses web access to retrieve OpenClaw documentation and source-code information.

Mitigation: Allow network access only to the expected official OpenClaw documentation and repository domains when deploying in a restricted environment.

Risk: The bundled GitHub helper can inherit local GitHub CLI authentication if executed.

Mitigation: Run the helper with a low-privilege or unauthenticated GitHub CLI setup when possible.

## Reference(s):

- [OpenClaw Official Documentation](https://docs.openclaw.ai)
- [OpenClaw Source Repository](https://github.com/openclaw/openclaw)
- [OpenClaw Community](https://discord.com/invite/clawd)
- [OpenClaw Channel Guide](https://docs.openclaw.ai/guides/channels)
- [OpenClaw Skills Guide](https://docs.openclaw.ai/guides/skills)
- [OpenClaw Agents Architecture](https://docs.openclaw.ai/architecture/agents)
- [OpenClaw Common Queries and Solutions](references/common_queries.md)
- [OpenClaw Documentation Structure](references/docs_structure.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown with links and optional inline code or shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should cite official OpenClaw documentation or source code and acknowledge unavailable information.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
