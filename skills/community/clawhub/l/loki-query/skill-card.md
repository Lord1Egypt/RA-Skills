## Description:

Query Grafana Loki logs by trace ID, keywords, pod, namespace, labels, or time range to debug Kubernetes application issues through the Loki API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peintune](https://clawhub.ai/user/peintune)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to generate and run Loki LogQL queries for Kubernetes troubleshooting, including error searches, trace lookups, pod log review, label filtering, and time-bounded investigation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Loki queries can expose sensitive production log data.

Mitigation: Use a scoped Loki URL or Kubernetes context and review returned logs before sharing or storing them.

Risk: Network or Kubernetes access may reach unintended log sources if the endpoint or context is broad.

Mitigation: Limit access to the intended namespace, labels, time range, and Loki endpoint before running queries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/peintune/skills/loki-query)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text, JSON]

**Output Format:** [Markdown with inline shell commands and optional formatted log text or raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include returned log lines from Loki; query limit defaults to 100 and direct Loki URL access defaults to http://localhost:3100.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
