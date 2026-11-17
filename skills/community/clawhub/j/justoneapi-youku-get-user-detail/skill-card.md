## Description:

Call GET /api/youku/get-user-detail/v1 for YOUKU User Profile through JustOneAPI with uid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up a YOUKU profile by uid through JustOneAPI, then summarize profile data for creator analysis, account monitoring, and social CRM workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through command arguments or URL query strings.

Mitigation: Use a scoped or short-lived token when available, avoid sharing logs or process telemetry that may contain command arguments or URLs, and rotate the token if exposure is suspected.

Risk: A broad token or token with billing impact increases the consequence of misuse.

Mitigation: Review the skill before installing in environments where the JustOneAPI token has broad permissions or billing impact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-youku-get-user-detail)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youku_get_user_detail&utm_content=project_link)
- [YOUKU User Profile operations](generated/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown summary with an inline shell command and raw JSON response when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, JUST_ONE_API_TOKEN, and a uid query parameter.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
