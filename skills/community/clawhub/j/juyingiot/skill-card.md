## Description:

This skill helps an agent read status from and send explicit control commands to Juying Cloud IoT devices operated through Beijing Juying Electronics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liupster](https://clawhub.ai/user/liupster)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to list Juying Cloud devices, read device state, refresh real-time status, and open or close relay/output channels after providing their own API token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control real Juying Cloud hardware.

Mitigation: Install it only when hardware control is intended, require clear user authorization, confirm the target device and channel before control commands, and prefer read-only status checks when unsure.

Risk: A user API token can authorize device read and control operations.

Mitigation: Use a token limited to the devices and operations needed, never hardcode or share the token, and ask the user for their own token when it is missing.

Risk: Read responses and control commands use different channel numbering conventions.

Mitigation: Check channel mapping carefully: query feedback is zero-based, while control commands use one-based channel numbers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liupster/skills/juyingiot)
- [Juying Cloud OpenAPI base URL](https://openapi.iot02.com/api/v1)
- [Artifact overview](artifact/overview.md)
- [Artifact endpoints](artifact/endpoints.md)
- [Artifact examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, API calls]

**Output Format:** [Markdown or plain text with JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided API_Token and may issue authenticated requests to read or control Juying Cloud devices.]

## Skill Version(s):

1.0.7 (source: server release evidence; artifact frontmatter lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
