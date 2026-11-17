## Description:

Import ICS calendars, expand recurring events, inspect conflicts, create meeting files and transfer CalDAV resources with version checks. Use for Calendar and Agenda Desk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT-0

## Use Case:

Calendar users can import ICS data, review recurring agendas and conflicts, create event files, and manage CalDAV resources with version checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weak remote deletion safeguards could put a connected calendar at risk.

Mitigation: Use local calendar functions or a read-only connection until deletion rejects collection targets and wildcard version values; back up connected calendars before remote changes.

Risk: Connected calendar data and credentials may be sensitive.

Mitigation: Keep credentials and the .mochilab state directory private, and use reviewed installer and dependency versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-calendar-desk)
- [JSON actions reference](references/input.md)
- [MochiLab](https://mochilab.bz)

## Skill Output:

**Output Type(s):** [Text, JSON, ICS calendar files]

**Output Format:** [JSON results and ICS calendar files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agenda and conflict requests use an explicit time range with timezone offsets.]

## Skill Version(s):

1.0.1 (source: server-resolved release and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
