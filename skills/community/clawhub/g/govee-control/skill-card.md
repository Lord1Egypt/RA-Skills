## Description:

Script-free Govee OpenAPI setup and control guide. Use when the user wants to get a Govee API key, connect Govee, list devices, check state, or send power/brightness/color commands with secure key handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cole-z](https://clawhub.ai/user/cole-z)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure secure Govee API access, discover linked devices, inspect device state, and prepare manual curl commands for one-device-at-a-time control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A leaked GOVEE_API_KEY could allow unwanted access to the user's Govee API account.

Mitigation: Keep GOVEE_API_KEY private, store it only in a per-user secrets file, avoid chat logs and git, and load only that variable when needed.

Risk: Control commands can change real device state, especially when applied to multiple devices or bulk actions.

Mitigation: Review each control command before running it, prefer one-device-at-a-time actions, and ask before controlling multiple devices.

Risk: Unrelated outbound requests or unrelated secret reads would expand the skill's operational scope.

Mitigation: Restrict outbound requests to Govee developer endpoints and read only GOVEE_API_KEY from the selected per-user secrets file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cole-z/skills/govee-control)
- [Publisher profile](https://clawhub.ai/user/cole-z)
- [Govee Developer Portal](https://developer.govee.com/)
- [Govee OpenAPI base endpoint](https://developer-api.govee.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses placeholders for device identifiers and API keys; no scripts are shipped.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
