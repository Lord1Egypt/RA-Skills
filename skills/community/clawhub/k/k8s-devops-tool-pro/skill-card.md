## Description:

K8s清单生成专业版 helps DevOps teams generate and manage Kubernetes manifests with Helm, Kustomize, policy validation, multi-environment workflows, GitOps, CI/CD, and CRD guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, and platform teams use this skill for Kubernetes manifest, Helm Chart, Kustomize overlay, policy validation, GitOps, CI/CD, and CRD work. It should not be used for unrelated analytics or reporting tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes overly broad analytics and reporting trigger language that could route unrelated tasks to a Kubernetes DevOps workflow.

Mitigation: Use it only for Kubernetes manifest, Helm, Kustomize, policy, GitOps, or CRD work.

Risk: Suggested publish, sync, prune, install, or production commands can affect live infrastructure.

Mitigation: Require an explicit target cluster, environment, repository, and dry-run or user confirmation before running those commands.

Risk: Credentials such as Helm, ArgoCD, or Git tokens could be mishandled in local configuration.

Mitigation: Use protected environment variables or approved secret storage, and do not store tokens in plaintext local config files without verified permissions and storage protections.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/k8s-devops-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose file changes or Kubernetes-related commands; review targets and credentials before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
