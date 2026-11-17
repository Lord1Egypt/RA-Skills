## Description:

Call GET /api/instagram/get-post-detail/v1 for Instagram Post Details through JustOneAPI with code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve details for a specific Instagram post through JustOneAPI, including caption, media content, publish time, and engagement-oriented fields for analysis or archiving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is passed in command arguments and URL query parameters, which may expose it in process listings, logs, URLs, or diagnostics.

Mitigation: Use a narrowly scoped, revocable token, avoid shared machines and verbose command logging, and rotate the token if it may have appeared in process lists, logs, URLs, or diagnostics.

Risk: The skill makes authenticated requests to api.justoneapi.com using the user's token.

Mitigation: Install and run it only when you are comfortable granting a JustOneAPI token for this endpoint and external service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-instagram-get-post-detail)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_get_post_detail&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_get_post_detail&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; calls the JustOneAPI Instagram post detail endpoint with a post code.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
