## Description:

Respond to Kubernetes incidents with runbooks and diagnostics. Use for outages, pod failures, node issues, network problems, and emergency response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to triage Kubernetes outages, investigate pod, node, network, and control-plane issues, and follow incident recovery runbooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Emergency actions such as deleting resources or rolling back workloads can disrupt production services.

Mitigation: Restrict access to the intended cluster and namespaces, and require explicit approval before each deletion or rollback.

Risk: An unverified or incorrect recovery revision can worsen an incident.

Mitigation: Review release history and select a verified recovery revision rather than defaulting to revision 1.

Risk: Inspecting Kubernetes Secrets or retaining diagnostic logs can expose sensitive information.

Mitigation: Limit Secret inspection to relevant resources and protect diagnostic logs.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/rohitg00/skills/k8s-incident)
- [Publisher profile](https://clawhub.ai/user/rohitg00)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown runbooks with diagnostic guidance and example Kubernetes command/tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples are intended for use in an authorized Kubernetes environment.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
