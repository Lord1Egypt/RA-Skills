## Description:

Orchestrator skill that audits Huawei Cloud network topology for security and configuration risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and network or security engineers use this skill to compare a described access path with live Huawei Cloud resources, assess topology and configuration risks, and receive a Markdown audit report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional quality reporting may send cloud credentials and audit context to a configurable remote endpoint when enabled.

Mitigation: Keep reporting disabled unless needed; before enabling it, review the telemetry settings, destination, and data that may be sent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-network-topology-audit)
- [Huawei Cloud DCS List Instances API](https://support.huaweicloud.com/api-dcs/ListInstances.html)
- [Huawei Cloud DCS Show Instance API](https://support.huaweicloud.com/api-dcs/ShowInstance.html)
- [Huawei Cloud CCE List Clusters API](https://support.huaweicloud.com/api-cce/ListClusters.html)
- [Huawei Cloud CCE List Nodes API](https://support.huaweicloud.com/api-cce/ListNodes.html)
- [Huawei Cloud API Explorer](https://console.huaweicloud.com/apiexplorer/#/openapi)
- [Resource-Skill Mapping](references/resource-skill-mapping.md)
- [Least-Privilege IAM Policies](references/iam-policies.md)
- [Rule Authoring Guide](references/rule-authoring-guide.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Markdown audit report with a Mermaid topology diagram and ASCII fallback]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes one described access path within a single Huawei Cloud account and region.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
