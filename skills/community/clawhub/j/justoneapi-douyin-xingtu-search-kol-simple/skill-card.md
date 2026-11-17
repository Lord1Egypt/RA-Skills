## Description:

Call GET /api/douyin-xingtu/search-kol-simple/v1 for Douyin Creator Marketplace (Xingtu) KOL Keyword Search through JustOneAPI with keyword, page, and platformSource.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query JustOneAPI for Douyin Creator Marketplace (Xingtu) creator search results by keyword, page, and platform source for creator sourcing and shortlist building.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a JustOneAPI token in ways that can expose it through process listings or URL logs.

Mitigation: Use a narrowly scoped or disposable token where possible, avoid sharing logs or process listings from runs, and rotate the token if command history, monitoring, or URL logs may have captured it.

Risk: The API call may consume paid quota or use broad account access attached to the supplied token.

Mitigation: Review the token's quota and account permissions before installation or execution, especially for long-lived or production credentials.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_search_kol_simple&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_search_kol_simple&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-search-kol-simple)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell command examples and raw JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JUST_ONE_API_TOKEN and returns endpoint-specific summaries before raw JSON when used as documented.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
