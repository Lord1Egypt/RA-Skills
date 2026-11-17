## Description:

Query specific Kubernetes resources in Huawei Cloud CCE clusters through kubectl cce. Trigger when users ask to get, describe, inspect, or view a Pod, workload, Service, ConfigMap, node, namespace, or other CCE Kubernetes resource, or when they ask to install or repair the local kubectl-cce prerequisites. Install kubectl and kubectl-cce only when they are missing locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to inspect specific Huawei Cloud CCE Kubernetes resources with read-only kubectl cce queries and to restore local kubectl-cce prerequisites when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented x509 recovery path automatically retries with upstream TLS verification disabled after certificate errors.

Mitigation: Remove the automatic TLS-bypass retry and resolve certificate trust errors before querying a cluster.

Risk: The skill and plugin guidance conflict on when cluster-wide reads are allowed.

Mitigation: Reconcile the query-scope rules, use narrowly scoped read-only credentials, and limit queries to the requested resource.

Risk: The kubectl-cce plugin implementation is downloaded separately and is not bundled with the skill.

Mitigation: Review the downloaded plugin separately before relying on it.

## Reference(s):

- [Plugin usage and credential guidance](artifact/references/plugin-usage.md)
- [Installation and troubleshooting](artifact/references/installation.md)
- [IAM and local access controls](artifact/references/iam-policies.md)
- [Resource-query acceptance criteria](artifact/references/acceptance-criteria.md)
- [Kubernetes release downloads](https://kubernetes.io/releases/download/)
- [kubectl-cce v0.2.1 release](https://gitee.com/pancake0001/kubectl-cce-plugin/releases/tag/v0.2.1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with resource-query results and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the target cluster, region, resource identity, requested status or fields, and prerequisite or installation state.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
