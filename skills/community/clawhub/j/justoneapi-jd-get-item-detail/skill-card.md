## Description:

Call GET /api/jd/get-item-detail/v1 for JD.com Product Details through JustOneAPI with itemId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ecommerce analysts use this skill to retrieve JD.com product detail data by item ID, including pricing, images, and shop information, for catalog analysis, product monitoring, and ecommerce research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is sent as a query parameter for JD.com product-detail lookups.

Mitigation: Use a narrowly scoped or revocable token, avoid sharing token values in chat or logs, and rotate the token if request URLs may have been captured by infrastructure logs.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_jd_get_item_detail&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_jd_get_item_detail&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-jd-get-item-detail)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON, or formatted JSON from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and an itemId query parameter.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
