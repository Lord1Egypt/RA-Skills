## Description: <br>
Aegis Bridge helps agents orchestrate Claude Code sessions through a local Aegis HTTP/MCP bridge for implementation, review, CI repair, batch tasks, and other multi-agent coding workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onestepat4time](https://clawhub.ai/user/onestepat4time) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to spawn, monitor, steer, and clean up local Claude Code sessions for code implementation, review, CI repair, and parallel task execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated Claude Code sessions can receive broad coding and shell authority through the local bridge. <br>
Mitigation: Use project-scoped MCP setup where possible, review permission prompts and bash approvals before approving, and keep session work directories tightly scoped. <br>
Risk: The bundled examples include auto-approval patterns for permission prompts. <br>
Mitigation: Do not use auto-approval loops as-is unless the repository and command set are tightly controlled; change the heartbeat behavior to log or reject untrusted commands. <br>
Risk: Prompts, transcripts, and shared state may expose sensitive project data. <br>
Mitigation: Avoid sending secrets through prompts or transcripts, review shared memory contents, and clean up sessions and shared memory regularly. <br>
Risk: MCP setup can modify user-level or project-level Claude Code configuration. <br>
Mitigation: Prefer project-scoped configuration, inspect configuration changes before applying them, and install only when the local Aegis bridge and npx-resolved package are trusted. <br>


## Reference(s): <br>
- [Aegis API Quick Reference](references/api-quick-ref.md) <br>
- [Agent Template](references/agent-template.md) <br>
- [Heartbeat Template](references/heartbeat-template.md) <br>
- [Workflow Examples](references/workflow-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with HTTP, MCP, JSON, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Aegis server on localhost:9100 and optional MCP configuration.] <br>

## Skill Version(s): <br>
0.6.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
