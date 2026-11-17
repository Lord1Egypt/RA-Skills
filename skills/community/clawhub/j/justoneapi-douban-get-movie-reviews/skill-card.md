## Description:

Call GET /api/douban/get-movie-reviews/v1 for Douban Movie Movie Reviews through JustOneAPI with subjectId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call JustOneAPI's Douban movie reviews endpoint for review titles, ratings, snippets, and audience-sentiment research keyed by a Douban subject ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a JustOneAPI token, and token exposure in chat, logs, screenshots, shell history, or process listings could allow unauthorized API use.

Mitigation: Use a narrowly scoped, revocable token; pass it through the documented environment variable or token argument; avoid sharing command logs; and rotate the token if exposure is suspected.

Risk: Movie review lookup requests are sent to api.justoneapi.com.

Mitigation: Confirm that the subject IDs and query parameters are appropriate to send to the third-party API before execution.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_movie_reviews&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_movie_reviews&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douban-get-movie-reviews)
- [Generated operation reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Concise Markdown summary followed by raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; required endpoint input is subjectId, with optional sort and page query parameters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
