## Description:

Meeting Load Balancer audits exported ICS calendars to measure meeting load, focus fragmentation, series cost, and rule-based opportunities to kill, shorten, batch, or move meetings async.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Employees, managers, team leads, consultants, and other external users use this skill to audit personal or team calendar exports, quantify meeting hours and focus-time loss, and prepare evidence-based meeting reduction proposals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted calendar content may be printed to a terminal without escaping control characters.

Mitigation: Use ICS files from trusted sources, avoid permissive terminals for untrusted calendar data, and prefer a patched version that escapes event titles, attendee names, filenames, and other ICS-derived text before printing.

Risk: Calendar exports can contain sensitive meeting titles, names, email addresses, and attendee relationships.

Mitigation: Keep exports local and access-controlled, collect team exports only with consent, share aggregate results where possible, and delete or securely store ICS files after the audit.

## Reference(s):

- [ICS Export How-To + Meeting Audit Methodology](references/ics-export.md)
- [ClawHub Skill Page](https://clawhub.ai/voronindenis5/skills/meeting-load-balancer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local analysis output from Python commands over user-supplied ICS calendar files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
