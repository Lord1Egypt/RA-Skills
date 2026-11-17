## Description:

ClickMeeting (clickmeeting.com). Use this skill for ANY ClickMeeting request — reading, creating, updating, and deleting data. Whenever a task involves ClickMeeting, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using ClickMeeting through an OOMOL-connected account can ask an agent to retrieve meeting, session, registration, attendee, recording, and chat information, or to create, update, register for, or delete meeting resources. The agent checks each action's current input schema before calling the connector.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic setup can execute unverified remote code.

Mitigation: Review and approve the CLI installation separately; use a pinned release with independently verified integrity before installing it.

Risk: Connecting ClickMeeting lets OOMOL mediate access to meeting data and room tokens.

Mitigation: Connect only the ClickMeeting account needed for the task and review the connection before allowing access.

Risk: Create, update, registration, token-generation, and delete actions change ClickMeeting state.

Mitigation: Confirm the exact action and payload with the user before running a state-changing command; confirm the target explicitly before deletion.

## Reference(s):

- [ClickMeeting API documentation](https://dev.clickmeeting.com/api-doc/)
- [ClickMeeting homepage](https://clickmeeting.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON connector responses and concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector results depend on the connected ClickMeeting account and the selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
