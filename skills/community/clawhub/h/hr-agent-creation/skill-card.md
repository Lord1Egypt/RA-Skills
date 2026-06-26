## Description: <br>
Creates an HR-style OpenClaw agent that helps gather configuration details, create agent workspace files, and bind the agent to a Feishu group chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jingqiu2180](https://clawhub.ai/user/jingqiu2180) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create and configure an HR-style agent that can coordinate agent creation and Feishu group bindings. It is intended for teams that need a repeatable agent workspace setup with guided configuration review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide persistent OpenClaw configuration changes and Feishu group routing updates. <br>
Mitigation: Use interactive mode, review configuration diffs before applying them, keep OpenClaw configuration private, and test first with a non-sensitive Feishu group. <br>
Risk: The generated HR agent is described as having broad agent creation and management powers. <br>
Mitigation: Review and scan generated agent files before deployment, limit tool permissions to the intended workspace, and require human approval for production bindings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jingqiu2180/hr-agent-creation) <br>
- [Quick start guide](examples/quick-start.md) <br>
- [Publisher profile](https://clawhub.ai/user/jingqiu2180) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent OpenClaw workspace and routing configuration guidance that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
