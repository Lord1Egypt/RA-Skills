## Description: <br>
Memoria adds persistent, local-first memory to OpenClaw agents, with SQLite-backed recall, knowledge graph, procedural learning, continuous capture, and configurable local or remote LLM providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nieto42](https://clawhub.ai/user/nieto42) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Memoria to give agents persistent recall of conversations, tool results, procedures, preferences, and project context across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records conversations and tool output into persistent memory. <br>
Mitigation: Enable it only in workspaces where persistent agent memory is acceptable, and keep generated memory files out of shared repositories. <br>
Risk: Configured remote LLM fallbacks can send conversation data to cloud providers. <br>
Mitigation: Use local providers only for local-only operation, or explicitly review and restrict remote provider configuration and API keys. <br>
Risk: Generated markdown sync files may expose extracted facts if shared. <br>
Mitigation: Review syncMd behavior and inspect generated summaries before committing or publishing workspace files. <br>
Risk: The curl-to-bash installer path can execute remote shell code. <br>
Mitigation: Inspect installer scripts before running them or install manually from reviewed source. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/nieto42/openclaw-memoria) <br>
- [Publisher profile](https://clawhub.ai/user/nieto42) <br>
- [Project homepage](https://github.com/Primo-Studio/openclaw-memoria) <br>
- [Architecture guide](docs/ARCHITECTURE.md) <br>
- [Module guide](docs/MODULES.md) <br>
- [Security policy](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text memory context with optional configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist local SQLite memory and optional markdown summaries in the OpenClaw workspace.] <br>

## Skill Version(s): <br>
3.34.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
