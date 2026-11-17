## Description:

Provides date and time manipulation operations for formatting, parsing, comparing, and manipulating dates and times.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to format, parse, compare, and manipulate dates and times in JavaScript workflows, including date arithmetic, calendars, relative time, duration calculations, and basic timezone offset handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Timezone-sensitive ISO timestamp output may be mistaken for a standard UTC ISO string.

Mitigation: Review toISOString behavior before relying on it for logs, audit records, or API timestamps; use native Date.toISOString or an explicit timezone-aware formatter when UTC semantics are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-date-utils)
- [artifact/SKILL.md](artifact/SKILL.md)
- [artifact/package.json](artifact/package.json)

## Skill Output:

**Output Type(s):** [code, guidance]

**Output Format:** [JavaScript module exports with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local date and time utility behavior; no hidden access, persistence, network activity, or destructive behavior identified in security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
