## Description:

Access Finnish sports club events, invoices, notifications, and RSVP on myclub.fi for AI agents and parents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jannemakela](https://clawhub.ai/user/jannemakela)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve family sports club schedules, RSVP status, invoices, notifications, participant lists, and calendar subscriptions from myclub.fi.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a mutable npm CLI that handles myclub.fi account credentials.

Mitigation: Install only from a trusted publisher, prefer a pinned or audited CLI version, avoid elevated privileges, and clear stored credentials when no longer needed.

Risk: Skill outputs can contain sensitive family, club, invoice, and attendance information.

Mitigation: Treat command output as private data and avoid sharing it outside the intended family or club context.

Risk: The wrapper script can fall back to a local build path outside the packaged skill boundary.

Mitigation: Review the installed wrapper and local filesystem fallback before enabling the skill in an agent environment.

## Reference(s):

- [Maiklubi Skill on ClawHub](https://clawhub.ai/jannemakela/skills/maiklubi-myclub)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Text, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the maiklubi CLI and may surface sensitive family and club information.]

## Skill Version(s):

1.2.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
