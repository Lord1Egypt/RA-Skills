## Description:

Kubernetes Agent Swarm is an instruction-only, coordinated multi-agent system for Kubernetes and OpenShift platform operations across orchestration, cluster operations, GitOps, security, observability, artifacts, and developer experience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kcns008](https://clawhub.ai/user/kcns008)

### License/Terms of Use:

MIT-0

## Use Case:

Platform engineers, SREs, security engineers, and developer-experience teams use this skill to coordinate Kubernetes and OpenShift operations, triage incidents, manage GitOps workflows, inspect cluster state, and prepare operational reports. The skill provides markdown guidance and command patterns that rely on host-installed tools such as kubectl, oc, helm, and jq.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad cluster, cloud, and repository authority could expose or change sensitive operational state.

Mitigation: Install only in a controlled operations environment with narrowed kubeconfig and cloud permissions, and require explicit approval for upgrades, secret reads, and external incident transmissions.

Risk: Operational logs, alerts, and incident messages could disclose sensitive data.

Mitigation: Apply strict redaction rules before writing logs, sending alerts, or sharing incident details.

Risk: Automated repository update flows could persist unintended changes.

Mitigation: Disable or rewrite broad git add and auto-PR workflows, and require human review before repository changes are submitted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kcns008/skills/kubernetes)
- [Skill Definition](artifact/SKILL.md)
- [Swarm README](artifact/README.md)
- [Swarm Configuration and Protocols](artifact/AGENTS.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell command examples and YAML or JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only output; no executable scripts are bundled.]

## Skill Version(s):

2.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
