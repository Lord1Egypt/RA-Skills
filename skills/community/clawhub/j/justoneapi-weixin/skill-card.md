## Description:

Analyze WeChat Official Accounts workflows with JustOneAPI, including user Published Posts, article Engagement Metrics, and article Comments across 5 operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve API-backed WeChat Official Accounts posts, article details, engagement metrics, comments, and keyword search results from JustOneAPI when they have the required account IDs, article URLs, or search filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeChat article URLs, account IDs, keywords, and returned content are sent through JustOneAPI.

Mitigation: Use the skill only when sharing those identifiers and returned content with JustOneAPI is acceptable for the task.

Risk: JUST_ONE_API_TOKEN is passed through command arguments and query parameters, which can expose it through shell tracing, logs, process monitoring, or request logs.

Mitigation: Keep the token out of chat, screenshots, shell history, CI logs, and request logs; disable tracing around calls and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-weixin)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN for authenticated JustOneAPI requests.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
