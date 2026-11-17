## Description:

Operate GPU inference clusters across vLLM, Ray Serve, SGLang, and TGI with observability, latency diagnosis, scaling, and model operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and inference platform engineers use this skill to inspect GPU serving health and performance, diagnose latency or utilization issues, and manage supported Ray Serve and model operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: State-changing operations can interrupt inference services, and MCP commands do not enforce approval checks.

Mitigation: Begin with access restricted to read and metrics endpoints. Before enabling writes, require approval outside the model for the exact target and change; treat audit logs and undo as records and recovery aids, not authorization.

Risk: Developer mode, configured endpoints, and credentials can expose production systems if misconfigured.

Mitigation: Keep developer mode disabled in production, protect endpoints and credentials, and test changes on a non-production cluster.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zw008/skills/inference-aiops)
- [Project homepage](https://github.com/AIops-tools/Inference-AIops)
- [Capabilities](references/capabilities.md)
- [Agent guardrails](references/agent-guardrails.md)
- [CLI reference](references/cli-reference.md)
- [Setup and security guide](references/setup-guide.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Structured operational results with concise Markdown guidance and shell commands when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cost per token is an estimate based on throughput and supplied GPU hourly pricing.]

## Skill Version(s):

0.13.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
