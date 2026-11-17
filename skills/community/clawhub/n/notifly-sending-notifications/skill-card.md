## Description:

Sends a Notifly workflow to a subscriber or topic after an explicit preview confirmation, then checks its status in the activity feed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

People using Notifly can send a workflow to a verified subscriber or topic, review the recipients and message details before confirming, and check the resulting delivery status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A confirmed notification is sent to real recipients and cannot be recalled; a topic may reach multiple subscribers.

Mitigation: Check the workflow, recipients or topic, channels, payload, and environment in the preview; send only after explicit confirmation.

## Reference(s):

- [Sending Notifications on ClawHub](https://clawhub.ai/devino/skills/notifly-sending-notifications)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Plain-language Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pre-send preview and confirmation request; transaction ID and activity-feed status after sending.]

## Skill Version(s):

1.0.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
