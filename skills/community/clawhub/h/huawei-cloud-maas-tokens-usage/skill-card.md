## Description:

Queries Huawei Cloud MaaS token, request, and error statistics for a selected time range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to review Huawei Cloud MaaS token consumption, request volume, and error rates. It queries aggregate statistics for preset service, My Service, or a custom endpoint.

### Deployment Geography for Use:

Huawei Cloud cn-southwest-2 (Southwest-Guiyang-1) only

## Known Risks and Mitigations:

Risk: Optional notifications could forward usage statistics to an unapproved recipient through redirects.

Mitigation: Use query-only mode until webhook redirects are blocked or every redirect destination is validated. If enabling notifications, approve the exact recipient and the data shared.

## Reference(s):

- [Huawei Cloud MaaS ShowStatistics API](https://support.huaweicloud.com/api-maas/ShowStatistics.html)
- [MaaS tokens usage query guide](references/task-query-tokens-usage.md)
- [Security guide](references/security-guide.md)
- [Security design](references/security-design.md)
- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-maas-tokens-usage)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Plain-text metrics table with the queried period and optional query or setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Aggregate statistics for a selected time range; optional raw JSON response.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
