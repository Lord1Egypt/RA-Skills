## Description:

Fetches webpage content as clean Markdown through Jina AI Reader API and searches the web through Jina AI Search API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claudy-my-laudy](https://clawhub.ai/user/claudy-my-laudy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve readable page Markdown from URLs, extract web content for summarization or analysis, and run Jina-backed web searches with rich result content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested URLs, search terms, and any configured JINA_API_KEY are sent to Jina AI services.

Mitigation: Use the skill only when third-party processing is acceptable; avoid private internal URLs, token-bearing URLs, sensitive personal data, and confidential research queries.

Risk: Jina Search requires a JINA_API_KEY, so search workflows may fail when no key is configured.

Mitigation: Configure JINA_API_KEY for search usage or use an approved fallback search skill when a key is unavailable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/claudy-my-laudy/skills/jina-ai-skill)
- [Jina AI API Dashboard](https://jina.ai/api-dashboard)
- [Jina Reader API Endpoint](https://r.jina.ai/)
- [Jina Search API Endpoint](https://s.jina.ai/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or JSON responses, with shell command examples and Python script usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reader requests can strip images; search returns up to five results by default and can be trimmed with --results for JSON output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
