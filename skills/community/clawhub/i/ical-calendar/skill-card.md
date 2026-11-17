## Description:

Query `.ics` calendar files, raw iCal strings, or remote iCal feeds with the local `icali` CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[docmarionum1](https://clawhub.ai/user/docmarionum1)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to answer natural-language questions over user-provided iCal calendar files, raw iCal text, or remote iCal feeds. It helps agents translate calendar questions into `icali` queries, then summarize matching events clearly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar files and feed URLs can contain sensitive personal or business scheduling data.

Mitigation: Install only where agents are allowed to inspect user-provided calendar data, and avoid exposing raw event details beyond what is needed to answer the request.

Risk: Ambiguous calendar sources or timezones can produce incorrect date-window answers.

Mitigation: Confirm the `.ics` path, feed URL, or raw iCal text and the relevant timezone before lookup when either is unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/docmarionum1/skills/ical-calendar)
- [iCaLI CLI homepage](https://github.com/docmarionum1/iCaLI)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown prose with inline bash command examples and JSON-derived calendar summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calendar answers should state the interpreted date or datetime window, identify whether cancelled items were excluded, and summarize matching events in chronological order.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
