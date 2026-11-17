## Description:

Uses ideamake-cli to pull Marketing Cloud data and generate full monthly real-estate visitor analysis reports as HTML and PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crespoyin](https://clawhub.ai/user/crespoyin)

### License/Terms of Use:

MIT-0

## Use Case:

Real-estate sales and marketing teams use this skill to generate monthly management reports from project details, customer records, visit recordings, transcript analysis, competitor mentions, consultant performance, and conversion signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can download and store sensitive customer transcripts, identifiers, and CRM-derived records.

Mitigation: Install only in an approved business environment, confirm authorization before accessing customer recordings or CRM data, and write outputs to encrypted, access-controlled storage.

Risk: Generated reports may expose names, contact details, or sensitive customer quotes if shared broadly.

Mitigation: Redact names, contact details, and sensitive quotes before distribution, avoid broad sync or sharing of transcript folders, and apply a clear retention policy.

Risk: Embedded examples or previous report values could be copied into a new report if metrics are not recalculated.

Mitigation: Verify that all report metrics are recalculated from the selected month and source records before using the report for business decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crespoyin/skills/mc-monthly-visitor-report)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; produced artifacts include Markdown files, transcript text files, HTML reports, and PDF reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated ideamake-cli setup and the onepage-pdf skill; generated outputs may contain customer transcripts and identifiers.]

## Skill Version(s):

0.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
