## Description:

Capture useful durable notes into Karakeep from OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gasgangrene](https://clawhub.ai/user/gasgangrene)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to capture durable, human-discoverable notes, findings, source URLs, setup details, and project context into Karakeep from OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends authenticated requests to a local HTTP Karakeep endpoint.

Mitigation: Install it only for a Karakeep instance you control on a trusted network, and prefer HTTPS or a trusted private tunnel.

Risk: Captured notes could accidentally contain credentials, private messages, or other sensitive material.

Mitigation: Review note content before saving, avoid secrets and private third-party messages, and keep the Karakeep token file protected.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/gasgangrene/skills/karakeep-note-capture)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
