## Description:

Standardized literature search workflow integrating tavily-search, pubmed-database, bgpt-paper-search, openalex-database and other academic search skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earthwalking](https://clawhub.ai/user/earthwalking)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and academic assistants use this skill to run a staged literature-search workflow that analyzes a query, searches academic and web sources, organizes results, retrieves full text when available, and produces a structured report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A bundled hard-coded Tavily credential could be exposed or reused unintentionally.

Mitigation: Remove the embedded credential, rotate it, and require users to provide TAVILY_API_KEY through their own secret-management process.

Risk: Search queries and result retrieval are sent to external services, which may disclose research topics or sensitive query text.

Mitigation: Document the external Tavily API behavior and advise users to avoid confidential, regulated, or unpublished research content unless approved.

Risk: The documentation lists several academic search providers, while the bundled script directly implements Tavily and leaves other providers as optional placeholders.

Mitigation: Align the public documentation with the actual implementation and clearly separate implemented behavior from optional integrations.

Risk: Broad keyword triggers could activate the skill for generic literature-search phrases.

Mitigation: Narrow trigger terms or require explicit user confirmation before running external searches.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/earthwalking/skills/literature-search-workflow)
- [Publisher Profile](https://clawhub.ai/user/earthwalking)
- [PubMed Central Example Source](https://pmc.ncbi.nlm.nih.gov/articles/PMC4107280/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with citations, source links, DOI fields, full-text links, and optional BibTeX entries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes timestamped literature_search_*.md report files when the bundled script is run.]

## Skill Version(s):

1.0.0 (source: server release evidence, openclaw.skill.json, SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
