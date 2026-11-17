## Description:

计划架构师 converts design documents into executable implementation plans with 2-5 minute tasks, TDD steps, precise file paths, validation commands, and execution checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to turn approved designs, feature requests, bug reports, refactoring goals, and migration work into detailed implementation plans that can be executed and verified task by task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated plans may include shell commands, package installs, or file changes that affect the project.

Mitigation: Review each command and file edit before execution, run work in a sandbox or branch, and keep rollback steps available.

Risk: Plans may mention callback URLs, API keys, or network/service setup.

Mitigation: Do not provide credentials or enable network flows until the service, scope, and data path are explicit and approved.

Risk: Detailed implementation plans can be incorrect or overconfident when the source design is incomplete.

Mitigation: Validate assumptions against the actual repository, run the proposed tests, and require human review before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown plans with inline code snippets, shell commands, file paths, validation steps, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans may include task dependencies, time estimates, rollback steps, and TDD red-green-refactor sequencing.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
