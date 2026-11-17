## Description:

Analyze TikTok workflows with JustOneAPI, including user Published Posts, post Details, and user Profile across 7 operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and analysts use this skill to retrieve TikTok profile, post, comment, reply, and search data through JustOneAPI when they have the required token and identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through process arguments or request URLs.

Mitigation: Run the skill where process arguments and request URLs are not logged, keep JUST_ONE_API_TOKEN private, and rotate the token if it may have appeared in logs.

Risk: TikTok profile, post, comment, reply, or search responses may include personal data.

Mitigation: Request data only for a legitimate purpose and handle returned personal data according to the user's policy and applicable requirements.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and TikTok identifiers or filters such as awemeId, postId, secUid, keyword, cursor, or commentId.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
