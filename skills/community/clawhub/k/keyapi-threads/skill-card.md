## Description:

Discover and analyze Threads users and content through the KeyAPI REST API using live official docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyzzero](https://clawhub.ai/user/xyzzero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to turn Threads profile, post, comment, and keyword-search questions into KeyAPI REST workflows, then return concise analysis, tables, raw JSON, or integration guidance grounded in the current KeyAPI docs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the auth helper can persist a KeyAPI token in shell startup files.

Mitigation: Prefer setting KEYAPI_TOKEN only in the current private shell session when persistence is not needed, avoid passing tokens on the command line, and review shell profile changes after setup.

Risk: The security evidence reports that helper options can send local file contents to KeyAPI when file-based body, query, or image inputs are used.

Mitigation: Use --body-file, --query-file, and --image-file only with files intentionally prepared for the request, and avoid sensitive local paths unless the user explicitly approves sending that content.

Risk: Live API calls can expose user-provided queries and retrieved Threads data to the KeyAPI service.

Mitigation: Limit requests to the approved task scope, avoid unnecessary broad crawling or fan-out enrichment, and keep API observations distinct from agent inference in reports.

## Reference(s):

- [KeyAPI Threads documentation index](https://docs.keyapi.ai/llms.txt)
- [KeyAPI Threads docs](https://docs.keyapi.ai/en/threads/)
- [KeyAPI API base URL](https://api.keyapi.ai)
- [KeyAPI authentication](https://docs.keyapi.ai/overview/authentication#bearer-authentication)
- [KeyAPI dashboard](https://keyapi.ai/app/dashboard)
- [Search profiles](https://docs.keyapi.ai/en/threads/search_profiles.md)
- [Get user info](https://docs.keyapi.ai/en/threads/fetch_user_info.md)
- [Get user info by ID](https://docs.keyapi.ai/en/threads/fetch_user_info_by_id.md)
- [Get user posts](https://docs.keyapi.ai/en/threads/fetch_user_posts.md)
- [Get user replies](https://docs.keyapi.ai/en/threads/fetch_user_replies.md)
- [Get user reposts](https://docs.keyapi.ai/en/threads/fetch_user_reposts.md)
- [Get post detail](https://docs.keyapi.ai/en/threads/fetch_post_detail.md)
- [Get post comments](https://docs.keyapi.ai/en/threads/fetch_post_comments.md)
- [Search top content](https://docs.keyapi.ai/en/threads/search_top.md)
- [Search recent content](https://docs.keyapi.ai/en/threads/search_recent.md)
- [Global rules](references/global-rules.md)
- [Scenario cards](references/scenarios.md)
- [Routing policy](references/routing-policy.md)
- [Setup and auth](references/setup-and-auth.md)
- [Threads rules](references/threads-rules.md)
- [Threads profile rules](references/threads-profile-rules.md)
- [Threads content rules](references/threads-content-rules.md)
- [Threads search rules](references/threads-search-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown with inline shell commands, optional tables, JSON snippets, and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce live KeyAPI observations, inferred analysis separated from observed facts, setup commands, and optional saved JSON outputs when requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
