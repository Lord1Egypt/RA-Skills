## Description:

Chorus (chorus.ai). Use this skill for ANY Chorus request — searching and reading data. Whenever a task involves Chorus, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to search and read Chorus conversations, engagements, scorecards, teams, and current-user details through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run downloaded installer code without separate approval; the remote installer contents could not be verified.

Mitigation: Install a verified oo CLI release separately and require approval before running downloaded installers. Review or disable automatic skill synchronization and limit the Chorus connection to the access needed.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Chorus](https://www.chorus.ai)
- [Chorus API documentation](https://api-docs.chorus.ai/)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON inputs and returned data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Chorus retrieval actions; action inputs are checked against the live schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
