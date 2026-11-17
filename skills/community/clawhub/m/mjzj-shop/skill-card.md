## Description:

卖家之家(跨境电商)全球开店平台查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjzj-tec](https://clawhub.ai/user/mjzj-tec)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search the 卖家之家 global ecommerce shop-opening platform directory by platform name. It calls the public /api/global/queryPlatform endpoint and returns platform matches or the full platform list when no keyword is supplied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Platform search keywords are sent to data.mjzj.com.

Mitigation: Avoid entering sensitive personal, customer, or business secrets as search keywords.

Risk: The metadata declares MJZJ_API_KEY while the skill text says the endpoint is public.

Mitigation: Verify deployment configuration before installation and avoid supplying secrets unless the service requires them.

Risk: Snowflake-style IDs can lose precision if handled as numbers.

Mitigation: Treat id fields such as id and regionId strictly as strings in requests, responses, and downstream output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mjzj-tec/skills/mjzj-shop)
- [卖家之家全球开店平台](https://mjzj.com/gongxu)
- [queryPlatform API example](https://data.mjzj.com/api/global/queryPlatform?keywords=amazon)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [Markdown or plain text responses based on JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserve id fields such as id and regionId as strings to avoid snowflake ID precision loss.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
