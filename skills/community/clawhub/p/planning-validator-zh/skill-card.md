## Description: <br>
计划验证器在执行前检查代理计划的基本结构、工具字段和可行性假设，以减少由不受支持或未经验证的计划步骤造成的失败。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill as a lightweight pre-execution checklist for multi-step agent plans, especially to confirm required plan fields, referenced tools, permissions, dependencies, and user clarification points before acting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be mistaken for a complete safety gate even though the release security summary says it is much weaker than its description suggests. <br>
Mitigation: Use it only as a lightweight checklist and independently verify tools, permissions, credentials, dependencies, and execution risks before acting. <br>
Risk: The bundled validator checks only basic plan fields and whether each step declares a tool, so unsafe or infeasible plans can still pass. <br>
Mitigation: Require human review and explicit approval for complex or high-impact plans, and add project-specific validation for real tool availability and constraints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/planning-validator-zh) <br>
- [Publisher profile](https://clawhub.ai/user/kofna3369) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown guidance with Python examples and command-line validation output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
