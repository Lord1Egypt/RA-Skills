## Description:

Pans Gpu Calculator helps agents estimate GPU memory needs, recommend GPU configurations, and estimate costs for AI training and inference workloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and AI infrastructure sales teams use this skill to estimate GPU counts, memory needs, throughput, training time, and costs for model deployment planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Built-in prices and formulas may be rough planning assumptions rather than current procurement data.

Mitigation: Verify prices, utilization assumptions, and capacity requirements with the target cloud or hardware provider before purchasing capacity.

Risk: Broad GPU-related trigger phrases may activate the skill for general GPU sizing or cost questions.

Mitigation: Use the calculator only when the task needs GPU deployment estimates, and treat unrelated GPU advice as outside the skill's scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dashiming/skills/pans-gpu-calculator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown summaries, terminal tables, and optional JSON from the local calculator CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses built-in GPU price and performance assumptions; estimates should be verified before purchasing capacity.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
