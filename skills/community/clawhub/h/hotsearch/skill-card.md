## Description:

Gets current Weibo, Baidu, and Douyin hot-search rankings, links, scores, and update times through JisuAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer hot-search questions by retrieving current Weibo, Baidu, and Douyin rankings from JisuAPI and summarizing titles, links, scores, and update times.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts JisuAPI and uses JISU_API_KEY, so the API key is a credential exposed to the configured runtime environment.

Mitigation: Set JISU_API_KEY only in trusted agent runtimes, avoid logging it, and review JisuAPI terms, pricing, and privacy practices before use.

Risk: Hot-search results are live third-party API data and may be unavailable, delayed, or returned with API errors.

Mitigation: Handle api_error, http_error, request_failed, and invalid_json outputs, and include update times when summarizing trends.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/hotsearch)
- [JisuAPI](https://www.jisuapi.com/)
- [JisuAPI hot-search API](https://www.jisuapi.com/api/hotsearch/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON from the helper script; text or Markdown summaries from the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; returns one platform's hot-search result list per invocation.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
