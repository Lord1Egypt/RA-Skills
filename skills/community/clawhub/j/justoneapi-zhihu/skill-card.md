## Description:

Search Zhihu topics, inspect answer lists, read column article detail, and track column article feeds through JustOneAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Zhihu content through JustOneAPI for topic discovery, answer research, column article archiving, and content monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through process listings or full URL logs because authenticated requests use a command-line token and query parameters.

Mitigation: Use a narrowly scoped token if available, avoid environments that log command arguments or full URLs, and rotate the token if exposure is suspected.

## Reference(s):

- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_zhihu&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown summaries with structured JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN; operations are read-only GET requests with query parameters and no request bodies.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
