## Description:

Helps users list Huawei Cloud OBS buckets with capacity and object counts and query download traffic and request counts with optional month-over-month comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use this skill to inspect OBS bucket capacity and object counts and summarize traffic and request trends through Huawei Cloud monitoring metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overly broad cloud permissions can expose more resources than the statistics task requires.

Mitigation: Use a read-only IAM user with CES read access; avoid OBS Administrator permissions.

Risk: Credentials may be exposed if access keys are shared in chat or pasted into commands.

Mitigation: Configure credentials interactively in the user's terminal and do not share access keys in conversation.

Risk: Bucket inventories and traffic statistics may reveal sensitive business information.

Mitigation: Limit access to outputs and review them before sharing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-obs-stats)
- [Huawei Cloud OBS monitoring metrics](https://support.huaweicloud.com/usermanual-obs/obs_03_0010.html)
- [Huawei Cloud CES ShowMetricData API](https://support.huaweicloud.com/api-ces/ces_03_0059.html)
- [Huawei Cloud OBS IAM authorization](https://support.huaweicloud.com/perms-cfg-obs/obs_40_0001.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown summaries, metric tables, and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Statistics depend on the selected region, bucket, and time range; comparisons are optional.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
