## Description:

Collect weekly reports from Lark Reports (oa.larksuite.com), summarize into Lark Docs, and notify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengxiao-wang](https://clawhub.ai/user/pengxiao-wang)

### License/Terms of Use:


## Use Case:

Employees, managers, and operations teams use this skill to collect weekly reports for specific Lark teams or templates, identify missing submissions, summarize submitted reports into Lark Docs, and notify recipients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles employee report data from Lark workplace reports.

Mitigation: Use it only after confirming the exact team, report template, and week to collect.

Risk: The skill may write report data to an unspecified temporary local file.

Mitigation: Confirm the local file path before use and delete temporary report data after the summary workflow is complete.

Risk: Generated Lark Docs and notifications may expose report summaries to unintended recipients.

Mitigation: Confirm the Lark Doc audience and notification recipients before creating or sending outputs.

## Reference(s):

- [Lark Reports entry page](https://oa.larksuite.com/report/record/entry)
- [ClawHub skill page](https://clawhub.ai/pengxiao-wang/skills/lark-report-collector)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with browser automation commands, JavaScript snippets, API instructions, and report-summary content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local report data file and Lark Docs output before notification.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
