## Description:

Analyze YOUKU workflows with JustOneAPI, including video Search, video Details, and user Profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search YOUKU videos, retrieve YOUKU video details, and inspect YOUKU user profiles through JustOneAPI-backed requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is passed through command-line arguments and URL query parameters.

Mitigation: Run the skill where process arguments and request URLs are not broadly logged, keep the token private, and rotate it if it may have appeared in logs or diagnostics.

Risk: YOUKU API requests and token-bearing calls are sent to JustOneAPI.

Mitigation: Install and use the skill only if you trust JustOneAPI with the requested YOUKU lookups and associated token handling.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youku&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youku&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with JSON API response data when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JUST_ONE_API_TOKEN and operation-specific parameters such as keyword, page, uid, or videoId.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
