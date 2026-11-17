## Description:

Finds a company's patent-applicant name variants, counts their patent records, and builds a consolidated applicant search query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, IP researchers, and patent analysts use this skill to identify applicant-name variants for a company, including subsidiaries and former or English names, and assemble a broader patent search query.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential routing and cache-path handling need review before using a paid key or running alongside sensitive files.

Mitigation: Use only after the publisher addresses credential routing and validates cache paths; avoid paid keys and sensitive-file co-location until then.

Risk: Searches are sent to PatentMax and may incur charges.

Mitigation: Explain the expected cost and obtain authorization before making paid searches.

Risk: Applicant statistics return only the top 20 names, so the list may be incomplete.

Mitigation: Present the results as a limited candidate list and cross-check before treating it as exhaustive.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ip930/skills/patent-applicant-names)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [API reference](artifact/references/api-reference.md)
- [Search workflow](artifact/references/search-workflow.md)
- [Query syntax](artifact/references/query-syntax.md)

## Skill Output:

**Output Type(s):** [text, CSV, search query]

**Output Format:** [UTF-8 CSV applicant-name table and a copyable applicant search query, with a concise summary in the conversation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The table includes applicant-name categories, patent counts, and whether each name is included in the query. Statistics return up to 20 names per dimension.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
