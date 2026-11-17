## Description:

Unified planning+execution workflow: create a file-based plan with sub-plans, freeze it as FINALIZED, and execute in a separate session with checkpoints and progress/findings logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[double729](https://clawhub.ai/user/double729)

### License/Terms of Use:


## Use Case:

Developers and agents use PlanSuite to create file-based project plans with milestones, freeze an approved plan, and track execution through progress and findings logs. It is suited for controlled implementation work that needs checkpoints and change control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or update task_plan.md, progress.md, and findings.md in the current project directory.

Mitigation: Direct the agent to use a dedicated folder or alternate file names when project-root tracking files are not desired.

Risk: Planning guidance can become stale or incorrect if execution uncovers new constraints.

Mitigation: Use the documented change-control flow: record findings, return the plan to DRAFT, and wait for renewed user confirmation before continuing.

Risk: The bundled templates contain Chinese headings, which may not fit every team workflow.

Mitigation: Ask the agent to translate or adapt the templates before initializing project files.

## Reference(s):

- [PlanSuite ClawHub skill page](https://clawhub.ai/double729/skills/plansuite)
- [Publisher profile: double729](https://clawhub.ai/user/double729)
- [Task plan template](artifact/templates/task_plan.md)
- [Progress template](artifact/templates/progress.md)
- [Findings template](artifact/templates/findings.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files]

**Output Format:** [Markdown planning files and concise conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates task_plan.md, progress.md, and findings.md in the working directory unless the agent is directed to use another location.]

## Skill Version(s):

0.1.3 (source: server release metadata; artifact _meta.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
