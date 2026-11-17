## Description:

Hypertension Manager helps users record daily blood pressure, review same-day trends, receive general lifestyle guidance, manage relaxation audio use, and generate Markdown health reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hcrunner](https://clawhub.ai/user/hcrunner)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to log blood pressure readings, summarize same-day measurements, and create a Markdown report they can save themselves. It is for health tracking and general wellness guidance, not diagnosis, treatment, or prescription advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Blood-pressure classifications and relaxation audio suggestions could be mistaken for medical care.

Mitigation: Present the skill as a logging and general wellness aid only, keep medical disclaimers visible, and direct users to professional care for abnormal readings or health concerns.

Risk: The hard-coded third-party audio link may disclose browsing metadata and exposes users to unaudited medical content.

Mitigation: Warn users before opening the external audio resource and allow them to skip audio recommendations without affecting blood-pressure logging or reporting.

Risk: Local health-note writes and optional report files can contain sensitive health information.

Mitigation: Minimize stored data, keep records local, and remind users that saved reports are user-managed sensitive files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hcrunner/skills/hypertension-manager)
- [Blood Pressure Reference Standards](references/bp_reference.md)
- [Hypertension Audio Therapy Protocol](references/protocol.md)
- [Audio Link Reference](references/music.md)
- [Progress Report Template](assets/templates/progress_report.md)
- [Third-Party Audio Resource](https://myxt.com/link/738cba02-d41a-453a-99db-9be5545c1cd7)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports and conversational text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write same-day health notes locally and generate optional Markdown report files for user-managed storage.]

## Skill Version(s):

1.0.2 (source: server release metadata; skill frontmatter metadata.version is 0.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
