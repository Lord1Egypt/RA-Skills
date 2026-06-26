## Description: <br>
Orchestrate OpenClaw end-to-end R&D delivery in Feishu from requirement intake to closure using PM, developer, reviewer, and tester subagents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinlihudong](https://clawhub.ai/user/yinlihudong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate Feishu-driven R&D tasks from intake through implementation, review, testing, bug rework, and final owner notification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can drive Feishu and repository workflow actions with broad read and write authority. <br>
Mitigation: Use narrowly scoped Feishu spaces, repositories, and task IDs, and require dry runs plus explicit confirmation before Feishu reads, branch pushes, PR creation, or task/status updates. <br>
Risk: Unclear data access and write boundaries can make unattended execution risky. <br>
Mitigation: Do not grant broad credentials or unattended execution until the skill documents its data access and write boundaries clearly. <br>


## Reference(s): <br>
- [OpenClaw RD Pipeline on ClawHub](https://clawhub.ai/yinlihudong/openclaw-rd-pipeline) <br>
- [Feishu Field Mapping](references/feishu-fields.md) <br>
- [Workflow Templates](references/templates.md) <br>
- [Status Validation Script](scripts/validate_status_flow.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, YAML-like structured blocks, shell commands, and workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured requirement, prompt, PR, review, test, status, and notification artifacts for an agent-led workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
