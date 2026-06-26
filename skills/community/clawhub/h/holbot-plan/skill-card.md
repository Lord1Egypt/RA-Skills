## Description: <br>
HolBot Plan helps agents create structured plans for multi-step tasks and deepen existing plans through review-oriented sub-agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcbuer](https://clawhub.ai/user/jcbuer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to convert multi-step goals into scoped plans with context, file maps, implementation steps, acceptance criteria, risks, and test scenarios. It also supports deepening an existing plan when more implementation detail is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Planning output could be followed without enough review, leading to incorrect scope, file paths, or test coverage. <br>
Mitigation: Review the generated plan against current project context before execution, including scope, file maps, acceptance criteria, risks, and test scenarios. <br>
Risk: Export requests may save plans outside the intended workspace if the destination is not explicit. <br>
Mitigation: Ask the agent to save under the current workspace or another explicit path before export. <br>
Risk: Broad natural-language routing can invoke planning when brainstorming or deepening would be more appropriate. <br>
Mitigation: Use explicit commands such as /plan, /brainstorm, or 'deepen the plan' to select the intended workflow. <br>


## Reference(s): <br>
- [HolBot Plan on ClawHub](https://clawhub.ai/jcbuer/holbot-plan) <br>
- [Brainstorm Skill](references/brainstorm.md) <br>
- [Deepening Workflow](references/deepening-workflow.md) <br>
- [Plan Sections Reference](references/plan-sections.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown plan with structured sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Plans may include scoped steps, repo-relative file maps, acceptance criteria, risk mitigations, and test scenarios; export should use an explicit destination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
