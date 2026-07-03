## Description: <br>
Diagnoses Huawei Cloud CCE workload rollout failures, replica shortages, probe readiness problems, and related workload evidence using a Python SDK dispatcher. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to investigate Deployment, StatefulSet, and DaemonSet rollout failures in Huawei Cloud CCE, including unavailable replicas, blocked ReplicaSet creation, probe failures, and event-backed handoffs to related diagnostics. Review before installation because server security evidence describes the packaged code as broader than a narrow read-only diagnoser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server security evidence says the package is broader than a narrow read-only CCE workload diagnoser and exposes powerful cloud, cluster, credential, secret, and remediation actions. <br>
Mitigation: Review the packaged actions before installation and prefer a split or patched version that exposes only the documented diagnostic actions. <br>
Risk: Broad Huawei Cloud permissions could allow destructive or mutating operations if credentials are over-privileged or confirm=true is used. <br>
Mitigation: Use a least-privilege IAM user that cannot delete or mutate clusters, nodes, workloads, addons, EIPs, AOM rules, HSS state, or Kubernetes secrets unless those powers are explicitly intended; avoid confirm=true unless a real production change is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pintudeyudi/huawei-cloud-cce-workload-failure-diagnoser) <br>
- [Workflow](references/workflow.md) <br>
- [Output Schema](references/output-schema.md) <br>
- [Risk Rules](references/risk-rules.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Huawei Cloud CCE Documentation](https://support.huaweicloud.com/cce/index.html) <br>
- [Huawei Cloud Python SDK CCE API Reference](https://support.huaweicloud.com/api-cce/cce_02_0113.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-shaped diagnostic outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces rollout summaries, evidence timelines, ranked top causes, warnings, and handoff recommendations; requires Huawei Cloud credentials and CCE identifiers.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
