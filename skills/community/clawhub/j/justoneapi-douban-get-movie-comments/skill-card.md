## Description:

Call GET /api/douban/get-movie-comments/v1 for Douban Movie Comments through JustOneAPI with subjectId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to fetch Douban movie comments by subject ID through JustOneAPI, then summarize ratings, snippets, and interaction counts for sentiment sampling or review monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token is passed through command-line arguments and URL query parameters, which can expose credentials in process metadata or logs.

Mitigation: Use a low-scope, revocable token; avoid shared machines and verbose logging; rotate the token if command histories, process telemetry, proxy logs, or API logs may have exposed it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douban-get-movie-comments)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_movie_comments&utm_content=project_link)
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_movie_comments&utm_content=project_link)
- [Operations reference](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with inline shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a Douban subjectId; optional sort and page parameters control result ordering and pagination.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
