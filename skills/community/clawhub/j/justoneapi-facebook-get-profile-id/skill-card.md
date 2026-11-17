## Description:

Calls JustOneAPI's Facebook get-profile-id endpoint to retrieve the unique Facebook profile ID from a supplied Facebook profile URL path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to look up a Facebook profile ID through JustOneAPI when given the profile URL path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is placed in the URL query string, where it may be captured by logs or telemetry.

Mitigation: Use the skill only when this credential handling is acceptable; prefer a version that uses an Authorization header or another non-query secret mechanism, and rotate the token if URLs may have been logged.

Risk: The supplied Facebook profile path is sent to JustOneAPI.

Mitigation: Submit only profile paths you are permitted to process and avoid using the skill for sensitive or private lookup contexts.

## Reference(s):

- [Facebook Get Profile ID operations](generated/operations.md)
- [JustOneAPI API homepage](https://api.justoneapi.com)
- [Just One API usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook_get_profile_id&utm_content=project_link)
- [Just One API dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook_get_profile_id&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown summary followed by raw JSON from the JustOneAPI endpoint.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; sends the Facebook profile path and token to JustOneAPI as query parameters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
