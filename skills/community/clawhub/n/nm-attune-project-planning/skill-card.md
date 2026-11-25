## Description:

Converts a specification into a phased, dependency-ordered implementation plan. Use after specification is complete and before execution begins

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill after requirements are specified to organize architecture decisions and work into dependency-ordered implementation tasks before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow directs the agent to continue automatically from planning into execution, which may begin implementation without affirmative user approval.

Mitigation: Review the continuation instructions and ensure the execution skill and its tools have suitable approval controls before use.

## Reference(s):

- [ClawHub release](https://clawhub.ai/athola/skills/nm-attune-project-planning)

## Skill Output:

**Output Type(s):** [Markdown, Planning guidance]

**Output Format:** [Structured implementation plan with architecture notes, tasks, dependencies, acceptance criteria, and estimates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dependency-ordered phases; may identify a critical path and risks when supported by the specification.]

## Skill Version(s):

1.10.4 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
