## Description:

Freshservice (freshworks.com). Use this skill for ANY Freshservice request — reading, creating, and updating data. Whenever a task involves Freshservice, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Freshservice users and support teams use this skill to read tickets, locations, and service catalog items, and to create tickets and service requests through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unverified remote code or change other installed agent skills.

Mitigation: Inspect and verify the CLI release before installation, explicitly approve execution, and disable automatic skill synchronization with OO_SKILLS_SYNC_DISABLED.

Risk: The connected service can expose Freshservice account and ticket data, and write actions can change records.

Mitigation: Use limited account permissions and require confirmation of the exact payload and effect before write actions; get explicit approval for destructive actions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Freshservice homepage](https://www.freshworks.com/freshservice/)
- [Freshservice API documentation](https://api.freshservice.com/v2/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON inputs and responses, plus Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific inputs are checked against the live connector schema.]

## Skill Version(s):

1.0.5 (source: skill frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
