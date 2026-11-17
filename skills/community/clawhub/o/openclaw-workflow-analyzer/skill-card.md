## Description:

Analyzes a user's workflow, breaks it into automatable subprocesses, rates OpenClaw implementation difficulty, confirms third-party data dependencies, and recommends an incremental adoption path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangshan101-coder](https://clawhub.ai/user/fangshan101-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to evaluate which parts of a personal or team workflow are suitable for OpenClaw automation and what dependencies or learning steps are needed before implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automation recommendations may involve credentials, private systems, browser login, APIs, memory, or scheduled jobs.

Mitigation: Treat the skill output as planning guidance and confirm credentials, permissions, privacy impact, and approval boundaries before implementing automation.

Risk: Workflow assessments can be incomplete when third-party data access, API availability, or network reachability are unclear.

Mitigation: Ask the user to confirm APIs, authentication, export rights, network access, rate limits, costs, and browser automation feasibility before rating those steps.

## Reference(s):

- [OpenClaw capability matrix](references/openclaw-capabilities.md)
- [Project homepage](https://github.com/fangshan101-coder/openclaw-workflow-analyzer)
- [ClawHub skill page](https://clawhub.ai/fangshan101-coder/skills/openclaw-workflow-analyzer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown workflow analysis report with tables and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include clarifying questions before the final analysis when workflow details or third-party data access are unclear.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
