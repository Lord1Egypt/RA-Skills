## Description:

Syncs local Markdown data files to Google Sheets with dedup hashing for expenses, investments, and other key-value data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hohobohan](https://clawhub.ai/user/hohobohan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to parse local Markdown ledger-style records, deduplicate them against existing Google Sheets rows, and append only new expense or investment entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sync flow depends on a local Google service-account JSON credential.

Mitigation: Use a least-privilege service account and avoid logging, copying, or exposing the credential file.

Risk: Recurring scheduled writes can append data to the wrong spreadsheet or run more broadly than intended.

Mitigation: Confirm the spreadsheet destination, cron schedule, and narrowly defined source Markdown files before installation.

Risk: Parsed local Markdown records may create unintended Google Sheets rows if the input files are stale or malformed.

Mitigation: Review the source files and deduplication key behavior before enabling append-only sync.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with regex examples, API notes, and cron-oriented sync instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Append-only Google Sheets sync pattern using deduplication keys and local service-account credentials]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
