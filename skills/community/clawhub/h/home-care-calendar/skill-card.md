## Description:

Home Care Calendar helps homeowners, renters, and landlords build a local home-maintenance inventory, generate seasonal task calendars, track completion, export ICS calendar files, and estimate deferred-maintenance debt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to maintain homes, apartments, or rental properties by recording maintainable systems, reviewing due and overdue maintenance tasks, exporting tasks to a calendar app, and prioritizing overdue work by estimated neglect cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local JSON state can contain home inventory, install dates, notes, and maintenance history.

Mitigation: Keep the generated state file in a trusted local location and avoid recording sensitive notes that are not needed for maintenance.

Risk: ICS exports can expose household maintenance details when imported into shared or third-party calendars.

Mitigation: Choose the ICS output path intentionally, review event descriptions before importing, and avoid sharing calendars that contain sensitive home details.

Risk: Maintenance intervals and deferred-cost estimates are planning aids, not emergency repair or professional inspection substitutes.

Mitigation: Use licensed professionals for emergency repairs, structural issues, gas-line work, and other tasks marked as professional work.

## Reference(s):

- [Task Library & Maintenance Intervals](references/task-library.md)
- [ClawHub skill page](https://clawhub.ai/voronindenis5/skills/home-care-calendar)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown-style agent guidance, plain text CLI reports, optional JSON calendar output, and ICS calendar files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON state for home inventory and completion history; ICS exports may contain household details and should be shared carefully.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
