## Description:

Call GET /api/xiaohongshu-pgy/api/solar/cooperator/blogger/v2/v1 for Xiaohongshu Creator Marketplace (Pugongying) Creator Search through JustOneAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Xiaohongshu Creator Marketplace creators through JustOneAPI, applying filters such as keyword, audience age, audience gender, creator gender, content tags, fan-count range, and page number for discovery, comparison, and shortlist building.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through command-line arguments and request URLs.

Mitigation: Use a narrowly scoped token, avoid shell tracing and shared process-monitoring environments, rotate the token if command lines or request URLs may have been logged, and prefer a version that supports header-based authentication.

Risk: The skill can consume account quota or billing through API calls.

Mitigation: Review requests before execution and use tokens with the least quota and account access needed for the task.

## Reference(s):

- [JustOneAPI API Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_cooperator_blogger_v2&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_cooperator_blogger_v2&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown summary followed by raw JSON response data or JSON error details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN; token is passed to the helper and sent as a query parameter for the documented API operation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
