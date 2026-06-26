## Description: <br>
Use when creating OpenClaw agents, configuring workspaces, multi-agent routing, session isolation, or channel bindings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a12591771](https://clawhub.ai/user/a12591771) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create and configure OpenClaw agents, workspace files, routing rules, session isolation, channel bindings, and safety controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated hooks, exec permissions, heartbeat tasks, identity links, channel bindings, or memory and session retention settings could change agent behavior or expose private context if enabled without review. <br>
Mitigation: Review these settings before enabling them, restrict tool permissions and sandbox scope to the intended use case, and validate routing and retention behavior after configuration. <br>
Risk: Workspace Markdown files and configuration examples may include placeholders for credentials or user preferences. <br>
Mitigation: Keep raw secrets out of Markdown workspace files and store credentials in an appropriate secret manager or local environment configuration. <br>


## Reference(s): <br>
- [OpenClaw Docs](https://docs.openclaw.ai/) <br>
- [OpenClaw Agent Runtime](https://docs.openclaw.ai/concepts/agent.md) <br>
- [OpenClaw Skills](https://docs.openclaw.ai/tools/skills.md) <br>
- [OpenClaw Agent Workspace](https://docs.openclaw.ai/concepts/agent-workspace.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON5 configuration examples, Markdown file templates, shell commands, and checklists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose workspace files, agent settings, routing rules, sandbox options, and deployment checks for review before use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
