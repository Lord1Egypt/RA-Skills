## Description:

Use Push by Techulus to send notifications to a device group or to all devices targeted by the connected account or team API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users can send notifications through Push by Techulus, choosing a device group or the account and team API key's targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run a remote CLI installer and can introduce lasting agent changes through skill installation or refresh.

Mitigation: Review and approve CLI installation separately, verify the release, decide whether OOMOL may install or refresh other agent skills, and disable startup skill synchronization if unwanted.

Risk: Notifications can reach the selected device group or all devices targeted by the connected account or team API key.

Mitigation: Confirm the recipients and notification content; before sending a write action, confirm its exact payload and effect.

Risk: The inspected artifact does not include the external installer or live connector implementation.

Mitigation: Review and verify the release and assess the external installer and connector before relying on them.

## Reference(s):

- [Push by Techulus API documentation](https://docs.push.techulus.com/api-documentation)
- [Push by Techulus](https://push.techulus.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Notification text and JSON action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results depend on the provider response and selected notification action.]

## Skill Version(s):

1.0.5 (source: server-resolved release version and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
