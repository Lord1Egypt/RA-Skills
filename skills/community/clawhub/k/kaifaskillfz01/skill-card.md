## Description: <br>
Guides development requests through a structured Plan, approval, Implement, Review, and Report workflow with role-based agent handoffs and archived plan and review files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomm1399](https://clawhub.ai/user/tomm1399) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to manage larger development work with an explicit plan, approval gate, implementation phase, review phase, and final report. It is intended for tasks that benefit from structured planning and review rather than small edits or simple configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create plan and review files and use subagents for development work. <br>
Mitigation: For advice-only requests, explicitly tell the agent not to save plan or review files or start implementation. <br>
Risk: Security-sensitive, payment, authentication, production, or large changes need deeper review than the default workflow may provide. <br>
Mitigation: Request strict mode so planning and review use the skill's more rigorous path before implementation is accepted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tomm1399/kaifaskillfz01) <br>
- [Plan template](references/plan-template.md) <br>
- [Review checklist](references/review-checklist.md) <br>
- [Role prompt templates](references/roles.md) <br>
- [Workflow variants](references/workflow-variants.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Files, Code, Shell commands] <br>
**Output Format:** [Markdown guidance and archived plan/review files, with code or shell commands when implementation tasks require them.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create plan and review files under plans/ and may delegate implementation or review work to role-specific subagents.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
