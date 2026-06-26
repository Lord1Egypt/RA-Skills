## Description: <br>
Unified planning+execution workflow: create a file-based plan with sub-plans, freeze it as FINALIZED, and execute in a separate session with checkpoints and progress/findings logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[double729](https://clawhub.ai/user/double729) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and project maintainers use this skill to plan implementation work, freeze an approved plan, and execute milestones with progress and findings logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates or updates local planning files that may contain sensitive project details if the user records them there. <br>
Mitigation: Review task_plan.md, progress.md, and findings.md before resuming work, and avoid recording secrets in those files. <br>
Risk: Executing from an outdated or unapproved plan can cause work to diverge from the user's intent. <br>
Mitigation: Only proceed after the plan is finalized and the next execution step matches the user's approved scope. <br>


## Reference(s): <br>
- [PlanSuite on ClawHub](https://clawhub.ai/double729/plansuite) <br>
- [double729 ClawHub profile](https://clawhub.ai/user/double729) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown planning files and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates task_plan.md, progress.md, and findings.md in the current project.] <br>

## Skill Version(s): <br>
0.1.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
