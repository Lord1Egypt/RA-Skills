## Description:

Diagnose and fix Kubernetes pods, CrashLoopBackOff, Pending, DNS, networking, storage, and rollout failures with kubectl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq280948982](https://clawhub.ai/user/qq280948982)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to investigate Kubernetes pod, rollout, networking, DNS, storage, resource, and cluster-health failures with guided kubectl workflows and diagnostic scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic output can expose sensitive Kubernetes cluster state, workload configuration, events, logs, YAML, and credential-adjacent data.

Mitigation: Use the skill only with trusted cluster contexts, store diagnostic reports securely, and review outputs before sharing them.

Risk: Network diagnostics can bypass TLS certificate validation when the explicit --insecure mode is used.

Mitigation: Avoid --insecure except for tightly scoped troubleshooting where the risk is understood and approved.

Risk: Unsafe script behavior could run unintended local commands, especially around token handling and bash command construction.

Mitigation: Send the skill through Review before installing, do not run it with untrusted environment variables, and fix token handling and bash -c command construction before production use.

Risk: Some Kubernetes actions proposed by the skill can be disruptive, including force deletion, node drains, rollout restarts, rollbacks, and debug pod creation.

Mitigation: Require explicit confirmation, capture current state first, confirm blast radius, and prepare a rollback path before running disruptive commands.

## Reference(s):

- [K8s Debug ClawHub Skill Page](https://clawhub.ai/qq280948982/skills/k8s-debug)
- [Kubernetes Troubleshooting Workflows](references/troubleshooting_workflow.md)
- [Common Kubernetes Issues and Troubleshooting](references/common_issues.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and sectioned diagnostic report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some scripts can write diagnostic reports to files; generated diagnostics may contain sensitive cluster, workload, event, log, YAML, and credential-adjacent data.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
