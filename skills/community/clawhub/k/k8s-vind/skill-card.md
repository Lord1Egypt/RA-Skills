## Description:

Manage vCluster (virtual Kubernetes clusters) instances using vind. Use when creating, managing, or operating lightweight virtual clusters for development, testing, or multi-tenancy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to create, connect to, configure, upgrade, pause, resume, and remove lightweight virtual Kubernetes clusters for development, testing, and multi-tenancy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cluster deletion and production workflows can cause disruption or data loss when targets are not checked and changes are not approved.

Mitigation: Restrict credentials to dedicated development namespaces, keep kubeconfigs private, verify the host context and namespace contents, require approval before deletion or production changes, preserve needed data, validate service and traffic cutovers, and pin and verify CLI downloads.

## Reference(s):

- [vCluster Workflow Reference](references/WORKFLOWS.md)
- [vCluster CLI release download](https://github.com/loft-sh/vcluster/releases/latest/download/vcluster-$(uname -s | tr '[:upper:]' '[:lower:]')-$(uname -m))
- [ClawHub skill release](https://clawhub.ai/rohitg00/skills/k8s-vind)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python tool-call examples, YAML manifests, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include kubeconfig output; keep credentials private.]

## Skill Version(s):

2.0.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
