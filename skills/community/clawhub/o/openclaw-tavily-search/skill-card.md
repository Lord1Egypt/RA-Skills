## Description:

Search the public web through Tavily and return structured results with URLs and snippets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacky1n7](https://clawhub.ai/user/jacky1n7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover public web sources, retrieve structured search results, and support current-information lookup workflows. It is not intended for private, authenticated, or sensitive queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, domain filters, and the Tavily API key are sent to Tavily's API.

Mitigation: Use the skill only for public web search workflows and avoid private, authenticated, or sensitive queries.

Risk: Search result titles and snippets may be incomplete or unverified discovery data.

Mitigation: Open and verify relevant source pages before using results as evidence for factual claims.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jacky1n7/skills/openclaw-tavily-search)
- [Project Homepage](https://github.com/Jacky1n7/openclaw-skill-tavily-search)
- [Tavily Search API Endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON result contracts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include raw JSON, Brave-like JSON, or compact Markdown links with snippets.]

## Skill Version(s):

0.2.1 (source: server evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
