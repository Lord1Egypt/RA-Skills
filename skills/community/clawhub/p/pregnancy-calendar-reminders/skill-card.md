## Description:

Generates, verifies, updates, and helps import pregnancy reminder calendars from a last menstrual period date or doctor-adjusted due date, including daily reminders, key prenatal windows, .ics files, outlines, and validation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[5fivelogistic-cell](https://clawhub.ai/user/5fivelogistic-cell)

### License/Terms of Use:

MIT-0

## Use Case:

External users and caregivers use this skill through an agent to create checked pregnancy reminder calendars from LMP or doctor-adjusted due dates, then import the resulting reminders into Apple Calendar, iCloud, or compatible calendar tools. It supports planning and appointment preparation, not diagnosis or individualized medical care.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted output filename prefix could cause generated files to be written outside the intended output folder.

Mitigation: Use only trusted arguments, keep --output-dir in a disposable folder, avoid custom --prefix values, and review the generated file paths before opening or importing outputs.

Risk: Pregnancy reminders could be mistaken for diagnosis, prescriptions, or individualized hospital instructions.

Mitigation: Present the calendar as family planning and appointment-preparation support, defer clinical decisions to obstetric professionals, and advise timely medical contact for danger symptoms.

Risk: Incorrect LMP, due-date, or calendar-range inputs can produce misleading reminder dates.

Mitigation: Prefer doctor-adjusted due dates when provided, record the active LMP anchor and due date, and confirm the validation report passes before delivering calendar files.

## Reference(s):

- [Pregnancy Reminder Rules](artifact/references/pregnancy_rules.md)
- [Skill README](artifact/README.md)

## Skill Output:

**Output Type(s):** [files, json, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance plus generated .ics, JSON, outline Markdown, and validation JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated calendars should be validated before delivery and written to a trusted output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
