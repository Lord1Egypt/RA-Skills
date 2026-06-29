## Description: <br>
Converts a specification into a phased, dependency-ordered implementation plan for use after specification is complete and before execution begins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to turn completed specifications into architecture notes, task breakdowns, dependency ordering, acceptance criteria, estimates, and sprint plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move from planning into execution without asking the user first. <br>
Mitigation: Use the standalone option or explicitly ask the agent to stop after planning when only a plan is desired. <br>
Risk: A generated implementation plan may contain incorrect task sequencing, estimates, or dependency assumptions. <br>
Mitigation: Review the architecture, dependencies, acceptance criteria, risks, and sprint allocation before using the plan to guide code changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-attune-project-planning) <br>
- [Attune homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown implementation plan with task breakdowns and planning guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save docs/implementation-plan.md and proceed toward an execution phase unless the user requests standalone planning or stops after planning.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
