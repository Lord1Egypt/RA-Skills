## Description:

NetHunt (nethunt.com). Use this skill for ANY NetHunt request — reading, creating, updating, and deleting data. Whenever a task involves NetHunt, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams can use this skill to read and manage NetHunt records, comments, and call logs through an OOMOL-connected account. It guides users to confirm the action schema and approve data changes before they are run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions can execute remote CLI installers whose behavior was not verified in the release review.

Mitigation: Review and install the oo CLI yourself from a trusted source before enabling this skill.

Risk: Setup may enable automatic synchronization that installs additional agent skills.

Mitigation: Check the CLI's skill synchronization settings and disable synchronization if it is not wanted.

Risk: NetHunt requests pass through OOMOL, and write or delete actions can change connected account data.

Mitigation: Understand the OOMOL data route and retain explicit approval for each write or deletion.

## Reference(s):

- [NetHunt](https://nethunt.com)
- [NetHunt Integration API](https://nethunt.com/integration-api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The action and returned data depend on the requested NetHunt operation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
