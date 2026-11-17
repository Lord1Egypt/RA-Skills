## Description:

See and drive a real iPhone through an ESP32 Agent (Handsy) board with the esp32agent CLI or MCP server. Use when asked to look at, tap, swipe, type on, or operate an iPhone, or to test an iOS app on a real device.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onehumanbeing](https://clawhub.ai/user/onehumanbeing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and iOS app testers use this skill to inspect and operate a real iPhone through an ESP32 Agent board, including testing apps with screen-based interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates an unlocked phone that may expose private content or account actions.

Mitigation: Supervise the phone, limit screen access to what the task needs, and confirm before sending, spending, calling, deleting, changing security settings, or accepting terms.

Risk: Screenshots and recorded interaction histories may contain sensitive information.

Mitigation: Keep sensitive screens out of screenshots, review saved histories, and disconnect or unpair the board after use.

Risk: The CLI and firmware are downloaded separately, and the artifact review does not establish their safety.

Mitigation: Use a reviewed, pinned esp32agent version and verify firmware sources before installation.

## Reference(s):

- [Handsy](https://handsy.tech)
- [ESP32 Agent firmware installation](https://handsy.tech/install)
- [Handsy skill on ClawHub](https://clawhub.ai/onehumanbeing/skills/handsy)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Images]

**Output Format:** [Markdown guidance, CLI or MCP interaction results, and phone screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshots and interaction results reflect the connected iPhone; the skill notes that screenshots may lag and typing is ASCII-only.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
