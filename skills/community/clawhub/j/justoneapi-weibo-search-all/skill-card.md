## Description:

Call GET /api/weibo/search-all/v2 for Weibo Keyword Search through JustOneAPI with endDay, endHour, q, startDay, and startHour.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Weibo keyword search data through JustOneAPI for trend monitoring, including authors, publish times, and engagement signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Weibo search terms and a JustOneAPI token to api.justoneapi.com.

Mitigation: Use a dedicated, least-privileged token where possible, avoid logging commands or full URLs, and rotate the token if it may have appeared in logs or monitoring.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_search_all&utm_content=project_link)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_search_all&utm_content=project_link)
- [ClawHub skill listing](https://clawhub.ai/justoneapi/skills/justoneapi-weibo-search-all)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with a shell command example and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN; the token and Weibo search terms are sent to api.justoneapi.com.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
