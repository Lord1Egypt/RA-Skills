## Description:

Operate fal.ai model endpoints through an OOMOL-connected account, including model discovery, pricing, queued job submission, monitoring, cancellation, and result retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to discover fal.ai models and pricing, submit queued model jobs, monitor or cancel them, and retrieve completed results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may make broader, persistent changes to installed agent skills through synchronization.

Mitigation: Review the CLI before installing it; set OO_SKILLS_SYNC_DISABLED=1 before CLI use if you do not want skill synchronization.

Risk: Using the connected service entrusts OOMOL with provider credentials and request processing, and submitted jobs may incur costs.

Mitigation: Review the data sent and the relevant pricing before submission, and confirm the job's cancellation target.

Risk: The external installer and hosted implementation were not verified in the security assessment.

Mitigation: Review and install the CLI yourself before enabling the skill.

## Reference(s):

- [fal.ai](https://fal.ai)
- [fal.ai Model API documentation](https://docs.fal.ai/model-apis)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action responses with concise task guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected fal.ai endpoint and action.]

## Skill Version(s):

1.0.7 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
