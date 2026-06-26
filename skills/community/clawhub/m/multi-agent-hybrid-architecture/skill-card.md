## Description: <br>
OpenClaw 多 Agent 协作架构 - 混合层级 + 物理隔离 + 逻辑隔离的完美组合 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zoopools](https://clawhub.ai/user/Zoopools) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and agent builders use this skill to route tasks between coordinator and media agents, define role boundaries, and apply SOUL.md templates for multi-agent collaboration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The media agent is granted broad baoyu-* tool and public-posting authority. <br>
Mitigation: Narrow the media agent's permissions to the tools needed for the deployment and require explicit confirmation before any public post. <br>
Risk: Persistent memory duties could retain sensitive task details without clear deletion rules. <br>
Mitigation: Define what may be written to memory files, exclude sensitive information, and document how records can be deleted. <br>
Risk: Applying SOUL.md templates can overwrite existing local agent behavior. <br>
Mitigation: Back up and diff existing SOUL.md files before installing or merging the templates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zoopools/multi-agent-hybrid-architecture) <br>
- [Publisher profile](https://clawhub.ai/user/Zoopools) <br>
- [Architecture guide](docs/architecture.md) <br>
- [Task flow guide](docs/task-flow.md) <br>
- [Troubleshooting guide](docs/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces role-routing guidance, SOUL.md templates, and configuration-check instructions for an OpenClaw multi-agent setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
