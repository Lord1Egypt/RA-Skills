## Description:

Offline Quiz Builder converts study materials or existing question banks into a static offline quiz website with adaptive review scheduling, error review, favorites, progress tracking, and optional daily reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hounextitem](https://clawhub.ai/user/hounextitem)

### License/Terms of Use:

MIT-0

## Use Case:

Learners, educators, and developers use this skill to turn notes, handouts, PDFs, spreadsheets, Word documents, or existing question banks into an offline browser-based quiz and review site. It is intended for local study workflows that need question generation or conversion, schema validation, static site generation, and reminder setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malicious paths or reminder setup may trigger local command execution through the quiz-opening helper.

Mitigation: Review the skill before installation, use trusted site paths only, and avoid enabling reminders until the helper uses shell-free subprocess calls.

Risk: Untrusted question-bank data may inject browser scripts into generated quiz sites.

Mitigation: Use trusted question-bank files and escape or strictly validate option keys before sharing or opening generated sites with untrusted data.

Risk: Study progress is stored in browser localStorage and can be lost or split if the site path, browser, or origin changes.

Mitigation: Open the generated site consistently through its file URL, avoid moving the site directory after use, and export data before clearing browser storage or changing browsers.

## Reference(s):

- [Question Schema](references/question-schema.md)
- [Material Ingestion](references/material-ingestion.md)
- [Automation Reminder](references/automation-reminder.md)
- [ClawHub Skill Page](https://clawhub.ai/hounextitem/skills/offline-quiz-builder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON question-bank data, local static-site files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local files for an offline quiz site and may configure a daily reminder when requested.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
