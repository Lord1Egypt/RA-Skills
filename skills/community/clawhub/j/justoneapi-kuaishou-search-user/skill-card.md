## Description:

Call GET /api/kuaishou/search-user/v2 for Kuaishou User Search through JustOneAPI with keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to search Kuaishou user profiles through JustOneAPI by keyword. It supports creator discovery and account research by returning profile-oriented search results such as names, avatars, and follower counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JustOneAPI token exposure through command-line arguments and URL query strings.

Mitigation: Use a least-privilege, easily rotated token and avoid entering sensitive search terms where possible.

Risk: API tokens and search parameters may appear in local process metadata or service-side URL logs.

Mitigation: Review logs and runtime environments before use, and rotate the token if exposure is suspected.

## Reference(s):

- [Kuaishou User Search Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-kuaishou-search-user)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_search_user&utm_content=project_link)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_search_user&utm_content=project_link)
- [Generated Kuaishou User Search Operations](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary with raw JSON response data and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN environment value; accepts keyword and optional page query parameters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
