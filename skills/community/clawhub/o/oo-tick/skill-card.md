## Description:

Lets an agent read Tick clients, projects, tasks, users, and time entries, and create, update, or delete time entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

For people managing a Tick workspace through an agent: retrieve workspace data and manage time entries, with user confirmation for changes and explicit approval for deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded software without a separate approval or verification step.

Mitigation: Verify the CLI release and require approval before installation; review or disable automatic skill synchronization, connect only the intended Tick account, and retain write/delete confirmations.

## Reference(s):

- [Tick homepage](https://www.tickspot.com)
- [Tick API documentation](https://github.com/tick/tick-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-tick)
- [Publisher profile](https://clawhub.ai/user/oomol)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [oo CLI connector calls with JSON payloads and Tick results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads workspace data; creates, updates, or deletes time entries when requested.]

## Skill Version(s):

1.0.2 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
