## Description:

Call GET /api/instagram/search-hashtag-posts/v1 for Instagram Hashtag Posts Search through JustOneAPI with hashtag.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call JustOneAPI's Instagram hashtag posts endpoint for public hashtag lookup, then summarize captions, author profiles, and publish times for trend analysis or discussion monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A valuable or broad JustOneAPI token could be exposed through command text, request URLs, logs, screenshots, or shared transcripts.

Mitigation: Use a narrowly scoped token, pass it from the JUST_ONE_API_TOKEN environment variable, avoid logging commands or request URLs, and rotate the token if exposure is suspected.

Risk: Instagram hashtag monitoring can raise privacy, platform-policy, or local-law concerns when used beyond compliant public-data scenarios.

Mitigation: Use the endpoint only for permitted public-data workflows that comply with Instagram, JustOneAPI, privacy, and local legal requirements.

Risk: Backend error payloads or raw API responses may contain request or response details that should not be broadly shared.

Mitigation: Review backend payloads and raw JSON before sharing, storing, or pasting them into other systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-instagram-search-hashtag-posts)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_search_hashtag_posts&utm_content=project_link)
- [Generated operation reference](generated/operations.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown summary with optional raw JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN, the hashtag query parameter, and optionally endCursor for pagination.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
