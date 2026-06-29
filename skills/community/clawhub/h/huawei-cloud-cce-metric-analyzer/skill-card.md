## Description: <br>
Huawei Cloud CCE Metric Analyzer queries and analyzes CCE Pod and Node metrics plus ECS, ELB, EIP, and NAT resource metrics, including TopN rankings, time-series data, aggregation, and threshold-based anomaly detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to inspect Huawei Cloud CCE cluster and related cloud-resource metrics, identify high-utilization Pods, Nodes, and services, and summarize threshold-based anomalies for follow-up diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged dispatcher includes capabilities beyond the documented read-only metrics workflow. <br>
Mitigation: Review the dispatcher before installation and invoke only the declared metric-analysis actions for this skill. <br>
Risk: Huawei Cloud credentials and cluster access could expose sensitive cloud or Kubernetes resources. <br>
Mitigation: Use a least-privilege IAM user limited to read-only metric APIs, keep AK/SK values in environment variables, and avoid passing credentials as command parameters. <br>
Risk: Metric outputs may include sensitive pod names, node IPs, cluster IDs, kubeconfig material, certificates, or other operational identifiers. <br>
Mitigation: Treat generated outputs as sensitive and redact production identifiers before sharing summaries outside the operational team. <br>
Risk: Threshold classifications are baseline heuristics and may not match workload SLOs. <br>
Mitigation: Confirm thresholds against service-specific SLOs and use findings as input to diagnosis rather than as automatic remediation decisions. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Risk Rules](references/risk-rules.md) <br>
- [Output Schema](references/output-schema.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/pintudeyudi/huawei-cloud-cce-metric-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON metric results from the dispatcher] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include metric values, status classifications, time-series data, resource identifiers, and follow-up diagnostic recommendations.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
