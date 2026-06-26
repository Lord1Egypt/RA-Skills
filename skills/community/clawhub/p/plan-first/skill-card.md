## Description: <br>
Solve complex multi-step tasks by generating a detailed plan before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simoncatbot](https://clawhub.ai/user/simoncatbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, analysts, and other agent users use this skill to break complex multi-step tasks into ordered plans with dependencies, verification steps, risk analysis, and rollback guidance before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated plans can include steps that would modify files, databases, accounts, or production systems. <br>
Mitigation: Review the plan before execution and require explicit approval for steps that affect persistent state or production resources. <br>
Risk: Broad activation can add unnecessary planning overhead for simple tasks. <br>
Mitigation: Invoke the skill manually or narrow activation rules if it becomes noisy. <br>


## Reference(s): <br>
- [Plan First detailed examples](references/examples.md) <br>
- [Plan First on ClawHub](https://clawhub.ai/simoncatbot/plan-first) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown plan with ordered steps, dependencies, verification criteria, risk analysis, and rollback guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only planning output; no code execution or external tool invocation is performed by the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
