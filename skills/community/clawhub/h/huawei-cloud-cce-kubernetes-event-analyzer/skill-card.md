## Description: <br>
Query and analyze Kubernetes events in Huawei Cloud CCE clusters using API or LTS logs, apply filters, identify patterns, and hand off to diagnosis skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to inspect Huawei Cloud CCE Kubernetes events, identify warning patterns such as scheduling or mount failures, summarize affected resources, and decide which diagnosis workflow should receive the evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release presents as a read-only Kubernetes event analyzer, while the security scan reports bundled callable scripts with broader Huawei Cloud and Kubernetes administration actions. <br>
Mitigation: Review the installed script surface before use, restrict execution to the event-query tools, and require explicit manual approval before any scaling, deletion, node, addon, ECS, HPA, or public EIP action. <br>
Risk: The skill requires Huawei Cloud credentials and can access sensitive operational data from CCE, Kubernetes, and LTS sources. <br>
Mitigation: Use tightly scoped IAM and RBAC credentials, prefer least-privilege IAM users with MFA, avoid exposing AK/SK values, and rotate credentials regularly. <br>
Risk: Event and log outputs may expose production pod, node, workload, namespace, or cluster identifiers. <br>
Mitigation: Redact sensitive infrastructure names in shared summaries and inspect local report paths before distributing generated output. <br>
Risk: Unbounded event or log queries can overwhelm analysis and consume cloud API resources. <br>
Mitigation: Keep queries time-bounded, prefer recent 1-24 hour windows, and narrow by namespace, reason, or keyword where possible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pintudeyudi/huawei-cloud-cce-kubernetes-event-analyzer) <br>
- [Event Query Workflow](references/workflow.md) <br>
- [Risk Rules and Guardrails](references/risk-rules.md) <br>
- [Output Schema](references/output-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with JSON-like event query and analysis fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be time-bounded, redact sensitive cluster identifiers, and hand off remediation instead of executing it.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
