## Description: <br>
Loop Stability Check provides a structured protocol for detecting workflow loops, drift, retry waste, and missing feedback, then recommending guardrails or a halt condition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarkchenkai](https://clawhub.ai/user/clarkchenkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and workflow owners use this skill to diagnose stuck or unstable agent and human-bot workflows, classify the failure mode, and choose a small guardrail or halt condition that restores convergence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be invoked implicitly and may impose its loop-analysis format when the agent judges that a task is not converging. <br>
Mitigation: Review its recommendations before applying them to important workflows, especially when creative exploration or open-ended iteration is intended. <br>


## Reference(s): <br>
- [Failure Modes](references/failure-modes.md) <br>
- [Guardrails](references/guardrails.md) <br>
- [Wiener Reference](references/wiener.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/clarkchenkai/loop-stability-check-clarkchenkai) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/clarkchenkai) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown with six labeled sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The response contract ends with Loop Objective, Observed Behavior, Stability Risks, Likely Failure Mode, Guardrails, and Recommended Intervention.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
