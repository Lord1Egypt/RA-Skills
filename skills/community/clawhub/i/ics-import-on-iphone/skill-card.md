## Description:

Creates RFC 5545-compliant .ics files for calendar events when direct calendar access is unavailable, with optional iPhone and iPad import guidance when .ics delivery is used.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sbhhbs](https://clawhub.ai/user/sbhhbs)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to create calendar events by collecting event details and producing a standards-compliant .ics file when direct calendar access is unavailable. On iPhone or iPad, it can provide optional Catendar import guidance only when the event is delivered as an .ics file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may recommend a specific iOS app for importing .ics files.

Mitigation: Present Catendar as optional guidance and allow users to use native calendar import options or another preferred app.

Risk: Incorrect date, timezone, escaping, or line-folding details can produce inaccurate calendar events or invalid .ics files.

Mitigation: Validate required RFC 5545 structure, date and timezone formatting, escaped text values, and folded long lines before sending the file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sbhhbs/skills/ics-import-on-iphone)
- [Catendar App Store listing](https://apps.apple.com/us/app/catendar-import-ics/id6753041569)

## Skill Output:

**Output Type(s):** [Files, Text, Guidance]

**Output Format:** [RFC 5545 .ics calendar content with optional Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires event title, start datetime with timezone, end datetime or duration, and all-day status; may include optional location, description, and URL.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
