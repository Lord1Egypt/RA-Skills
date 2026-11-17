## Description:

Call 3 get-shop-item-list versions for Taobao and Tmall Shop Product List through JustOneAPI with shopId and userId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call JustOneAPI's Taobao and Tmall shop product list endpoints for seller research and catalog tracking. It supports versioned GET operations that require a userId, and v2 or v3 also require a shopId.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens may be exposed through command-line arguments and query-string request URLs.

Mitigation: Use narrowly scoped, revocable JustOneAPI tokens; avoid shared shells or logged CI jobs; confirm logs and surrounding infrastructure redact token values before use.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_get_shop_item_list&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_get_shop_item_list&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, shell commands, json]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token plus endpoint parameters; returns API response JSON after endpoint-specific guidance.]

## Skill Version(s):

1.0.0 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
