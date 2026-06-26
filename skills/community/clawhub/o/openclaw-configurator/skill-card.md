## Description: <br>
A smart assistant specialized in helping users configure OpenClaw by clarifying vague requirements through multi-round dialogue and generating AGENTS.md, SOUL.md, IDENTITY.md, USER.md, TOOLS.md, HEARTBEAT.md, MEMORY.md, and the one-time BOOTSTRAP.md ritual. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qomob](https://clawhub.ai/user/qomob) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to turn assistant requirements into a reviewed Markdown configuration package for persona, memory, tools, security, and onboarding setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated OpenClaw files can shape future assistant behavior, including memory rules, public-channel access, and daemon operation. <br>
Mitigation: Review AGENTS.md, MEMORY.md, public-channel access settings, and daemon instructions before placing generated files in the workspace. <br>
Risk: Sensitive plaintext in generated workspace files could expose passwords, API keys, account numbers, or other private data. <br>
Mitigation: Do not place secrets or account identifiers in generated Markdown; use environment variables or a secrets manager instead. <br>
Risk: Open public-channel settings can expose the assistant to unknown senders. <br>
Mitigation: Use pairing or allowFrom restrictions for Discord, WhatsApp, Telegram, and other public or semi-public channels. <br>


## Reference(s): <br>
- [OpenClaw Official Site](https://openclaw.ai) <br>
- [OpenClaw Documentation](https://openclaw.ai/docs) <br>
- [OpenClaw Security Guide](https://openclaw.ai/docs/security) <br>
- [OpenClaw CLI Reference](https://openclaw.ai/docs/cli) <br>
- [OpenClaw Configurator ClawHub Listing](https://clawhub.ai/qomob/openclaw-configurator) <br>
- [Output Schema](schemas/output-schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown configuration package with named .md files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files are intended for ~/.openclaw/workspace/ and should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
