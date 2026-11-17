## Description:

通过快递单号查询欧美主流物流状态（UPS、FedEx、USPS、DHL、英国皇家邮政、PostNL 等）。当用户发送快递单号或询问包裹状态时触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhongkedy-del](https://clawhub.ai/user/zhongkedy-del)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to identify likely carriers from package tracking numbers and retrieve current delivery status, tracking events, estimated delivery dates, and carrier tracking links through Track123.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expose a Track123 API key by pasting it into chat or storing it directly in SKILL.md.

Mitigation: Configure the key through a protected secret store or environment variable, never paste it into chat, and rotate any key that was already exposed.

Risk: Package tracking numbers are sent to Track123 and can reveal shipment metadata to a third party.

Mitigation: Use the skill only when the user is comfortable sharing the tracking number with Track123, and avoid submitting sensitive shipment identifiers.

## Reference(s):

- [Track123 API](https://www.track123.com/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown tracking summaries with optional tables, event lists, carrier links, and inline curl commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch queries may include a summary table followed by individual tracking details; long tracking histories are truncated to recent events.]

## Skill Version(s):

1.0.4 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
