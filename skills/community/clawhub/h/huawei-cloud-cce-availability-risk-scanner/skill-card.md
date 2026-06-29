## Description: <br>
Scans Huawei Cloud CCE clusters for availability risks, reports severity-rated findings, and suggests remediation plans without directly changing cluster resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and platform engineers use this skill to assess Huawei Cloud CCE clusters for high-availability gaps such as single replicas, missing PodDisruptionBudgets, unhealthy probes, node or workload AZ imbalance, gateway concentration, and resource overcommit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package is presented as a read-only scanner, but the bundled dispatcher exposes broader live cloud and Kubernetes mutation actions. <br>
Mitigation: Restrict exposed actions to the read-only scanner actions listed in skill-profile.yaml before installation or deployment. <br>
Risk: The skill requires sensitive Huawei Cloud credentials and can access administrative cloud and Kubernetes APIs. <br>
Mitigation: Use least-privilege Huawei Cloud IAM and Kubernetes RBAC credentials that cannot create, delete, scale, update addons, read secret data, bind EIPs, or administer alarms. <br>
Risk: Availability recommendations and YAML suggestions may be inappropriate without workload context. <br>
Mitigation: Review remediation plans with the service owner and require explicit authorization before any operational change. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pintudeyudi/huawei-cloud-cce-availability-risk-scanner) <br>
- [Workflow](references/workflow.md) <br>
- [Risk Rules](references/risk-rules.md) <br>
- [Output Schema](references/output-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus structured JSON scan results, optional report files, remediation plans, and YAML suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Huawei Cloud credentials and CCE/Kubernetes read access; optional outputs include availability-risk-summary.json, availability-risk-report.md, and raw inventory files.] <br>

## Skill Version(s): <br>
0.1.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
