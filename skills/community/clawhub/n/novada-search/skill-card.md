## Description:

AI Agent search platform with 9 engines, Google 13 sub-types, vertical scene search, and intelligent auto/multi/extract modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goldentrii](https://clawhub.ai/user/goldentrii)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to run multi-engine web search, vertical scene search, and URL content extraction through CLI, Python SDK, MCP, or LangChain interfaces. It is best suited for agent workflows that need structured search results such as agent-json, plus human-readable Markdown or table output when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, target URLs, and the Novada API key are sent to Novada services.

Mitigation: Avoid using this skill with private documents, intranet URLs, regulated data, or secrets in URLs; keep network permissions constrained to the declared Novada endpoint.

Risk: The action-links output format can produce shell command text from search results.

Mitigation: Prefer agent-json or normal link output for agent workflows, and review and sanitize every generated URL before running any action-link command.

Risk: Security evidence marks the release as suspicious because it performs real search/extraction calls and needs user review.

Mitigation: Run an initial validation in a sandbox with least-privilege environment variables and review outputs before integrating the skill into automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goldentrii/skills/novada-search)
- [Novada homepage](https://novada.com)
- [Novada Scraper API endpoint](https://scraperapi.novada.com)
- [PyPI package](https://pypi.org/project/novada-search/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON, Markdown, tables, raw API response, or shell command text depending on the selected output format]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NOVADA_API_KEY; agent-json includes unified_results, engine metadata, result counts, duplicate counts, and errors.]

## Skill Version(s):

1.0.8 (source: SKILL.md frontmatter, pyproject.toml, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
