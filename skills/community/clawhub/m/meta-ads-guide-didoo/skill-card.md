## Description:

[Didoo AI] Entry-point navigator and skill router for Didoo AI's Meta Ads workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elias-didoo](https://clawhub.ai/user/elias-didoo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill as an entry-point router for Didoo AI's Meta Ads workflow, selecting the right downstream skill for campaign strategy, creative work, publishing, monitoring, analysis, and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expose long-lived Meta access tokens while preparing downstream Meta Ads publishing or reporting tasks.

Mitigation: Use a protected secret store or OAuth-style connection when available, and grant only the minimum scopes needed for the task.

## Reference(s):

- [Didoo AI Blog](https://didoo.ai/blog)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with routing tables, workflow diagrams, and setup checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes Meta Ads tasks to related Didoo AI skills and identifies prerequisite campaign context.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
