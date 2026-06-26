## Description: <br>
Complete guide to using and extending Hermes Agent -- CLI usage, setup, configuration, spawning additional agents, gateway platforms, skills, voice, tools, profiles, and a concise contributor reference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oicqren](https://clawhub.ai/user/oicqren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and external users use this skill to configure, troubleshoot, operate, and extend Hermes Agent across CLI, gateway, profile, tool, skill, memory, voice, and multi-agent workflows. It is also useful for contributors who need concise reference material for Hermes commands, configuration paths, and extension patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The quick-start installer runs a remote shell script and can change the user's local environment. <br>
Mitigation: Review or pin the installer source before running it, and install only in an environment where Hermes Agent is intended to be used. <br>
Risk: Approval-bypass modes, spawned agents, gateways, cron jobs, tools, and memory can operate with broad access if configured too permissively. <br>
Mitigation: Keep credentials, gateway platforms, memory backends, scheduled jobs, and spawned agents scoped to trusted environments, and avoid approval-bypass modes on important systems. <br>
Risk: The skill references many credential environment variables and OAuth flows for model providers, voice services, and integrations. <br>
Mitigation: Store secrets only in the intended Hermes configuration or environment files and limit provider keys to the minimum privileges needed. <br>


## Reference(s): <br>
- [Hermes Agent ClawHub page](https://clawhub.ai/oicqren/hermes-agent-yuhu) <br>
- [Hermes Agent GitHub repository](https://github.com/NousResearch/hermes-agent) <br>
- [Hermes Agent documentation](https://hermes-agent.nousresearch.com/docs/) <br>
- [Configuration guide](https://hermes-agent.nousresearch.com/docs/user-guide/configuration) <br>
- [Provider integrations](https://hermes-agent.nousresearch.com/docs/integrations/providers) <br>
- [Messaging platforms](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/) <br>
- [Tools reference](https://hermes-agent.nousresearch.com/docs/reference/tools-reference) <br>
- [Slash commands reference](https://hermes-agent.nousresearch.com/docs/reference/slash-commands) <br>
- [Skills catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog) <br>
- [MCP feature guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp) <br>
- [Profiles guide](https://hermes-agent.nousresearch.com/docs/user-guide/profiles) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, configuration snippets, tables, and contributor reference notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are operational guidance for Hermes Agent and may include commands that install software, configure credentials, start gateways, spawn agents, or edit local configuration.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
