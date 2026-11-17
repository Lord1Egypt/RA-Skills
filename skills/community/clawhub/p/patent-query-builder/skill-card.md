## Description:

Builds broad, medium, and narrow patent search queries from technical descriptions, expands Chinese and English synonyms, and checks each query against the PatentMax database for hit counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Patent researchers and product teams use this skill to turn a technical topic into synonym-expanded patent search queries, compare broad, medium, and narrow strategies, and review observed hit counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API key transmission and storage practices warrant review.

Mitigation: Before using a paid key, verify HTTPS destinations and safe redirect handling; store credentials privately and provide a clear removal process.

Risk: Remote searches may expose confidential invention details or exceed the intended spend.

Mitigation: Generalize confidential details before remote searches and agree on a spending limit.

## Reference(s):

- [Query syntax](references/query-syntax.md)
- [Search workflow](references/search-workflow.md)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [ClawHub release](https://clawhub.ai/ip930/skills/patent-query-builder)

## Skill Output:

**Output Type(s):** [Text, Analysis, CSV files]

**Output Format:** [Markdown response with a UTF-8 CSV query plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes broad, medium, and narrow queries with observed database hit counts and relevance checks.]

## Skill Version(s):

1.0.1 (source: frontmatter; server release 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
