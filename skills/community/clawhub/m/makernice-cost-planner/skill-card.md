## Description:

Plan which Makernice models, resolutions and durations fit a budget before generating anything. Use when the user gives a budget in USD, asks how many videos or images they can make, or wants to compare the price of options. Planning never creates jobs or charges anything.

This skill is ready for commercial/non-commercial use.

## Publisher:

[makernice](https://clawhub.ai/user/makernice)

### License/Terms of Use:

MIT-0

## Use Case:

Creators use this skill to compare model, resolution, and duration options against a USD budget before deciding whether to run paid image or video generation jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prices or job parameters may change between planning and generation, and successful jobs remain chargeable even if safety review blocks their outputs.

Mitigation: Before each job, estimate its final prompt and parameters again, approve the scope and spending limit, and use the returned amount as max_cost_usd. Check per-job and daily limits before running the plan.

Risk: Price-cap and duplicate-charge protections depend on the connected service.

Mitigation: Confirm the connected service's limits and protections before relying on them; retry transient failures only with the same request_id and job parameters.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/makernice/skills/makernice-cost-planner)

## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Markdown comparison table with a recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices are in USD; planning does not create jobs or incur generation charges.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
