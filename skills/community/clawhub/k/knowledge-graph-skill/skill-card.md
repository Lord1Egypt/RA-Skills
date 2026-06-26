## Description: <br>
Embedded knowledge graph for AI agents that stores structured knowledge as entities and relations, supports search and traversal, generates KGML summaries, visualizes graph data, and includes an encrypted local vault. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xnohat](https://clawhub.ai/user/xnohat) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to give an AI agent persistent local structured memory for people, projects, decisions, services, knowledge artifacts, and relationships. It is useful when an agent needs to search prior context, maintain a compact session summary, import memory, or manage graph-based notes across OpenClaw, Claude Code, and Gemini CLI workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs an always-on local memory workflow and patches agent instruction files, which can change future agent behavior beyond a single session. <br>
Mitigation: Review the injected agent instruction block before use and keep only the triggers and storage rules that match the workspace policy. <br>
Risk: The graph, summaries, exports, and visualizations can persist personal details, project context, or other sensitive information. <br>
Mitigation: Limit what the agent may store, keep generated data files out of shared repositories, and treat summaries, exports, and visualizations as private data. <br>
Risk: The built-in vault can store credentials, but production secrets remain high-impact if mishandled. <br>
Mitigation: Avoid storing production credentials in the vault and never expose vault values in chat, logs, memory files, exports, or generated summaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xnohat/knowledge-graph-skill) <br>
- [README](README.md) <br>
- [Design document](DESIGN.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands, KGML summaries, JSON graph data, and generated local HTML visualizations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18 or newer and writes local graph, summary, configuration, visualization, and vault files under the skill data directory.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
