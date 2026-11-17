## Description:

Creates a one-page HTML dashboard and data table summarizing patent trends, applicants, regions, technology mix, patent types, and legal status for a selected technology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Patent and market analysts can use this skill to turn a technology or company patent search into a presentation-ready visual dashboard and accompanying data table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to PatentMax and may reveal confidential invention details.

Mitigation: Use non-sensitive search terms and omit unpublished invention details.

Risk: API credentials are stored locally, and paid patent-statistics calls can incur fees.

Mitigation: Review credential handling and use a restricted, low-balance API key.

Risk: Authenticated requests and cache-file handling warrant review before using a paid API key.

Mitigation: Prefer a version that restricts authenticated destinations and redirects and validates cache filenames.

## Reference(s):

- [PatentMax API reference](references/api-reference.md)
- [Patent search workflow](references/search-workflow.md)
- [Query construction guide](references/query-construction.md)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [ClawHub release](https://clawhub.ai/ip930/skills/patent-map)

## Skill Output:

**Output Type(s):** [HTML, CSV]

**Output Format:** [Self-contained HTML dashboard and CSV data table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The dashboard summarizes six patent-statistics dimensions and is designed for browser viewing and presentation screenshots.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
