## Description:

Guides K8s beginners through Kubernetes cluster deployment with kubeasz, covering AllinOne quickstarts and high-availability production deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to plan prerequisites, generate kubeasz configuration, run deployment commands, and validate Kubernetes clusters for lab or production scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-assisted Kubernetes deployment guidance may lead to root SSH setup, remote installer execution, cluster-wide RBAC changes, and other high-impact host or cluster administration.

Mitigation: Use first in a disposable lab, require explicit approval before commands run, verify downloaded tools and images, avoid cluster-admin Dashboard tokens, and protect or remove deployment SSH keys.

Risk: Destructive operations such as delete, drain, destroy, restore, or reboot can disrupt workloads or cause data loss when aimed at the wrong environment.

Mitigation: Confirm backups, target cluster names, node identities, and maintenance windows before running destructive cluster or host operations.

## Reference(s):

- [kubeasz project homepage](https://github.com/easzlab/kubeasz)
- [Prerequisites guide](guides/01-prerequisites.md)
- [AllinOne quickstart guide](guides/02-allinone-quickstart.md)
- [Production deployment guide](guides/03-production-deploy.md)
- [Post-deployment verification guide](guides/04-post-deploy.md)
- [Troubleshooting guide](troubleshooting.md)
- [ClawHub skill page](https://clawhub.ai/cn-big-cabbage/skills/kubeasz-deploy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that alter Kubernetes clusters and host configuration; commands should require user approval before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
