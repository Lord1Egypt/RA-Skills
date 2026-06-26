## Description: <br>
Generates ranked improvement candidates for a target skill using target analysis, feedback signals, memory inputs, and optional failure traces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to propose structured, ranked changes for skills, especially when retrying after evaluator failures or using memory and feedback to avoid repeated weak proposals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Target skill content and evaluator failure details may be sent to the external Claude CLI when it is available. <br>
Mitigation: Use the skill only where external Claude CLI analysis is acceptable, or run in an environment without the Claude CLI so it falls back to local templates. <br>
Risk: Generated improvement candidates may be incorrect, unsuitable for the target skill, or unsafe to pass directly to an executor. <br>
Mitigation: Inspect generated candidates and execution plans before applying them, especially in environments with private skills, proprietary prompts, or sensitive evaluation traces. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lanyasheng/improvement-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [JSON file with ranked candidate objects and a printed output path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Candidates include category, risk level, rationale, proposed change summary, executor support, and an execution plan.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
