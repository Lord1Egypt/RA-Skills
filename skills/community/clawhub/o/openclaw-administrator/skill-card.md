## Description: <br>
OpenClaw Admin helps agents operate, configure, and troubleshoot the OpenClaw CLI across setup, gateways, agents, routing, providers, HTTP APIs, security checks, backups, and diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[encryptshawn](https://clawhub.ai/user/encryptshawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to administer OpenClaw installations, configure agents and model providers, diagnose gateway or channel failures, and apply security-conscious configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides OpenClaw administration tasks that may involve gateway tokens, provider keys, OAuth credentials, and other sensitive configuration. <br>
Mitigation: Keep the gateway endpoint private, store tokens through environment variables or SecretRefs, and require explicit authorization before configuration changes. <br>
Risk: Optional cross-agent session search can allow one agent to search another agent's transcripts. <br>
Mitigation: Enable cross-agent session search only when everyone affected understands and accepts the transcript access model. <br>
Risk: Incorrect configuration guidance could disrupt gateway, agent, routing, provider, or channel behavior. <br>
Mitigation: Prefer non-destructive diagnostics first, validate JSON syntax, run OpenClaw health checks, and keep verified backups before risky operations. <br>


## Reference(s): <br>
- [OpenClaw Admin on ClawHub](https://clawhub.ai/encryptshawn/openclaw-administrator) <br>
- [OpenClaw CLI Docs](https://docs.openclaw.ai/cli) <br>
- [Command Map](references/command-map.md) <br>
- [Models and Providers](references/models-and-providers.md) <br>
- [Multi-Agent Recipes](references/multi-agent-recipes.md) <br>
- [OpenAI-Compatible HTTP API](references/openai-http-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenClaw CLI commands, JSON configuration examples, and diagnostic sequences.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
