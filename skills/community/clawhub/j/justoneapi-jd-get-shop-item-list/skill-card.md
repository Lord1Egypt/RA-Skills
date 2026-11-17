## Description:

Call GET /api/jd/get-shop-item-list/v1 for JD.com Shop Product List through JustOneAPI with shopId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to call JustOneAPI's JD.com shop product-list endpoint for a supplied shopId and summarize returned item titles, prices, images, and related catalog data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is passed to the helper command and sent to api.justoneapi.com as a request URL query parameter.

Mitigation: Use a narrowly scoped token if available, avoid logging commands or full request URLs, and rotate the token if it may appear in process lists, shell history, monitoring, or URL logs.

Risk: The skill sends shop lookup requests to a third-party API service.

Mitigation: Install and run it only when sending the requested JD.com shopId and JustOneAPI token to api.justoneapi.com is acceptable.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_jd_get_shop_item_list&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_jd_get_shop_item_list&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-jd-get-shop-item-list)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON when results are returned]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and a JD.com shopId; optional page parameter supports pagination.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
