## Description:

Search the web for one or more queries in parallel. Use when you need current information, news, prices, or any web content to complement on-chain Nansen data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts can use this skill to search for current web information, news, and prices alongside on-chain Nansen data. It returns results for one or more queries in parallel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web search snippets may omit context or become outdated, especially for current news and prices.

Mitigation: Review the linked source and its date before relying on consequential or time-sensitive claims.

Risk: The CLI requires authenticated Nansen access through a browser session or API key.

Mitigation: Keep authentication in the CLI session or configured environment and avoid exposing credentials in queries or shared output.

## Reference(s):

- [Nansen Web Searcher on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-web-searcher)
- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Search results with titles, links, snippets, dates, and optional knowledge graph data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One result set per query; 1–20 results per query, defaulting to 10.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
