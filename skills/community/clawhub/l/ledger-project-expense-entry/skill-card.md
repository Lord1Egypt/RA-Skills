## Description:

Record short natural-language project expense messages into local ledger JSONL entries, defaulting to expense and CNY unless the user specifies otherwise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shing19](https://clawhub.ai/user/shing19)

### License/Terms of Use:

MIT-0

## Use Case:

Users maintaining project expense ledgers use this skill to parse short expense messages, choose ledger fields and tags, and append an entry through the existing ledger script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write persistent ledger records from short natural-language messages.

Mitigation: Require the agent to show the parsed date, amount, currency, description, and tags before writing real records.

Risk: User-provided fields could be unsafe if interpolated into shell commands.

Mitigation: Invoke the ledger script with structured arguments rather than an interpolated shell command.

Risk: The default date uses the Asia/Taipei timezone.

Mitigation: Confirm that Asia/Taipei is the intended date basis before relying on default dates.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Files, Guidance]

**Output Format:** [Markdown with shell command guidance and a one-line ledger-entry summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append persistent ledger JSONL records through the configured ledger script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
