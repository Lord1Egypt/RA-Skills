## Description:

Uses the Tavily API to perform web search, page extraction, crawling, site mapping, and research, with the agent selecting the mode that fits the task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[343195246](https://clawhub.ai/user/343195246)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to call Tavily for web search, page extraction, site crawling, site mapping, and research workflows that need current web information or retrieved page content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, URLs, and retrieved page content are sent to Tavily as a third-party service.

Mitigation: Avoid sending confidential queries, private URLs, authenticated pages, or sensitive business data unless approved for that use.

Risk: Crawl and map modes can retrieve multiple pages from a target site.

Mitigation: Use crawl and map only on targets you are authorized to access, and keep scope limits appropriate for the task.

## Reference(s):

- [Tavily](https://tavily.com)
- [Tavily Documentation](https://docs.tavily.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples; script output is plain text derived from Tavily API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY and the @tavily/core package; external calls go to Tavily.]

## Skill Version(s):

1.0.0 (source: release metadata, changelog, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
