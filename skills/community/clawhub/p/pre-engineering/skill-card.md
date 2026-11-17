## Description:

PRE Engineering initializes a Plan-Review-Execute multi-agent collaboration workflow by collecting project requirements, generating project coordination documents, and providing startup guidance for Planner, Executor, and Reviewer agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangzhanluo](https://clawhub.ai/user/zhangzhanluo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to set up a structured multi-agent project workflow with requirements, a collaboration log, and role guides for planning, execution, and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated agents are instructed to scan project code and run continuously, which can expose project contents or sustain unintended automation.

Mitigation: Review generated guides before use, confirm which files agents may read, consider provider data-sharing rules, and run the workflow only in an appropriate repository.

Risk: The workflow includes git stash, git add, and commit steps that can affect repository state.

Mitigation: Use a clean branch or disposable repository, constrain broad git commands, and keep .pre and sensitive files ignored as appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangzhanluo/skills/pre-engineering)
- [Planner Agent Guide Document](references/planner-guide-template.md)
- [Executor Agent Guide Document](references/executor-guide-template.md)
- [Reviewer Agent Guide Document](references/reviewer-guide-template.md)
- [Collaboration Log Format Reference](references/collaboration-log-format-reference.md)
- [PRE State System Reference](references/state-system-reference.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown project documents and startup instructions with shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates .pre/ project documents after user confirmation and can adapt the default code directory path in role guide templates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
