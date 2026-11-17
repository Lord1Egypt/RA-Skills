## Description:

Control 750+ BLE intimate devices via Intiface Central using the direct Buttplug v4 WebSocket protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chizumystic](https://clawhub.ai/user/chizumystic)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent list, vibrate, pattern, and stop Buttplug.io-compatible BLE devices through Intiface Central. It is intended for explicit, supervised control sessions where the user can stop or replace device activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control intimate physical devices and some commands can run indefinitely.

Mitigation: Use explicit short durations, keep a stop command ready, and avoid unattended sessions.

Risk: Plaintext ws:// remote-use guidance can expose device control over LAN or unsecured networks.

Mitigation: Prefer localhost or a secured tunnel/VPN and avoid exposing INTIFACE_WS_URL on untrusted networks.

Risk: Local PID-lock and interval-validation behavior may be unreliable for safety-critical stopping or session control.

Mitigation: Review or fix the PID-lock and interval-validation behavior before relying on the connector.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chizumystic/skills/intiface-direct-package)
- [Publisher profile](https://clawhub.ai/user/chizumystic)
- [Intiface Central](https://intiface.com/central/)
- [Buttplug.io-compatible device index](https://iostindex.com)
- [ws npm package](https://registry.npmjs.org/ws/-/ws-8.21.1.tgz)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Node.js code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may act on physical devices via Intiface Central and can continue until stopped or replaced.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
