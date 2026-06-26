## Description: <br>
Diagnose Kubernetes cluster issues when users ask about Pod crashes, deployment failures, service inaccessibility, node health, storage binding, events, or full-cluster checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[magicczc](https://clawhub.ai/user/magicczc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and platform engineers use this skill to inspect Kubernetes resource health through natural-language requests and receive structured diagnostic reports with severity levels and suggested fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires read access to the target Kubernetes cluster and the security scan flags overly broad cluster access and admin kubeconfig use as a concern. <br>
Mitigation: Use a least-privilege, user-provided kubeconfig, avoid production cluster-admin credentials, and confirm the current Kubernetes context before running diagnostics. <br>
Risk: Troubleshooting guidance may include commands such as delete, rollback, debug, port-forward, or test-pod actions that can change cluster state or expose services. <br>
Mitigation: Treat any suggested destructive, mutating, or network-exposing command as a proposal that requires explicit human review and approval before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/magicczc/k8sskill) <br>
- [Analyzer detailed description](artifact/references/analyzers.md) <br>
- [Troubleshooting manual](artifact/references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown diagnostic report with tables, severity labels, and suggested Kubernetes troubleshooting commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires access to a Kubernetes cluster through kubeconfig and is intended to run with read-only permissions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
