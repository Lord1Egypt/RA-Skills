## Description:

Web search and URL fetching via Perplexity (default: sonar, optional: sonar-pro).

This skill is ready for commercial/non-commercial use.

## Publisher:

[aligurelli](https://clawhub.ai/user/aligurelli)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to search the web, fetch URL content as markdown or text, and configure Perplexity-backed web search with their own API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Perplexity under the user's own API key and account terms.

Mitigation: Avoid including secrets, private documents, or sensitive personal data in web_search queries.

Risk: Web search answers and fetched page content can be incomplete, stale, or misleading.

Mitigation: Review returned citations and source content before relying on the result for consequential decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aligurelli/skills/perplexity-web-search)
- [Perplexity API key settings](https://www.perplexity.ai/settings/api)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or text responses with citations, fetched page content, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search queries are sent to Perplexity; fetched page extraction is described as local to OpenClaw.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
