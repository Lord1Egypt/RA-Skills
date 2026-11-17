## Description:

Call 2 get-user versions for Xiaohongshu (RedNote) User Profile through JustOneAPI with userId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call JustOneAPI Xiaohongshu (RedNote) user profile endpoints by userId and summarize profile data such as follower counts and bio details for creator research, account analysis, and competitor monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token can be exposed through command-line arguments and URL query strings.

Mitigation: Use a narrowly scoped token when available, avoid shared or heavily logged systems, and rotate the token if it may have appeared in command history, process monitoring, proxy logs, or API logs.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_user&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_user&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance]

**Output Format:** [Markdown summary followed by raw JSON from the selected API operation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a Xiaohongshu userId; supports getUserV3 and getUserV4.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
