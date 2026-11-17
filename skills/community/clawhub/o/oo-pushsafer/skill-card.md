## Description:

Operate Pushsafer through an OOMOL-connected account to list devices and groups or send push notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can check registered Pushsafer devices and groups, and send push notifications from an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run remote installers and add persistent agent skills beyond Pushsafer functionality.

Mitigation: Review installer commands and skill synchronization settings before setup; disable startup synchronization if only Pushsafer functionality is needed.

Risk: Sending a push notification changes the user's Pushsafer account state.

Mitigation: Confirm the recipients and exact message payload with the user before running the send action.

## Reference(s):

- [Pushsafer API documentation](https://www.pushsafer.com/en/pushapi)
- [Pushsafer](https://www.pushsafer.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions]

**Output Format:** [JSON request payloads and connector response data, with inline shell commands for setup and use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions include read-only device and group listings and push notification sending.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
