## Description:

Analyze Facebook workflows with JustOneAPI, including post Search, get Profile ID, and get Profile Posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to retrieve Facebook profile IDs, fetch public profile posts, and search public Facebook posts through JustOneAPI-backed requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Facebook lookup or search inputs and a JustOneAPI token to JustOneAPI.

Mitigation: Install only when that data flow is acceptable for the intended use case.

Risk: The JustOneAPI token is handled in command arguments and URL query parameters, which can expose it in logs or process listings.

Mitigation: Use a token with limited scope and quota, avoid logging full command lines or request URLs, and rotate the token if exposed.

## Reference(s):

- [Facebook operations](artifact/generated/operations.md)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-facebook)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance]

**Output Format:** [Plain-language answers with selected JSON fields and optional raw JSON excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and Node.js; API responses come from JustOneAPI Facebook endpoints.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
