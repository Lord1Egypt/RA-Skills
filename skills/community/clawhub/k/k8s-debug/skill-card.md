## Description: <br>
Diagnose and fix Kubernetes pods, CrashLoopBackOff, Pending, DNS, networking, storage, and rollout failures with kubectl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qq280948982](https://clawhub.ai/user/qq280948982) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to diagnose Kubernetes workload, networking, storage, rollout, and cluster-health failures with a read-only-first workflow and targeted kubectl commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs access to the user's current Kubernetes context, which can expose cluster diagnostics, credentials, and sensitive operational data. <br>
Mitigation: Use a least-privilege kubeconfig, confirm the active cluster and namespace before running commands, and treat saved diagnostics as sensitive. <br>
Risk: Some Kubernetes actions suggested during troubleshooting can disrupt workloads or change cluster state. <br>
Mitigation: Review rollout, delete, drain, create-secret, and apply commands before approval, and capture current state before disruptive operations. <br>
Risk: The security scan notes an avoidable shell-command injection risk related to K8S_REQUEST_TIMEOUT. <br>
Mitigation: Do not set K8S_REQUEST_TIMEOUT from untrusted input; use trusted timeout values or the default. <br>


## Reference(s): <br>
- [Kubernetes Troubleshooting Workflows](references/troubleshooting_workflow.md) <br>
- [Common Kubernetes Issues and Troubleshooting](references/common_issues.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and diagnostic report guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save diagnostics to text files when requested; cluster outputs should be treated as sensitive.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
