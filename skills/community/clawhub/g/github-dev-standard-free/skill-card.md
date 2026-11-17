## Description: <br>
Guides individual developers through a structured project development workflow with a 9-step process and a basic acceptance checklist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual builders use this skill to plan fixes or feature work, keep changes scoped, run local checks, review diffs, and prepare release notes before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Command examples may run local development, Git, or GitHub-related actions when an agent applies the workflow. <br>
Mitigation: Review each proposed command before execution and limit it to the current task and repository. <br>
Risk: Generic create, query, modify, or delete wording could be over-read as permission for unrelated actions. <br>
Mitigation: Keep use scoped to the structured development workflow and reject unrelated operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/github-dev-standard-free) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code] <br>
**Output Format:** [Markdown guidance with checklist items and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes task-card templates, validation checklists, and command examples for local development checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
