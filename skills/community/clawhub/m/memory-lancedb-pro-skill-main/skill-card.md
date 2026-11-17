## Description:

This skill helps agents install, configure, and use memory-lancedb-pro, a production-grade long-term memory MCP plugin for OpenClaw AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoyang78](https://clawhub.ai/user/chaoyang78)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide OpenClaw memory plugin setup, configuration, verification, and day-to-day memory operations. It is aimed at agents that need operational guidance for Smart Extraction, hybrid retrieval, memory lifecycle management, multi-scope isolation, and self-improvement tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask users to provide API keys during setup.

Mitigation: Use environment variables or a secret manager, avoid pasting API keys into chat, and avoid storing literal keys in openclaw.json.

Risk: The skill includes remote installer and validator steps that should be reviewed before execution.

Mitigation: Review or replace remote setup steps with pinned, verified artifacts before installation.

Risk: Automatic memory capture can store sensitive content while credentials and memory scopes are being configured.

Mitigation: Consider disabling autoCapture until credential handling, memory scopes, and retention behavior are reviewed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/chaoyang78/skills/memory-lancedb-pro-skill-main)
- [Publisher profile](https://clawhub.ai/user/chaoyang78)
- [Full Technical Reference](references/full-reference.md)
- [memory-lancedb-pro setup toolbox](https://github.com/CortexReach/toolbox/tree/main/memory-lancedb-pro-setup)
- [Ollama download](https://ollama.com/download)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include configuration plans, verification steps, MCP tool usage guidance, and troubleshooting instructions.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
