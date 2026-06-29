## Description: <br>
Huawei Cloud CCE auto-remediation runner that converts remediation intent into preview-first, confirm-required, post-verified execution plans for CCE workloads, nodes, clusters, ECS, networking, and HSS actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to turn Huawei Cloud CCE remediation intent or diagnosis results into reviewable remediation plans, execute explicitly confirmed actions, and verify the result afterward. It is intended for high-impact operational workflows such as workload rollback or scaling, node cordon/drain, cluster hibernate or awake, traffic cutover, ECS start or stop, and HSS vulnerability status changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can exercise broad Huawei Cloud and Kubernetes administrative authority, including high-impact changes to workloads, nodes, clusters, ECS instances, networking, and HSS vulnerability status. <br>
Mitigation: Install only when that authority is intended, use least-privilege credentials, require preview and explicit confirmation for mutation actions, and verify state after execution. <br>
Risk: The skill requires sensitive Huawei Cloud credentials and can access secret-related operational data. <br>
Mitigation: Use short-lived or scoped credentials where possible, do not disclose credential environment variables, avoid include_data for Secrets, and do not request kubeconfig export through this skill. <br>
Risk: The security scan found extra high-impact cloud administration and secret-access capabilities that are not clearly disclosed. <br>
Mitigation: Review requested actions against the documented tool list, avoid enabling or invoking unlisted actions, and treat confirm=true as permission for live production changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pintudeyudi/huawei-cloud-cce-auto-remediation-runner) <br>
- [Workflow and action orchestration steps](references/workflow.md) <br>
- [Risk classification and confirm=true rules](references/risk-rules.md) <br>
- [Output execution record schema](references/output-schema.md) <br>
- [Huawei Cloud CCE Documentation](https://support.huaweicloud.com/cce/index.html) <br>
- [Huawei Cloud Python SDK Documentation](https://support.huaweicloud.com/api-cce/cce_02_0113.html) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON remediation previews and execution records, with optional Markdown reports and concise operator guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preview-first and confirmation-gated for mutation actions; post-execution verification is expected.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
