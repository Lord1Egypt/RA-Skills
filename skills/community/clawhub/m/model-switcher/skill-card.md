## Description: <br>
Automatically switch between fast and powerful models based on task complexity, including analysis, refactoring, architecture design, optimization, or explicit model-switching requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PUASERVICE](https://clawhub.ai/user/PUASERVICE) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agent users and developers use this skill to route simple tasks to a faster model and complex tasks to a more capable model during a conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may change models during a conversation when the switching rules are triggered. <br>
Mitigation: Install only when model switching is desired and review the configured model aliases before use, especially before sharing sensitive data. <br>
Risk: The documented switching rules work best for the listed Chinese keywords and may miss or over-classify other requests. <br>
Mitigation: Review task routing decisions for important work and adjust the keyword guidance for the deployment context. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Markdown guidance with inline tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no code, persistence, credential access, or data collection was reported by server security evidence.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
