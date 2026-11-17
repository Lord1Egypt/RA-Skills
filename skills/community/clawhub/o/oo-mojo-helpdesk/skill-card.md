## Description:

Use Mojo Helpdesk to read, search, create, and update tickets and comments through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Helpdesk agents and support staff use this skill to retrieve and search tickets, inspect comments and queues, and create or update tickets and comments in their connected Mojo Helpdesk account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unverified remote code without clear explanation or approval of local changes.

Mitigation: Install the CLI from a verified release and review its installation and synchronization behavior before setup; retain confirmation requirements for public comments and ticket changes.

## Reference(s):

- [Mojo Helpdesk](https://www.mojohelpdesk.com/)
- [Mojo Helpdesk API documentation](https://developer.mojohelpdesk.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON responses with concise task results and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions include read operations and ticket or comment changes; write and destructive actions require confirmation as described in the skill.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
