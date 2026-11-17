## Description:

Browser automation for Kubernetes dashboards and web UIs, including Kubernetes Dashboard, Grafana, ArgoCD UI, and similar interfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:


## Use Case:

Developers and cluster operators use this skill to drive browser-based Kubernetes workflows, inspect dashboards, interact with Grafana, and operate ArgoCD or similar web UIs through browser automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation can perform live ArgoCD sync, deploy, or other cluster-changing UI actions.

Mitigation: Require explicit approval before any cluster-changing action and review planned actions before execution.

Risk: Credential examples and authenticated dashboard workflows can expose real tokens or passwords in prompts, logs, or screenshots.

Mitigation: Use least-privilege, short-lived credentials and redact secrets from prompts, logs, and captured images.

Risk: Use against production clusters can inherit the operator's access and affect production resources.

Mitigation: Review the skill before installation, prefer non-production validation first, and restrict access to the minimum required cluster permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rohitg00/skills/k8s-browser)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash snippets and Python-style browser automation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser navigation steps, selectors, session commands, device or viewport settings, and screenshot capture instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
