## Description:

智能数据研究工作站 is a ClawHub bundle for multi-engine search, public web crawling, local archiving, incremental sync, and SQL-style analysis for data research workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Market researchers, data analysts, investment researchers, and academic researchers use this skill bundle to discover public information sources, crawl approved pages, archive findings locally, and run SQL-style analysis over collected text data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform web searches, crawl public pages, write local archives, and run scheduled sync jobs.

Mitigation: Install only for approved data research workflows, keep crawl scope limited to approved public sources, and review scheduled sync and notification settings before enabling them.

Risk: Search and crawling may trigger target-site anti-automation controls or violate site-specific access rules if configured aggressively.

Mitigation: Use conservative concurrency and rate limits, prefer public APIs when available, and follow robots.txt and site terms for the target sources.

Risk: Collected public data may still carry privacy, copyright, retention, or downstream-use obligations.

Mitigation: Review collected archives before redistribution or commercial use, apply local retention controls, and remove sensitive data discovered during analysis.

Risk: External search APIs and LLM services require credentials and may fail because of quota, regional availability, or provider configuration.

Mitigation: Provide credentials only through environment variables, monitor quota errors, and configure fallback engines where appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/plug-intelligent-data-research)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)
- [artifact/SKILL.md](artifact/SKILL.md)
- [artifact/plug.json](artifact/plug.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown and JSON responses with command snippets, configuration examples, search results, archive paths, SQL analysis summaries, and export file references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on network access, environment-provided API keys, local storage, crawler scheduling, and optional notification configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
