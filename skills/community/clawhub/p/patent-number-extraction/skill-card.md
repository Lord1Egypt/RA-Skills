## Description:

Extract patent-number candidates from supplied text with their original spelling, source locations, and context, while distinguishing publication candidates from Chinese application-number candidates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External users and patent researchers can extract patent-number candidates from supplied text or CSV and trace each occurrence to its source location. The local workflow identifies format candidates; it does not establish whether a patent number is authentic or valid.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional online client transmits patent identifiers and may incur charges.

Mitigation: Before online use, approve the identifiers to be sent and set a spending limit.

Risk: Spreadsheet software may interpret exported CSV cells as formulas.

Mitigation: Import candidate CSV files as plain text until the export handling issue is fixed.

Risk: The optional online client has incomplete credential-storage safeguards.

Mitigation: Prefer offline extraction; for online use, use a process-only API key.

## Reference(s):

- [Local workflow and format limits](references/local-workflow.md)
- [PatentMax API reference](references/api-reference.md)
- [PatentMax platform and account](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [Files, CSV, JSON, Text]

**Output Format:** [CSV occurrence table and index, with JSON details and concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves repeated occurrences and source positions; candidate formats are not validity checks.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
