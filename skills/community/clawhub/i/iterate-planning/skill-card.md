## Description: <br>
A requirements iteration workflow for OpenClaw that guides an agent through structured requirements discussion, implementation planning, and single-task iterative execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudyli](https://clawhub.ai/user/cloudyli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product or engineering teams use this skill to turn unclear requirements into topic specs, convert those specs into an implementation plan, and execute the plan one task at a time with validation and commits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The execution template can stage broad repository changes with git add ., which may include unintended files. <br>
Mitigation: Use a clean branch, review diffs before commits, and narrow staged files when generated or unrelated files appear. <br>
Risk: Generated specs or implementation plans may misunderstand requirements and drive incorrect implementation work. <br>
Mitigation: Review and approve specs and IMPLEMENTATION_PLAN.md before beginning iterative execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cloudyli/iterate-planning) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Operator guide](artifact/AGENTS.md) <br>
- [Requirements interview template](artifact/templates/requirements-interview.md) <br>
- [Planning prompt template](artifact/templates/planning-prompt.md) <br>
- [Build prompt template](artifact/templates/build-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with templates, checklists, file paths, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces specs/*.md, IMPLEMENTATION_PLAN.md, repository changes, validation output, and git commits when used for execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
