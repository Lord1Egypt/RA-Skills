## Description:

Retrieves vehicle location and status information, including locks, doors, windows, climate, engine-related state, SN, VIN, mileage, range, and power data, when a user asks about their vehicle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouzidan](https://clawhub.ai/user/zhouzidan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and vehicle-service assistants use this skill to retrieve a supported vehicle's current location and operating status after the user provides valid access and vehicle tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose precise vehicle location, vehicle identifiers, and vehicle status.

Mitigation: Use it only for authorized vehicles and require explicit user confirmation before performing location or status lookups.

Risk: Reusable access and vehicle tokens are cached in a plaintext local file.

Mitigation: Use tokens that can be rotated or revoked, restrict local file permissions, and remove the cache when access is no longer needed.

Risk: The documentation includes token examples and realistic token-shaped values that may be copied into transcripts or shared logs.

Mitigation: Mask credentials in examples and avoid sharing conversations, logs, or screenshots that contain access tokens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouzidan/skills/nokey-vehicle-info)
- [Nokey production vehicle condition API](https://openapi.nokeeu.com/iot/v1/condition)
- [Ingeek UAT vehicle condition API](https://uat-openapi.ingeek.com/iot/v1/condition)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return sensitive vehicle location, vehicle identifiers, and status fields derived from authenticated API responses.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
