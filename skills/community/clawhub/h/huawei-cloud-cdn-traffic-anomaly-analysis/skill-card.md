## Description:

Analyzes Huawei Cloud CDN traffic and bandwidth for a domain against a three-month baseline and absolute thresholds to flag possible anomalies or abuse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

CDN operators and engineers use this skill to inspect their Huawei Cloud CDN billing mode and domain traffic, compare recent usage with a three-month baseline, and identify potential traffic or bandwidth anomalies without changing CDN settings.

### Deployment Geography for Use:

Mainland China CDN analysis; overseas and cross-border analysis are not supported.

## Known Risks and Mitigations:

Risk: Huawei Cloud access keys may be exposed if pasted into a conversation or configured on an untrusted machine.

Mitigation: Never share access keys in chat; configure credentials locally on a trusted machine.

Risk: Overly broad IAM access could allow actions beyond the skill's read-only analysis.

Mitigation: Use a dedicated least-privilege IAM user with read-only CDN permissions and refuse requests to modify CDN resources.

Risk: Traffic spikes alone do not establish that traffic theft or abuse occurred.

Mitigation: Treat anomaly flags as screening signals and verify against account data before taking action.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cdn-traffic-anomaly-analysis)
- [Huawei Cloud CLI documentation](https://support.huaweicloud.com/hcloudcli/index.html)
- [Traffic metric queries](artifact/references/task-query-metrics.md)
- [Anomaly thresholds and report format](artifact/references/task-threshold-judgment.md)
- [Read-only IAM permissions](artifact/references/iam-policies.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown analysis report with metrics, baseline comparison, verdict, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only; daily metrics and three-tier anomaly status.]

## Skill Version(s):

1.0.2 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
