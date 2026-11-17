## Description:

Litigation Hub helps agents process Chinese court delivery messages, court links, and document photos into OCR-assisted parsing, document download, case filing, deadline matching, calendar reminders, email notices, and local reminder files across macOS, Windows, and Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leahlu0124-creator](https://clawhub.ai/user/leahlu0124-creator)

### License/Terms of Use:

MIT

## Use Case:

External legal practitioners and their agents use this skill to triage court delivery SMS messages, court delivery URLs, and photographed court documents, then organize the resulting case materials and reminders. It is aimed at litigation document intake, filing, and deadline awareness rather than legal advice.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Confidential court data may pass through email, OCR, HTTP download, local archives, scheduled tasks, or generated desktop reminder files.

Mitigation: Review before installation, start with non-confidential test data, avoid plaintext HTTP court workflows where possible, and restrict or periodically clean local email, archive, scheduled-task, and reminder-file locations.

Risk: OCR, browser automation, email sending, and dependency installation can expose documents or alter the local environment.

Mitigation: Require explicit approval before OCR, email, browser automation, or dependency installation, and pin and locally install dependencies before use.

Risk: Court deadline and filing reminders may be incomplete or incorrect if source documents, OCR, or rules are wrong.

Mitigation: Treat generated reminders as workflow aids and have a legal professional verify case deadlines and filings before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leahlu0124-creator/skills/litigation-hub)
- [Publisher profile](https://clawhub.ai/user/leahlu0124-creator)
- [ClawHub metadata homepage](https://github.com/leahlu0124-creator/litigation-hub)
- [Attribution](references/ATTRIBUTION.md)
- [Archive format](references/archive-format.md)
- [Report format](references/report-format.md)
- [SMS patterns](references/sms-patterns.json)
- [Deadline rules](references/deadline-rules.json)
- [China holidays](references/china-holidays.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text guidance with shell commands and JSON configuration or archive records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local case archive records, downloaded documents, calendar entries, email notices, scheduled reminders, and desktop reminder files depending on the selected workflow.]

## Skill Version(s):

2.2.3 (source: frontmatter and changelog, released 2026-07-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
