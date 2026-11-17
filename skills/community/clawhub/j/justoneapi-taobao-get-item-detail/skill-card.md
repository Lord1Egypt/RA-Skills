## Description:

Call 5 get-item-detail versions for Taobao and Tmall Product Details through JustOneAPI with itemId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to retrieve Taobao and Tmall product detail data by item ID for product research, catalog monitoring, and ecommerce analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is passed through command-line arguments and URL query parameters.

Mitigation: Use a low-privilege, revocable token, avoid sharing token values in chat or logs, and install the skill only when JustOneAPI is trusted with the token and product item IDs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-taobao-get-item-detail)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_get_item_detail&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_get_item_detail&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; supported operations call versioned GET endpoints under /api/taobao/get-item-detail.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
