## Description:

Clawfuse runs a continuous LangFuse-driven optimization loop for OpenClaw/OpenRouter model routing and prompt usage controls with persistent local memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ekalb81](https://clawhub.ai/user/ekalb81)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to ingest LangFuse observations and evaluator scores, generate task-level OpenClaw/OpenRouter routing policy JSON, and run guarded optimization cycles for cost, quality, and latency tradeoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires LangFuse API credentials and can access LangFuse observations and scores.

Mitigation: Use a trusted HTTPS LangFuse host, prefer environment variables for credentials, and avoid persisting secrets in configuration.

Risk: Telemetry-derived raw snapshots, scores, policies, and memory files are written locally under the configured output directory.

Mitigation: Restrict output directory permissions and periodically delete raw snapshots or other artifacts that are no longer needed.

Risk: Generated routing policies can affect model selection, cost, latency, and quality if promoted to the live runtime.

Mitigation: Review staged policies before enabling daemon mode or live promotion, and keep live policy promotion disabled unless the explicit promotion gate is intended.

## Reference(s):

- [Closed-Loop Playbook](references/closed-loop-playbook.md)
- [Data Contracts](references/data-contracts.md)
- [LangFuse API Overview](https://langfuse.com/docs/api-and-data-platform/overview)
- [Clawfuse ClawHub Skill](https://clawhub.ai/ekalb81/skills/langfuse-continuous-optimizer)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON policy artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces staged routing policy files, model statistics, raw LangFuse snapshots, optional optimizer memory, and optional live policy promotion when explicitly enabled.]

## Skill Version(s):

0.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
