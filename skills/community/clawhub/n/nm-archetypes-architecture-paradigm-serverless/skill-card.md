## Description:

Serverless FaaS patterns. Use for bursty event-driven workloads with pay-per-execution cost and little infrastructure

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and architects use this skill to assess whether serverless functions fit event-driven workloads and to plan function boundaries, state management, deployment, observability, and cost controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider-specific APIs can make it costly to move the workload between cloud providers.

Mitigation: Where practical, place provider-specific calls behind interfaces or use portable frameworks.

Risk: Distributed function execution can make failures and latency difficult to trace.

Mitigation: Standardize tracing and structured logging across functions.

Risk: Concurrency, memory, and other provider limits can constrain workload growth.

Mitigation: Monitor provider quotas and design workloads to be shardable or horizontally scalable.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-serverless)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown prose and structured recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include serverless adoption steps, architecture decision record guidance, and infrastructure, deployment, observability, and cost recommendations.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
