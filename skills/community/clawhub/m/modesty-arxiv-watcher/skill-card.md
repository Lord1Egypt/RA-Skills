## Description:

Search and summarize papers from ArXiv. Use when the user asks for the latest research, specific topics on ArXiv, or a daily summary of AI papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research analysts use this skill to find recent ArXiv papers by topic, author, or category and receive concise summaries with links for follow-up reading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist paper titles, authors, links, and summaries to memory/RESEARCH_LOG.md, which can expose sensitive research interests over time.

Mitigation: Ask the agent not to write memory for sensitive topics, or review and delete memory/RESEARCH_LOG.md after use.

Risk: The ArXiv search script accepts a raw query string and result count for an outbound API request.

Mitigation: Use URL-encoded queries and keep result counts bounded before running the script in automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/modestyrichards/skills/modesty-arxiv-watcher)
- [Complete setup guide](https://skillboss.co/skill.md)
- [ArXiv API query endpoint](https://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with paper metadata and links; XML results are fetched from the ArXiv API for parsing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append discussed paper metadata and summaries to memory/RESEARCH_LOG.md for long-term tracking.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
