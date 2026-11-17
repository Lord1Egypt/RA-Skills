## Description:

Call GET /api/bilibili/get-user-relation-stat/v1 for Bilibili user relation stats through JustOneAPI with wmid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to call a focused JustOneAPI Bilibili endpoint and retrieve user relation statistics for a supplied Bilibili WMID. The result supports creator benchmarking and audience growth tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is passed through a command-line argument and included as a URL query parameter.

Mitigation: Use a short-lived or narrowly scoped token when available, avoid sharing logs or screenshots that may capture the command or URL, and rotate the token if exposure is suspected.

Risk: The skill sends the provided WMID and token to api.justoneapi.com to retrieve Bilibili relation statistics.

Mitigation: Install and run the skill only when that data flow is acceptable for the intended user, account, and environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-bilibili-get-user-relation-stat)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_user_relation_stat&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_user_relation_stat&utm_content=project_link)
- [Generated operation reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, JSON]

**Output Format:** [Markdown summary with a shell command example and raw JSON API output when the endpoint is called]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; the endpoint requires wmid.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
