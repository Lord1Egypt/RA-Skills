## Description:

查询附近政府认证养老助餐点（北京、广州、深圳），数据来自政府公开名录，按距离排序，附电话和使用提醒。

This skill is ready for commercial/non-commercial use.

## Publisher:

[han815757857-cmd](https://clawhub.ai/user/han815757857-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Older adults and family members can use the skill to find nearby government-listed meal service locations in Beijing, Guangzhou, and Shenzhen, then check addresses, phone numbers, and practical usage reminders.

### Deployment Geography for Use:

China (Beijing, Guangzhou, and Shenzhen)

## Known Risks and Mitigations:

Risk: The security scan marks the skill suspicious because its API key and location queries could be sent to an untrusted destination; the scan was partial.

Mitigation: Before installation, confirm the endpoint uses HTTPS and an approved host, and clearly tell users what location data is sent and to whom. Keep the API key in the GAODE_POI_KEY environment variable and out of files.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/han815757857-cmd/skills/govt-meal-finder)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [Markdown by default, or JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Nearby meal-point names, addresses, phone numbers, straight-line distances, and usage reminders; up to 20 results.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
