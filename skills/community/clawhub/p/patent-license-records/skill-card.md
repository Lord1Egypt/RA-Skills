## Description:

Search public patent license recordation events for specified patents and summarize only information returned by the data source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External patent researchers, professionals, and businesses can check specified patents for publicly disclosed license recordation events and organize returned details. The skill does not determine whether an unrecorded contract exists or whether a license remains legally effective.

### Deployment Geography for Use:

Global; source coverage includes China, the United States, Europe, Japan, South Korea, and WIPO, subject to database coverage.

## Known Risks and Mitigations:

Risk: Patent identifiers and search terms are sent to PatentMax when queries run.

Mitigation: Submit only identifiers and search terms appropriate to send to the service.

Risk: Batch queries and legal event lookups may incur charges.

Mitigation: Confirm current prices, free allowance, and account balance before batching; keep the requested scope bounded.

Risk: A trial credential is cached locally, and a paid credential can be saved locally by choice.

Mitigation: Keep the credential directory private and save a paid key only when intended; use a temporary key for one-time work.

Risk: Database records may omit events or lack enough detail to establish a license's legal status.

Mitigation: Mark missing information as not returned and verify important conclusions against official records.

## Reference(s):

- [Legal event review guidance](references/legal-event-review.md)
- [Search workflow](references/search-workflow.md)
- [PatentMax API reference](references/api-reference.md)
- [Key setup and security](references/key-setup.md)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [PatentMax](https://ip930.com)

## Skill Output:

**Output Type(s):** [CSV files, JSON files, Text guidance]

**Output Format:** [UTF-8 CSV record table with JSON evidence files and a concise Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One row per returned event; unavailable fields are marked explicitly, and no facts are inferred beyond the data source.]

## Skill Version(s):

1.0.2 (source: server-resolved release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
