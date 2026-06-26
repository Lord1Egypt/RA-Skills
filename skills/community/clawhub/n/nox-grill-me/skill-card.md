## Description: <br>
Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nox-admin](https://clawhub.ai/user/Nox-admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users use this skill to stress-test a plan, idea, or design through sustained questioning and recommended answers. When a question can be answered from the project, the skill may inspect relevant codebase files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: In private repositories, the skill may read relevant project files while answering design questions. <br>
Mitigation: Limit the agent to specific paths or explicitly ask it not to inspect repository files when sensitive content is out of scope. <br>
Risk: Relentless questioning can surface misleading or overconfident recommendations if the plan context is incomplete. <br>
Mitigation: Review recommendations against project requirements and provide missing constraints before acting on the answers. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Markdown conversational responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include recommended answers to planning or design questions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
