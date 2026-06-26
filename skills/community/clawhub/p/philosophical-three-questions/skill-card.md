## Description: <br>
A structured decision framework for embodied navigation that uses Goal Tree, Current State Tree, and Future Tree analysis to guide Habitat-GS navigation decisions, multi-step planning, progress evaluation, and strategy resets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[The0xKa1](https://clawhub.ai/user/The0xKa1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents working on embodied navigation use this skill to structure each Habitat-GS decision around the current goal, observed state, and likely result of available actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead agents to persist episode memories, which may create unwanted logs. <br>
Mitigation: Require user approval before writing memory and avoid storing sensitive environment or task details. <br>
Risk: The skill suggests updating itself or creating new skills after enough navigation experience. <br>
Mitigation: Require explicit review and approval before editing this skill or creating follow-on skills. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/The0xKa1/philosophical-three-questions) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured navigation analysis and memory note templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No tool calls or code generation required; may instruct the agent to write episode memory when allowed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
