## Description:

Checks supplied patent CSV tables for missing fields, publication-number format issues, date precision, chronology, and duplicate identifiers without changing source records or treating table checks as authenticity verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Patent data managers and analysts can check supplied CSVs before import or delivery, review row-level issues and original values, and preserve records for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional online enrichment may send information to the service and incur charges.

Mitigation: Approve the information to be sent and set a spending limit before requesting online lookups.

Risk: Cached API credentials could be exposed if stored insecurely.

Mitigation: Keep the PatentMax cache private and prefer temporary use of a key.

## Reference(s):

- [Local patent table checks](references/local-workflow.md)
- [Key setup and storage guidance](references/key-setup.md)
- [PatentMax API Platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [CSV, JSON, Guidance]

**Output Format:** [CSV issue list and record details, JSON summary statistics, and concise review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves original values for review; checks do not verify patent authenticity or legal status.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
