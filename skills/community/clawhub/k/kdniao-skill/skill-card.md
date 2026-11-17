## Description:

Queries real-time Kdniao courier tracking data so agents can report shipment status, shipment progress, and delivery details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[15814059255](https://clawhub.ai/user/15814059255)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and logistics-support agents use this skill to query Kdniao with user-provided waybill numbers and present tracking status and timeline details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tracking numbers and authenticated request material can be sent to an external logistics API.

Mitigation: Use only authorized tracking numbers and tell users that shipment data will be sent to Kdniao or the configured API destination.

Risk: The optional API URL can redirect requests to an arbitrary destination.

Mitigation: Avoid overriding the default API URL unless the destination is trusted and controlled.

Risk: Credential-looking examples may be copied into environments or logs.

Mitigation: Replace examples with the user's own Kdniao credentials and keep the credential environment variable out of shared logs and transcripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/15814059255/skills/kdniao-skill)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown instructions with bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the Kdniao API response pretty-printed as JSON.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
