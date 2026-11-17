## Description:

Builds GPU compute plans from workload type, deployment scale, and monthly budget, then recommends GPU configurations, estimated costs, scaling roadmap, and technical guidance in Markdown or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure planners use this skill to draft GPU sizing and budget options for training, inference, fine-tuning, batch inference, and development workloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GPU pricing and sizing assumptions may be inaccurate or stale for purchasing or budgeting decisions.

Mitigation: Independently verify the generated cost and capacity recommendations before using them for procurement, budgeting, or production planning.

Risk: The --output option can create or overwrite the user-specified output file.

Mitigation: Use a workspace-local output path and choose a filename that is acceptable to create or overwrite.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dashiming/skills/pans-gpu-solution-builder)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write output to a user-specified file path when the --output option is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
