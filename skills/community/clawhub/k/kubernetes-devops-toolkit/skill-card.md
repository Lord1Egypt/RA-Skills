## Description:

Manage, deploy, monitor, and troubleshoot Kubernetes clusters with multi-cluster control, resource monitoring, log aggregation, diagnostics, and Helm lifecycle support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to operate Kubernetes clusters, deploy applications, monitor resources, aggregate logs, diagnose pod issues, and manage Helm releases across development and production environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helm install, upgrade, rollback, or list operations can target the wrong cluster because the configured kubeconfig is not passed to Helm commands.

Mitigation: Use an isolated kubeconfig and context, verify the active Helm context before changes, and prefer a patched version that passes the selected kubeconfig explicitly to every Helm command.

Risk: Using the toolkit with production Kubernetes access can read or modify live cluster resources.

Mitigation: Review carefully before installation, restrict the kubeconfig to the minimum required permissions, and test operations in a non-production context before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaiyuelv/skills/kubernetes-devops-toolkit)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform live Kubernetes API and Helm operations when connected to cluster credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
