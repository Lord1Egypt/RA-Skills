## Description:

Search news articles via NewsAPI with filtering by time windows, sources, domains, and languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hegghammer](https://clawhub.ai/user/hegghammer)

### License/Terms of Use:


## Use Case:

Developers, researchers, and analysts use this skill to search NewsAPI article and headline endpoints, filter by source, domain, language, country, category, and time window, and list available news sources for monitoring or research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill loads environment variables from ~/.openclaw/.env, which may expose unrelated secrets if that file contains more than the NewsAPI key.

Mitigation: Keep ~/.openclaw/.env limited to NEWSAPI_KEY for this skill, or provide the key through a scoped environment when running the scripts.

Risk: NewsAPI request URLs include the API key as a query parameter and may be captured by tools that log full URLs.

Mitigation: Avoid routing requests through logging proxies or shell wrappers that record URLs unless apiKey values are redacted.

Risk: News search results may include incomplete, outdated, or low-quality reporting from the selected sources.

Mitigation: Use source, domain, exclusion, date, and language filters, and verify important claims against the linked publisher pages before relying on results.

## Reference(s):

- [NewsAPI](https://newsapi.org)
- [NewsAPI Parameter Reference](references/api-reference.md)
- [NewsAPI Search Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JavaScript examples; runtime scripts return JSON article, headline, or source data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a NEWSAPI_KEY in the user's environment or ~/.openclaw/.env; NewsAPI free-tier and endpoint constraints apply.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
