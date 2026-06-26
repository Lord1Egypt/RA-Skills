## Description: <br>
Set up or audit an OpenClaw agent workspace with standardized governance files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[u0003-yxuan](https://clawhub.ai/user/u0003-yxuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up new OpenClaw agent workspaces or audit existing workspaces for required governance, memory, and daily log files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect persistent governance and memory files in an OpenClaw workspace. <br>
Mitigation: Confirm the workspace path before running apply and back up existing AGENTS.md or MEMORY.md files if they matter. <br>
Risk: The artifact references local agent-governance commands and templates that are not bundled with the artifact. <br>
Mitigation: Inspect the local command and template files before applying changes in a workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/u0003-yxuan/openclaw-agent-governance) <br>
- [Publisher profile](https://clawhub.ai/user/u0003-yxuan) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and workspace file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or verify governance files such as MEMORY.md, AGENTS.md, memory/projects.md, memory/lessons.md, and daily log files when applied in a workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, released 2026-03-26) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
