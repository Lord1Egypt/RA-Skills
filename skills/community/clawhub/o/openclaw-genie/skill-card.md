## Description: <br>
Use when the user asks about OpenClaw installation, configuration, agents, channels, memory, tools, hooks, skills, deployment, Docker, multi-agent, OAuth, gateway, CLI, browser, exec, PDF, voice, secrets, sandboxing, sessions, cron, webhooks, heartbeat, sub-agents, nodes, companion devices, canvas, camera, or messaging platform integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fcsouza](https://clawhub.ai/user/fcsouza) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to get OpenClaw setup, configuration, channel integration, memory, tooling, deployment, and multi-agent guidance. It helps agents answer OpenClaw questions with concise explanations, command examples, and configuration snippets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup examples may install packages, fetch remote scripts, or configure long-running services. <br>
Mitigation: Use pinned or verifiable installs, review remote scripts before running them, and avoid unnecessary daemon or system-wide installation. <br>
Risk: Broad channel, browser, memory, broadcast, or PDF capabilities can expose more local or user data than intended. <br>
Mitigation: Grant only the channel and tool scopes needed, review memory indexing behavior, isolate browser profiles, limit broadcasts, and check whether PDFs are sent to remote model providers. <br>


## Reference(s): <br>
- [OpenClaw Configuration Reference](references/configuration.md) <br>
- [OpenClaw Channels Reference](references/channels.md) <br>
- [OpenClaw Memory System Reference](references/memory.md) <br>
- [OpenClaw Tools Reference](references/tools.md) <br>
- [OpenClaw Deployment Reference](references/deployment.md) <br>
- [OpenClaw Multi-Agent Reference](references/multi-agent.md) <br>
- [OpenClaw Docs](https://docs.openclaw.ai) <br>
- [OpenClaw Website](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline command and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenClaw CLI commands, JSON configuration snippets, setup steps, and operational cautions.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
