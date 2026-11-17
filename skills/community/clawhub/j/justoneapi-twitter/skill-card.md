## Description:

Analyze Twitter workflows with JustOneAPI, including user Profile and user Published Posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to retrieve Twitter/X user profile metadata and published posts through JustOneAPI when they have a user Rest ID and a valid API token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Twitter/X lookup parameters and the JustOneAPI token are sent to api.justoneapi.com.

Mitigation: Install only when that data flow is acceptable for the user's use case, and avoid sending unnecessary identifiers or filters.

Risk: The API token could be exposed through chat messages, screenshots, shell history, process monitoring, or URL logs.

Mitigation: Keep JUST_ONE_API_TOKEN private, avoid logging commands that include it, and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-twitter)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_twitter&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_twitter&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and Twitter/X request parameters such as restId and optional cursor.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
