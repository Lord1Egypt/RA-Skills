## Description:

Searches market-wide financial news and related signals from natural-language questions, returning relevant news snippets for research workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenzisay](https://clawhub.ai/user/wenzisay)

### License/Terms of Use:

MIT-0

## Use Case:

Financial research users and agents use this skill to retrieve market news, public sentiment, industry updates, company news, and other financial information with natural-language queries and optional date ranges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a local plaintext API token and may expose tokens through shell history when configured on the command line.

Mitigation: Use a dedicated token with limited scope where possible, avoid pasting real tokens into chat or shell commands, restrict access to the local config file, and rotate any token previously entered through command-line history.

Risk: The configurable API base URL can send the configured token to an arbitrary endpoint.

Mitigation: Do not use --set-url unless the endpoint is fully trusted, and verify the configured base URL before running searches with a real token.

Risk: Financial-news results may be incomplete, stale, unavailable, or rejected by the upstream service.

Mitigation: Preserve returned titles, sources, summaries, and dates; do not fabricate missing financial information; and report upstream errors such as 401, 403, or 429 without retrying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wenzisay/skills/ifind-repilot-news-search)
- [Feiyan platform](https://repilot.51ifind.com/)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Guidance]

**Output Format:** [JSON API responses summarized as concise Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a locally configured auth token; accepts a natural-language query and optional start and end dates.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
