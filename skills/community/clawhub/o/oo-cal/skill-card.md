## Description:

Cal.com (cal.com). Use this skill for ANY Cal.com request — reading, creating, updating, and deleting data. Whenever a task involves Cal.com, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to read and manage Cal.com bookings, availability, event types, schedules, and profile settings through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs users to run a remote installer whose integrity is unverified, and automatic skill synchronization could modify agent configuration.

Mitigation: Review and approve installation separately, use a pinned release with independently verified integrity, and check automatic skill synchronization before allowing configuration changes.

Risk: The skill accesses the connected calendar account and includes actions that can create, update, or delete calendar data.

Mitigation: Confirm the exact payload and effect before write actions, and confirm the target before destructive actions.

## Reference(s):

- [Cal.com API documentation](https://cal.com/docs/api-reference/v2/introduction)
- [Cal.com](https://cal.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON connector responses and concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses can contain connected calendar data; some actions change bookings, schedules, event types, profiles, or calendar settings.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
