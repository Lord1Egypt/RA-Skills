## Description:

Convert natural-language spending or income statements into ledger JSONL records and append them into projects/data/YYYY/YYYY-MM.jsonl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shing19](https://clawhub.ai/user/shing19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers or maintainers of a ledger project use this skill to convert natural-language transaction requests into structured ledger entries. It also supports monthly aggregation and chart generation from existing ledger JSONL files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify ledger data files, report files, and possibly .gitignore.

Mitigation: Use it only in ledger projects where changes to projects/data, projects/reports, and .gitignore are expected, and review file paths before writes.

Risk: Raw user text could be unsafe if pasted directly into shell command arguments.

Mitigation: Pass arguments safely, with explicit quoting or validation, before executing write commands.

Risk: Incorrect transaction parsing can create inaccurate ledger records.

Mitigation: Confirm ambiguous amount, direction, date, currency, description, or tag values before appending a record.

Risk: Monthly totals can be misleading when source data includes multiple currencies.

Mitigation: State when totals are mixed-currency trend values or convert values to a single base currency before presenting totals.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown responses with shell commands and file outputs such as JSONL ledger records and PNG summary charts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Appends records to monthly JSONL files under projects/data and may generate report charts under projects/reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
