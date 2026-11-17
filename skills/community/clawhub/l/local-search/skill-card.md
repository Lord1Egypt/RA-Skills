## Description:

Local Search lets an agent query public web search engines from the user's machine and return structured search results with source engine, snippets, dates, rankings, and optional raw HTML or score fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sakurakilove](https://clawhub.ai/user/sakurakilove)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to retrieve current public web information, fact-check claims, discover source material, and gather recent documentation or news without using a hosted search SDK.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may contain confidential project names, incidents, internal URLs, or personal data and can be sent directly to external search engines.

Mitigation: Review queries before use and avoid submitting confidential or personal data to public search providers.

Risk: The default automatic search path may contact Brave before DuckDuckGo, Bing, or Google, which can surprise users who expect a different provider order.

Mitigation: Choose a specific engine explicitly when provider control, policy compliance, or data handling expectations matter.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/sakurakilove/skills/local-search)
- [Publisher profile](https://clawhub.ai/user/sakurakilove)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result objects include url, name, snippet, host_name, rank, date, favicon, source_engine, and optional raw_html or score fields.]

## Skill Version(s):

1.6.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
