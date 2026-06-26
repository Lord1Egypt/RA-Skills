## Description: <br>
Build high-performing OpenClaw agents end-to-end by designing personas, operating rules, guardrails, and required workspace files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and advanced OpenClaw users use this skill to create a new agent workspace or improve an existing one with tailored persona files, operating rules, safety boundaries, memory posture, heartbeat behavior, and acceptance tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated agent workspaces can encode autonomy, heartbeat, memory, or tool-use behavior that is broader than intended. <br>
Mitigation: Review AGENTS.md, SOUL.md, HEARTBEAT.md, MEMORY.md, and tool notes before using the generated agent, and only enable heartbeat or high-autonomy behavior after confirming the rules match the user's intent. <br>
Risk: Secrets or credentials could be placed in generated workspace files if the user provides them during customization. <br>
Mitigation: Keep secrets out of the workspace and use the OpenClaw credential locations described in the workspace reference instead. <br>


## Reference(s): <br>
- [OpenClaw Agent Workspace](references/openclaw-workspace.md) <br>
- [OpenClaw Agent File Templates](references/templates.md) <br>
- [Agent Architecture Patterns](references/architecture.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/modestyrichards/modesty-agent-builder) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown file contents, targeted diffs, checklists, and scenario prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce SOUL.md, IDENTITY.md, AGENTS.md, USER.md, HEARTBEAT.md, optional MEMORY.md, optional TOOLS.md, and acceptance-test prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
