## Description:

Daily automated briefings that fetch trending content via Google News RSS, summarize articles, and store summaries in memory for RAG retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dainash](https://clawhub.ai/user/dainash)

### License/Terms of Use:

MIT-0

## Use Case:

External users configure domains of interest so an agent can fetch Google News RSS items, summarize new articles into attributed Markdown, and store them in local memory for RAG retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured interest topics are sent to Google News when fetching RSS results.

Mitigation: Avoid sensitive or identifying topics in memory/clawforage/domains.md before running the skill.

Risk: Internet-derived summaries are stored in persistent local memory for future retrieval.

Mitigation: Review or delete files under memory/knowledge when fetched articles are suspicious, off-topic, or no longer appropriate for retrieval.

## Reference(s):

- [Knowledge Harvester on ClawHub](https://clawhub.ai/dainash/skills/knowledge-harvester)
- [dainash publisher profile](https://clawhub.ai/user/dainash)
- [Google News RSS search endpoint](https://news.google.com/rss/search)
- [InspireHub Labs](https://inspireehub.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files with YAML frontmatter and concise run summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq, curl, and bash; stores article summaries under memory/knowledge.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
