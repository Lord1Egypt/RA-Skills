## Description: <br>
Generates structured behavior plans for OpenClaw agents from user requirements for creating plans, designing behavior, or organizing multi-step execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Umfl](https://clawhub.ai/user/Umfl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to turn user goals into OpenClaw-ready execution plans with prerequisites, tool or skill choices, fallback handling, and completion criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated plans can suggest sensitive actions such as shell commands, file writes, secret handling, calendar access, Slack messages, email posts, or other account actions. <br>
Mitigation: Review every generated plan before running it and require explicit user confirmation for sensitive or account-affecting steps. <br>
Risk: A plan may reference unavailable tools, missing permissions, or incorrect dependencies. <br>
Mitigation: Verify required tools, skills, permissions, and input data before executing the planned steps. <br>


## Reference(s): <br>
- [examples.md](artifact/examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/Umfl/openclaw-behavior-plan) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown behavior plan with prerequisites, execution steps, fallbacks, and completion criteria.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask one or two clarification questions for ambiguous requests and should mark sensitive operations as requiring user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
