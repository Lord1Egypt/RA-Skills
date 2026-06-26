## Description: <br>
Validates agent plans before execution to prevent hallucinated planning failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill as a planning checklist to review plan structure, tool assumptions, permissions, dependencies, feasibility, and clarification needs before executing multi-step agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents itself as a safety validator, but server security evidence says it can approve plans without actually validating them. <br>
Mitigation: Treat it as a prototype or checklist and require independent validation of tools, permissions, dependencies, constraints, and missing assumptions before execution. <br>
Risk: Important or risky plans may be acted on after incomplete validation. <br>
Mitigation: Use a fail-closed process: pause execution when validation is incomplete and ask for clarification before proceeding. <br>


## Reference(s): <br>
- [Planning Validator release page](https://clawhub.ai/kofna3369/planning-validator) <br>
- [kofna3369 publisher profile](https://clawhub.ai/user/kofna3369) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python examples and optional command-line validation output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces checklist-style guidance and simple validation results; server security evidence says it should be treated as a prototype rather than a complete execution gate.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
