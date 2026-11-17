## Description:

AI-optimized web search via Tavily API proxy, providing concise and relevant results with options for deep or news-focused queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to run web or news searches and extract page content through AIsa's Tavily API proxy when they need concise external source material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and submitted URLs are sent to AIsa's API using AISA_API_KEY.

Mitigation: Do not use the skill with confidential prompts, private documents, presigned URLs, or internal-only links unless AIsa is approved for that data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aisadocs/skills/openclaw-aisa-web-search-tavily)
- [AIsa](https://aisa.one)
- [AIsa Marketplace](https://marketplace.aisa.one)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text emitted by Node.js command-line scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output includes an answer section when available and source snippets; result count is capped at 20.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
