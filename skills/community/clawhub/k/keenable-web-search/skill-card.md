## Description:

Keenable Web Search lets agents search the live web for current, citable information such as news, research papers, documentation, company research, and fact-checking sources through a bundled keyless Python script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keenable](https://clawhub.ai/user/keenable)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to gather current web references for research, news, fact-checking, company or market research, and documentation lookup. It is intended for web information retrieval, not local file operations or non-web tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and filters are sent to Keenable's public search service.

Mitigation: Avoid submitting secrets, private internal details, personal data, or regulated information unless Keenable's data handling has been reviewed for the use case.

Risk: Search snippets may be incomplete or misleading if used without checking the source page.

Mitigation: Open the most relevant result URL and cite the primary source before relying on a claim.

Risk: The public endpoint can rate limit requests.

Mitigation: Retry later or add backoff when automating repeated searches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keenable/skills/keenable-web-search)
- [Keenable homepage](https://keenable.ai)
- [Keenable public search endpoint](https://api.keenable.ai/v1/search/public)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Formatted text search results with titles, URLs, and snippets, or raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports natural-language queries plus optional site and date filters; no API key is required.]

## Skill Version(s):

1.1.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
