## Description:

StatusCake (statuscake.com). Use this skill for ANY StatusCake request — reading, creating, updating, and deleting data. Whenever a task involves StatusCake, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to inspect StatusCake uptime tests, locations, alerts, history, and uptime periods, and to create, update, or delete tests through their connected account. Changes and deletions require user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup can automatically execute an unverified remote CLI installer.

Mitigation: Review and approve CLI installation separately, preferably using a verified release. Confirm whether setup will install or update other agent skills, and ensure you trust OOMOL to handle the StatusCake connection.

## Reference(s):

- [StatusCake](https://www.statuscake.com)
- [StatusCake API documentation](https://developers.statuscake.com/)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action requests and responses with concise textual summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action and payload vary by the requested StatusCake operation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
