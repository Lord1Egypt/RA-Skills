## Description: <br>
Lobster Dev Planner guides software project planning, produces detailed development documentation, and coordinates agent-assisted implementation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and builders use this skill to turn informal software ideas into structured plans, implementation documents, API and style guidance, and coordinated agent tasking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move from planning into broad file, repository, database, deployment, and notification actions. <br>
Mitigation: Use it in a sandbox or clearly scoped repository, connect least-privilege MCP accounts, and prefer development databases. <br>
Risk: Automatic commits, pushes, SQL writes, deployments, shell commands, or external notifications could create unintended changes. <br>
Mitigation: Require explicit approval before those actions and review generated plans and documents before implementation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangxiaofei860208-source/lobster-dev-planner) <br>
- [Plan template](references/plan-template.md) <br>
- [Development document template](references/dev-doc-template.md) <br>
- [API document template](references/api-doc-template.md) <br>
- [Style guide template](references/style-guide-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown plans, documentation templates, implementation task briefs, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May coordinate file, repository, database, deployment, and notification tools when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
