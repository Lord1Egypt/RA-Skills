## Description:

Pointagram (pointagram.com). Use this skill for ANY Pointagram request — reading, creating, updating, and deleting data. Whenever a task involves Pointagram, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Pointagram account users use this agent to inspect players and teams, manage team membership, and create, update, or delete player and team records through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run changing remote code and automatic skill synchronization may make broader skill changes; the installer and runtime were unavailable for verification.

Mitigation: Review and approve a fixed CLI release before setup, inspect the installation behavior, and use OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization when appropriate.

Risk: The connected OOMOL account mediates access to Pointagram account data, and write or deletion actions change that data.

Mitigation: Review the requested action and exact payload; retain the skill's confirmation requirement for writes and explicit approval for deletions.

## Reference(s):

- [Pointagram](https://www.pointagram.com/)
- [Pointagram Custom API Documentation](https://www.pointagram.com/custom-api-2-0-gamification/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured JSON action results with natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
