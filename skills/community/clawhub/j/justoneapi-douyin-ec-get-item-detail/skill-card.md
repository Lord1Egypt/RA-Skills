## Description:

Call GET /api/douyin-ec/get-item-detail/v1 for Douyin E-commerce Item Details through JustOneAPI with itemId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and commerce analysts use this skill to retrieve Douyin e-commerce item details, including price, title, and stock, via JustOneAPI for product monitoring and competitive analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through request URLs or process arguments.

Mitigation: Use a narrowly scoped, low-privilege token; rotate it regularly; and avoid environments that record command lines or full URLs in logs.

Risk: The skill depends on a third-party API service and may return backend error payloads.

Mitigation: Review backend responses before sharing them and avoid including sensitive tokens, URLs, or business data in logs or chat transcripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-ec-get-item-detail)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_ec_get_item_detail&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_ec_get_item_detail&utm_content=project_link)
- [Generated Operation Reference](generated/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with a shell command pattern and JSON API response output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and an itemId query parameter.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
