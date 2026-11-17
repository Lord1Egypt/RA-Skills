## Description:

Analyzes Java business code to identify monitorable business metrics and provide monitoring recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azrcn](https://clawhub.ai/user/azrcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze Java service, controller, manager, and facade code for monitorable business metrics. It produces metric name, label, type, and collection suggestions, with optional AOP, interceptor, and filter review to avoid duplicate collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases and optional project-wide AOP scanning could lead the agent to examine more Java files than the user intended.

Mitigation: Confirm the analysis scope and user approval before scanning AOP, interceptor, filter, or project-wide files.

Risk: Metric suggestions are based on code patterns and may not match the application's actual business semantics.

Mitigation: Review proposed metric names, labels, types, and collection methods against business definitions before instrumenting code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/azrcn/skills/metric-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/azrcn)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown report with tables and Java snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optional AOP, interceptor, and filter coverage notes when the user approves broader project scanning.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
