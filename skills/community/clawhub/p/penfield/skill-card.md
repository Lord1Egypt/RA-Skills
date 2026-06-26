## Description: <br>
Persistent memory for OpenClaw agents that stores decisions, preferences, context, artifacts, and graph-linked knowledge across sessions with hybrid BM25, vector, and graph recall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dial481](https://clawhub.ai/user/dial481) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Penfield to give agents persistent memory for preferences, decisions, project context, session checkpoints, files, and connected knowledge graphs across sessions and integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can retain preferences, decisions, project context, checkpoints, and files longer than intended. <br>
Mitigation: Avoid saving secrets, regulated data, confidential files, or personal details unless retention, access, review, and deletion controls are understood. <br>
Risk: Outdated or incorrect stored memories can influence later agent responses. <br>
Mitigation: Use correction and update workflows to revise memories, connect superseding context, and review recalled memories before relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dial481/penfield) <br>
- [openclaw-penfield npm Package](https://www.npmjs.com/package/openclaw-penfield) <br>
- [Penfield MCP Server](https://mcp.penfield.app) <br>
- [Penfield Website](https://penfield.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can invoke Penfield memory, graph, context, artifact, and personality tools when the plugin or MCP server is installed.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
