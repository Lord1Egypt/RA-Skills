## Description:

Call GET /api/facebook/get-profile-posts/v1 for Facebook Get Profile Posts through JustOneAPI with profileId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch public posts from a Facebook profile through JustOneAPI when they have a profile ID and a JustOneAPI token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is sent to api.justoneapi.com and used as a query parameter for this endpoint.

Mitigation: Use a narrowly scoped token if available, avoid sharing token values in chat or logs, and rotate the token if it is exposed.

Risk: Query-string authentication can appear in server, proxy, or diagnostic logs.

Mitigation: Review logging practices before use and avoid copying full request URLs that include credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-facebook-get-profile-posts)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook_get_profile_posts&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook_get_profile_posts&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper returns formatted JSON from the JustOneAPI endpoint and the skill asks agents to summarize the operation and profile lookup scope before raw JSON.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
