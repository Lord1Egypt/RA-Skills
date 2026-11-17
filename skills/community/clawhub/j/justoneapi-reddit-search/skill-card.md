## Description:

Call GET /api/reddit/search/v1 for Reddit Keyword Search through JustOneAPI with keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Reddit by keyword through JustOneAPI and summarize titles, authors, and subreddit context for topic discovery and monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token may be exposed through command-line arguments and URL query parameters.

Mitigation: Use a short-lived, scoped token, avoid sensitive search terms, and rotate the token if it may have appeared in shell history, process telemetry, proxy logs, or API gateway logs.

Risk: Reddit search keywords are sent to api.justoneapi.com.

Mitigation: Avoid sending confidential or sensitive keywords unless that external service use is acceptable for the deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-reddit-search)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_reddit_search&utm_content=project_link)
- [Reddit Keyword Search Operations](generated/operations.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary with raw JSON response data and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a keyword; supports an optional after pagination token.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
