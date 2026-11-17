## Description:

Multi-query research tool with LLM-ranked results and freshness control. Breaks a topic into focused queries, previews top results. No API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c5huracan](https://clawhub.ai/user/c5huracan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, external researchers, and agent users use this skill to break a research topic into focused queries, retrieve LLM-ranked web results, and preview selected results with configurable freshness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries, chosen agent_id values, and selected result URLs are transmitted to api.rhdxm.com.

Mitigation: Do not include secrets, private business information, proprietary research topics, or sensitive identifiers unless that external service is approved for the use case.

Risk: Search previews and LLM-ranked results can be incomplete, outdated, or misleading for decisions that require authoritative sources.

Mitigation: Review the linked source pages and corroborate important claims before using results in high-impact work.

## Reference(s):

- [Meyhem Researcher on ClawHub](https://clawhub.ai/c5huracan/skills/meyhem-researcher)
- [RHDXM API documentation](https://api.rhdxm.com/docs)
- [RHDXM MCP endpoint](https://api.rhdxm.com/mcp/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance and terminal text containing search queries, result titles, URLs, and short previews.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill sends search queries, an agent_id, and selected result URLs to api.rhdxm.com; no API key is required.]

## Skill Version(s):

0.2.5 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
