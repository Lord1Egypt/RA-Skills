## Description:

Provision and manage production-grade databases on Kubernetes using KubeBlocks for MySQL, PostgreSQL, Redis, MongoDB, Kafka, Elasticsearch, Milvus, Qdrant, RabbitMQ, and other data infrastructure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earayu](https://clawhub.ai/user/earayu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to route database requests to KubeBlocks workflows for provisioning, scaling, backup, restore, monitoring, security, and troubleshooting on Kubernetes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through broad Kubernetes database operations.

Mitigation: Use a least-privilege kubeconfig scoped to the intended cluster and namespace, and review planned operations before execution.

Risk: Installer, uninstall, apply, and delete commands can change cluster state or remove resources.

Mitigation: Pin and review downloaded installers, require explicit approval for sudo, kubectl apply/delete, uninstall, and production changes, and test outside production first.

Risk: Credential retrieval and external service exposure can reveal secrets or increase network exposure.

Mitigation: Require explicit approval before password retrieval or external exposure, protect secret output, and review LoadBalancer or NodePort settings before applying them.

## Reference(s):

- [KubeBlocks Official Docs](https://kubeblocks.io/docs/preview/user_docs/overview/introduction)
- [KubeBlocks GitHub Repository](https://github.com/apecloud/kubeblocks)
- [KubeBlocks LLM Index](https://kubeblocks.io/llms-full.txt)
- [Supported Addons](https://kubeblocks.io/docs/preview/user_docs/overview/supported-addons)
- [Safety Patterns](references/safety-patterns.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with YAML manifests and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Kubernetes manifests, Helm commands, kubectl commands, operational checklists, and troubleshooting guidance.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
