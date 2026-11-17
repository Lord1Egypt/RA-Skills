## Description:

Ticket Tailor (tickettailor.com). Use this skill for ANY Ticket Tailor request — searching and reading data. Whenever a task involves Ticket Tailor, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using a connected Ticket Tailor account can retrieve event, issued ticket, and order information. The skill supports listing these records and retrieving individual records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs users to run remote installers whose contents have not been verified.

Mitigation: Verify the CLI release independently and review the installer; require user approval before running it.

Risk: The CLI may synchronize skills automatically, and the hosted connector implementation is unverified.

Mitigation: Review the CLI's synchronization behavior and authorize only the Ticket Tailor data access needed through OOMOL.

## Reference(s):

- [Ticket Tailor skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-ticket-tailor)
- [Ticket Tailor](https://www.tickettailor.com/)
- [Ticket Tailor API documentation](https://developers.tickettailor.com/docs/api/ticket-tailor-api/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON]

**Output Format:** [oo CLI commands with JSON payloads and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only event, issued ticket, and order data from the connected Ticket Tailor account.]

## Skill Version(s):

1.0.2 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
