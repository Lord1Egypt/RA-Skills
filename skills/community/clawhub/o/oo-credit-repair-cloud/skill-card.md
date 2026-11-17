## Description:

Credit Repair Cloud (creditrepaircloud.com). Use this skill for ANY Credit Repair Cloud request — reading, creating, updating, and deleting data. Whenever a task involves Credit Repair Cloud, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to read and manage Credit Repair Cloud affiliate, lead, and client records through their connected account. It guides the agent to inspect each action's schema and obtain confirmation before writes or deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded code and can affect which skills are synchronized across agents.

Mitigation: Install a verified oo CLI release separately, and disable automatic skill synchronization unless additional skills are intended.

Risk: The connected account may expose sensitive client data, and record changes or deletions can alter or remove records.

Mitigation: Keep explicit approval requirements for writes and deletions, and review account access before connecting the service.

## Reference(s):

- [Credit Repair Cloud API documentation](https://app.creditrepaircloud.com/webapi)
- [Credit Repair Cloud homepage](https://www.creditrepaircloud.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON inputs and returned data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs follow the live connector schema; writes and deletions require user confirmation.]

## Skill Version(s):

1.0.4 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
