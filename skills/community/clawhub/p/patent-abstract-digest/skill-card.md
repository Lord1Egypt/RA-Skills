## Description:

Turns supplied patent numbers or search results into a topic-grouped digest with source abstracts, short reading guides, and an index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, researchers, and external users can turn a supplied patent list or search results into a grouped reading packet that preserves source abstracts and links each entry to its publication number.

### Deployment Geography for Use:

Global; documented patent coverage includes China, the United States, Europe, Japan, Korea, and WIPO.

## Known Risks and Mitigations:

Risk: Patent identifiers and search terms are sent to PatentMax during online lookups.

Mitigation: Avoid sending confidential invention details unless their disclosure is approved.

Risk: Batch lookup activity may incur usage charges.

Mitigation: Set a spending cap and review the service-reported usage before large batches.

Risk: A personal API credential may be stored in a local cache for persistent access.

Mitigation: Keep the credential cache private and save a personal key only when persistent access is wanted.

## Reference(s):

- [Search workflow](artifact/references/search-workflow.md)
- [Query syntax](artifact/references/query-syntax.md)
- [API reference](artifact/references/api-reference.md)
- [Credential setup](artifact/references/key-setup.md)
- [PatentMax](https://ip930.com)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV files]

**Output Format:** [UTF-8 CSV and Markdown digest with source abstracts, reading guides, topic groups, and an index]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source abstracts and publication-number links; summaries are based on supplied materials or returned patent data.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
