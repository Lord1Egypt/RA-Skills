## Description:

Query Prometheus monitoring metrics, alerts, and cluster status using PromQL with options for direct URL or Kubernetes port-forward access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peintune](https://clawhub.ai/user/peintune)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to inspect Prometheus metrics, alerts, and service health through direct Prometheus access or a Kubernetes port-forward.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prometheus metrics and alert labels can expose infrastructure details.

Mitigation: Use scoped Prometheus access and only provide endpoints the agent is authorized to inspect.

Risk: Queries can target arbitrary Prometheus URLs supplied at runtime.

Mitigation: Review the Prometheus endpoint and PromQL before execution, especially in shared or production environments.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text with optional shell commands and PromQL snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Formatted Prometheus metric, range-query, or alert results; matrix responses show the first five points per series.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
