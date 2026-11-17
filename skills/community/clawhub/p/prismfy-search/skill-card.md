## Description:

Default web search for OpenClaw that uses Prismfy to search engines such as Google, Reddit, GitHub, arXiv, Hacker News, and others, with a bundled shell helper for search, quota checks, engine filters, time filters, and domain filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uroboros1205](https://clawhub.ai/user/uroboros1205)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to add live web search to OpenClaw, retrieve current search results, check Prismfy quota, and filter searches by engine, time range, domain, page, or language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad default-search behavior can send ordinary user requests to an external Prismfy service more often than users may expect.

Mitigation: Install only if Prismfy is acceptable as the default search provider, and narrow use to explicit search commands in stricter privacy environments.

Risk: Sensitive terms, secrets, private code, customer data, or confidential internal details may be exposed if included in requests that trigger search.

Mitigation: Avoid entering sensitive content in requests that may trigger search, and review intended queries before execution.

## Reference(s):

- [Prismfy homepage](https://prismfy.io)
- [ClawHub skill page](https://clawhub.ai/uroboros1205/skills/prismfy-search)
- [ClawHub publisher profile](https://clawhub.ai/user/uroboros1205)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with source links and inline shell commands; raw JSON is available from the helper script when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include title, URL, snippet, source engine, cache status, result count, and quota information when requested.]

## Skill Version(s):

1.3.8 (source: server release evidence; artifact frontmatter reports 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
