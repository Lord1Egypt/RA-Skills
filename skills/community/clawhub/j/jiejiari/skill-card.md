## Description:

Looks up official 2026 Mainland China public holiday schedules and make-up workdays from bundled reference data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Mainland China 2026 public-holiday, make-up-workday, and festival break questions with exact dates. It is not intended for calendar event management, reminders, non-China holiday calendars, or years not included in the bundled data.

### Deployment Geography for Use:

Global; content is limited to Mainland China 2026 public-holiday arrangements.

## Known Risks and Mitigations:

Risk: The skill may be used for years or regions outside its bundled data.

Mitigation: State that only 2026 Mainland China public-holiday and make-up-workday data is included when a request is out of scope.

Risk: Users may confuse lunar festival dates with official holiday and make-up-workday arrangements.

Mitigation: Separate festival-date questions from official holiday schedule answers and use only the bundled reference data for official arrangements.

## Reference(s):

- [cn-holidays-2026.json](references/cn-holidays-2026.json)
- [ClawHub skill page](https://clawhub.ai/jvy/skills/jiejiari)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Plain text or Markdown answers, with optional JSON from the bundled CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers are limited to bundled 2026 Mainland China data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
