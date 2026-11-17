## Description:

Researches public holidays, bank holidays, observed days, school breaks, and make-up workdays for a specified country, region, year, and holiday type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to answer holiday and closure questions by resolving the jurisdiction, year, and holiday type before checking authoritative sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Holiday answers can be wrong or misleading when the country, region, year, or closure type is ambiguous.

Mitigation: Confirm the jurisdiction, year, and whether the user means a public holiday, bank holiday, school break, market closure, or company-specific closure before answering.

Risk: Holiday schedules are time-sensitive and may differ between official holidays, observed substitute days, and institution-specific closures.

Mitigation: Use authoritative government, official gazette, central bank, education, or institution calendars, and state the exact date, scope, and source basis in the answer.

## Reference(s):

- [Holiday Query Patterns](references/query-patterns.md)
- [Holiday Source Guidelines](references/source-guidelines.md)
- [ClawHub Skill Page](https://clawhub.ai/jvy/skills/holiday)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with optional shell commands and JSON checklist output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jurisdiction, year, and holiday type to produce reliable answers.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
