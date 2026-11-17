## Description:

Configure Kubernetes autoscaling with HPA, VPA, and KEDA for horizontal and vertical pod autoscaling, event-driven scaling, and capacity management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Kubernetes operators use this skill to configure, inspect, and troubleshoot HPA, VPA, and KEDA autoscaling for workloads and capacity management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autoscaling examples may interrupt running services or activate workloads earlier than expected.

Mitigation: Restrict access to the intended cluster, namespace, and workload; validate activation thresholds and replica limits; start VPA in Off mode; and assess redundancy and disruption protections before enabling automatic updates.

## Reference(s):

- [Kubernetes Autoscaling release](https://clawhub.ai/rohitg00/skills/k8s-autoscaling)
- [KEDA trigger configuration guide](artifact/KEDA-TRIGGERS.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Code, Guidance]

**Output Format:** [Markdown guidance with YAML manifests and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes HPA, VPA, and KEDA autoscaling examples.]

## Skill Version(s):

2.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
