## Description:

Check, monitor, and summarize student homework and tasks from Webtop (SmartSchool), Galim Pro, and Ofek across pending work, submission status, due items, and daily school updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaike1](https://clawhub.ai/user/shaike1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect student homework status, summarize urgent or overdue work in Hebrew, and maintain local automation for family school-task updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles children's school credentials and student task data.

Mitigation: Use dedicated least-privilege school and calendar credentials, keep environment files private with chmod 600, and avoid broadly shared target calendars.

Risk: Calendar sync can write student task details to an external calendar.

Mitigation: Preview sync with --dry-run and confirm the target calendar before allowing writes.

Risk: Credential loading can be unsafe if WEBTOP_GALIM_ENV points to an untrusted file.

Mitigation: Only use trusted local env files and review the selected file before sourcing or executing the wrapper.

Risk: The Webtop path relies on an external pywebtop script boundary.

Mitigation: Audit or remove the external pywebtop dependency before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaike1/skills/ofek-galim)
- [Environment credentials format](references/env-example.md)
- [Ofek student portal](https://students.myofek.cet.ac.il/he)
- [Galim Pro tasks page](https://lms.galim.org.il/personal?lang=he)
- [Google Calendar API endpoint](https://www.googleapis.com/calendar/v3)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Hebrew text or Markdown summaries, JSON task reports, shell commands, and calendar-sync status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create Google Calendar events during calendar sync; otherwise prints task reports and setup guidance to stdout.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
