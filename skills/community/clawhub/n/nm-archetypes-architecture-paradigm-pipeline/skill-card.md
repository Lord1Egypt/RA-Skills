## Description:

Provides guidance on the pipes-and-filters architecture paradigm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and architects use this skill to decide when a pipeline architecture fits and to plan its stages, data contracts, observability, and deployment. It also provides adoption guidance and exit criteria for reviewing a proposed pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A pipeline can become constrained by a single slow stage.

Mitigation: Monitor per-stage throughput and latency, and scale or split bottleneck stages when needed.

Risk: Schema changes between stages can cause incompatible data to flow through the pipeline.

Mitigation: Maintain shared schema definitions and enforce compatibility checks between adjacent stages.

Risk: Insufficient buffering or back-pressure handling can cause data loss under load.

Mitigation: Load test buffering, retries, and back-pressure at and above expected peak throughput.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-archetypes-architecture-paradigm-pipeline)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/archetypes)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Markdown architecture guidance with adoption steps, risks, and review criteria]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
