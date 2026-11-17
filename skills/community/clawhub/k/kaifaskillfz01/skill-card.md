## Description:

KAIFASKILLFZ01 provides a structured development workflow that routes agent coding work through assessment, planning, user approval, implementation, review, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomm1399](https://clawhub.ai/user/tomm1399)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to manage agent-assisted software development with explicit plans, approval gates, specialized implementation and review roles, and archived plan and review records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quick mode can skip security review while still guiding code changes.

Mitigation: Use standard or strict mode for sensitive work, including authentication, payment, production code, filesystem handling, command execution, or network services, and require security review even for small changes.

## Reference(s):

- [KAIFASKILLFZ01 ClawHub listing](https://clawhub.ai/tomm1399/skills/kaifaskillfz01)
- [Plan output template](references/plan-template.md)
- [Review checklist](references/review-checklist.md)
- [Role prompt templates](references/roles.md)
- [Workflow variants](references/workflow-variants.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown plans and review reports, conversational summaries, code changes, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates plan and review files under a plans directory when the workflow is followed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
