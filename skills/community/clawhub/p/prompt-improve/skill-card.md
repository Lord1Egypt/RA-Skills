## Description: <br>
Converts vague user requests into structured, actionable prompts using a four-part framework without executing the requested task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flonerze](https://clawhub.ai/user/flonerze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn underspecified or mixed-language requests into complete prompt text with role, task, context, and constraints. It is intended for prompt refinement only, not for carrying out the refined task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad routing language may cause the skill to activate when a user expects the agent to answer or execute a task directly. <br>
Mitigation: Enable it only for prompt-rewriting workflows, and disable or avoid it in conversations where direct execution is desired. <br>
Risk: Generated prompts can carry incorrect assumptions from ambiguous input. <br>
Mitigation: Review the generated prompt before using it for downstream work, especially when requirements, constraints, or success criteria matter. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flonerze/prompt-improve) <br>
- [Publisher profile](https://clawhub.ai/user/flonerze) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown prompt text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates prompt text only; does not inspect files, call tools, or execute the requested task.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
