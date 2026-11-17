## Description:

Run multi-source evidence gathering with confidence scoring across web, academic, Tavily, and synthesis layers via AISA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and researchers use this skill to gather evidence-backed answers from multiple search sources when one search pass is not enough.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, requested URLs, and AISA API credentials are sent to AISA's API.

Mitigation: Avoid sensitive queries, private documents, secrets, and credential-related tasks unless external processing by AISA is acceptable.

Risk: The skill depends on an external AISA API key and network service.

Mitigation: Confirm AISA_API_KEY is configured and review API availability, account terms, and data-handling requirements before use.

## Reference(s):

- [AISA](https://aisa.one)
- [AISA API Base](https://api.aisa.one/apis/v1)
- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/multi-search-aisa)
- [Publisher profile](https://clawhub.ai/user/bibaofeng)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or terminal text with search results, citations, confidence scoring, and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; sends search queries and requested URLs to AISA.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
