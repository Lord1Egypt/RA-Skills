## Description:

Manage Helm charts, releases, and repositories. Use for Helm installations, upgrades, rollbacks, chart development, and release management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to manage Helm chart repositories and Kubernetes releases, including installing, upgrading, rolling back, and troubleshooting deployments. It also provides guidance for chart authoring, templating, linting, and packaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helm changes, especially uninstalling, deleting, or force-replacing resources, can disrupt running applications or remove data.

Mitigation: Use limited cluster permissions; confirm the cluster, namespace, and release before changes; require approval before uninstall, delete, or force-replace actions; and review backups and storage retention first.

Risk: Installing Helm through a downloaded installer can execute unreviewed code.

Mitigation: Install Helm from a verified release or inspect the installer before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rohitg00/skills/k8s-helm)
- [Chart Structure](references/CHART-STRUCTURE.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with Helm command examples and YAML configuration or chart templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and procedures are tailored to the requested Helm chart or release task.]

## Skill Version(s):

2.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
