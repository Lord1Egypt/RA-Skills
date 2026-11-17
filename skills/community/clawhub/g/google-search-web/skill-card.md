## Description:

Calls a Google web search API endpoint to retrieve real-time web search results, including result titles, links, and snippets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyriswu](https://clawhub.ai/user/kyriswu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need to run a Google web search and return a concise list of titles, links, and snippets. It supports searches through a bundled Python script using a required query and an optional paid API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and optional AZT API keys are sent to a third-party endpoint.

Mitigation: Use the skill only when the user trusts the endpoint with the query, avoid sensitive searches, and provide paid API keys through environment variables or managed secrets instead of command-line arguments.

Risk: Free-tier usage may fail after the daily limit or when the endpoint returns an error.

Mitigation: Check the returned status message, retry later for transient service failures, or configure a valid paid API key for higher-frequency use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyriswu/skills/google-search-web)
- [Publisher profile](https://clawhub.ai/user/kyriswu)
- [Google web search API endpoint](https://coze-js-api.devtool.uk/google/search/web)
- [Devtool plugin documentation](https://devtool.uk/plugin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown search-result summary or raw JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns status information and result entries with title, link, and snippet when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
