## Description:

Call GET /api/douban/get-movie-review-detail/v1 for Douban Movie Review Details through JustOneAPI with reviewId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up detailed Douban movie review data by reviewId through JustOneAPI, including metadata, content fields, and engagement signals for review archiving and opinion analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through command arguments or request URLs during normal invocation.

Mitigation: Use a short-lived or restricted token, avoid sharing command logs or URLs, and rotate the token if exposure is suspected.

Risk: The API token may have billing, quota, or account-level impact.

Mitigation: Review token scope and account limits before installation or use.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_movie_review_detail&utm_content=project_link)
- [Douban Movie Review Details API on ClawHub](https://clawhub.ai/justoneapi/skills/justoneapi-douban-get-movie-review-detail)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Markdown summary followed by raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, JUST_ONE_API_TOKEN, and a reviewId query parameter.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
