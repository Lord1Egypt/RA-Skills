## Description:

Checks iCalendar (.ics) files against RFC 5545 and documented Google, Outlook, and Apple Calendar import behavior, reporting sourced findings without modifying files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and calendar maintainers can validate iCalendar files, investigate calendar import failures, and check calendar files in CI using findings tied to RFC 5545 or named importer sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation uses pip to fetch a Git-hosted package, and scan coverage is incomplete because a referenced example file was missing.

Mitigation: Review the package source before installing and inspect the missing example file when it is available.

## Reference(s):

- [RFC 5545: Internet Calendaring and Scheduling Core Object Specification](https://www.rfc-editor.org/rfc/rfc5545)
- [icslint source repository](https://github.com/RakTikoo/icslint)
- [ICS Lint on ClawHub](https://clawhub.ai/raktikoo/skills/icslint)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Line-based findings or JSON findings, with file, line, component, rule ID, severity, explanation, and source]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports findings without editing or converting input files.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
