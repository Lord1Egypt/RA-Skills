## Description: <br>
Provides an offline OpenClaw reference for agents answering configuration, setup, troubleshooting, CLI, channel, provider, security, installation, and platform questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxwellmelo](https://clawhub.ai/user/maxwellmelo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and engineers use this skill to answer OpenClaw operational questions, draft configuration, troubleshoot gateway, channel, provider, and platform issues, and locate relevant reference sections without live documentation lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is documentation-only but includes copy-paste commands and operational OpenClaw guidance. <br>
Mitigation: Review suggested commands before execution, especially remote installers, cleanup commands, workspace or memory publishing, and shell pipelines. <br>
Risk: The guide discusses provider keys, voice data, remote code execution, gateway tokens, OAuth tokens, wallets, and other sensitive credentials. <br>
Mitigation: Treat credentials and tokens as sensitive, prefer token files or secret references where available, and avoid exposing workspace, memory, or diagnostic files without inspection. <br>


## Reference(s): <br>
- [OpenClaw Expert Guide on ClawHub](https://clawhub.ai/maxwellmelo/openclaw-expert-guide) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [OpenClaw GitHub Repository](https://github.com/openclaw/openclaw) <br>
- [OpenClaw Core Concepts Reference](references/01-core-concepts.md) <br>
- [OpenClaw Gateway Reference](references/02-gateway.md) <br>
- [OpenClaw CLI Reference](references/03-cli.md) <br>
- [OpenClaw Channels Reference](references/04-channels.md) <br>
- [OpenClaw Providers Reference](references/05-providers.md) <br>
- [OpenClaw Tools Reference](references/06-tools.md) <br>
- [OpenClaw Plugins Reference](references/07-plugins.md) <br>
- [OpenClaw Automation Reference](references/08-automation.md) <br>
- [OpenClaw Installation Reference](references/09-installation.md) <br>
- [OpenClaw Security and Miscellaneous Reference](references/10-security-and-misc.md) <br>
- [OpenClaw Platforms Reference](references/11-platforms.md) <br>
- [OpenClaw Full Reference](references/12-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Suggested commands and configuration snippets should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
