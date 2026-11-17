## Description:

Queries Kdniao shipment tracking APIs for real-time logistics status and tracking timelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[15814059255](https://clawhub.ai/user/15814059255)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to look up package delivery progress from a user-provided tracking number, then summarize the latest shipment status and timeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tracking numbers and credential-derived request data may be sent to a caller-selected API URL.

Mitigation: Use the official Kdniao endpoint unless an alternate destination has been independently verified, and restrict or review use of the --api-url option before deployment.

Risk: Real API credentials are required to call the service.

Mitigation: Store credentials securely, avoid reusing sample values, and provide credentials only through the documented KUAIDI_BIRD_API_CREDENTIALS environment variable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/15814059255/skills/kdniaoapi-skill)
- [ClawHub Publisher Profile](https://clawhub.ai/user/15814059255)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KUAIDI_BIRD_API_CREDENTIALS in CUSTOMER_CODE|APP_KEY format and a shipment tracking number.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
