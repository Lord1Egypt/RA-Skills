## Description:

Merges patent CSV lists by complete publication number while preserving source rows, publication versions, field conflicts, and unresolved identifiers without inferring patent families.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Patent analysts and researchers can merge user-provided patent CSV lists into a traceable index, retaining source rows and flagging conflicts or identifiers that need review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conflicting instructions around online enrichment and spending could lead to data transmission or charges without clear approval.

Mitigation: Prefer offline merging; before online enrichment, explicitly approve the data to be sent and set a spending limit.

Risk: Weak trial-key storage could expose credentials.

Mitigation: Use a private credential location for any API key.

Risk: Source credits may not match the actual origin of records.

Mitigation: Verify that each source credit reflects where its record actually came from.

## Reference(s):

- [Deduplication format and matching rules](artifact/references/dedupe-format.md)
- [Search workflow](artifact/references/search-workflow.md)
- [API reference](artifact/references/api-reference.md)
- [Credential setup guidance](artifact/references/key-setup.md)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [CSV files, Text guidance]

**Output Format:** [UTF-8 with BOM CSV files and a concise handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retains original rows and source locations, records field conflicts and unresolved identifiers, and keeps A/B publication versions distinct.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
