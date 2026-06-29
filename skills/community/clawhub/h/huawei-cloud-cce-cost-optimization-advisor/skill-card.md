## Description: <br>
Analyzes Huawei Cloud CCE clusters for cost optimization opportunities, including idle resources, oversized CPU and memory requests, low-utilization nodes, utilization trends, HPA recommendations, and node autoscaler policy suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and cloud operations teams use this skill to review Huawei Cloud CCE resource utilization, identify waste, and prepare cost optimization recommendations with verification and rollback guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan verdict is suspicious because the package is presented as a read-only cost advisor but includes callable Huawei Cloud and Kubernetes administrative actions that can modify infrastructure and access secrets or logs. <br>
Mitigation: Install only when broad Huawei Cloud and Kubernetes administrative capability is intended; prefer tightly scoped test accounts or read-only IAM and RBAC where possible. <br>
Risk: Cloud credentials may be exposed if passed directly in command-line arguments or logs. <br>
Mitigation: Use environment variables for Huawei Cloud credentials and review outputs for secrets before sharing reports. <br>
Risk: Configuration or scale changes could affect cluster availability or cost if executed without review. <br>
Mitigation: Review any invocation that can create, update, delete, expose, roll back, scale, or otherwise modify cluster resources; use preview mode and require explicit confirmation before applying changes. <br>
Risk: Cost recommendations based on incomplete metrics or a single short observation window can be misleading. <br>
Mitigation: Require both 24-hour and 7-day utilization windows, flag missing metrics or request data as data gaps, and include rollback and verification steps in recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pintudeyudi/huawei-cloud-cce-cost-optimization-advisor) <br>
- [Cost optimization workflow](references/workflow.md) <br>
- [Risk rules](references/risk-rules.md) <br>
- [Output schema](references/output-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON reports, Markdown summaries, YAML previews, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write summary JSON, report Markdown, chart files, or configuration previews when an output path is provided.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
