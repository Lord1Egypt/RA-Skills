## Description:

Set up a local webhook server to receive Nansen smart alerts in real-time with HMAC signature verification and public tunneling. Use when a user wants to listen for alerts on their local machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers who use Nansen smart alerts can set up a local listener to receive and verify alert payloads through a public tunnel. They can optionally forward verified payloads to a configured OpenClaw Gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The public tunnel exposes the local listener to internet traffic, and unsigned requests still reach the machine even when rejected.

Mitigation: Choose and review the tunnel provider, keep the listener's signature verification enabled, and stop the tunnel when it is no longer needed.

Risk: The optional forwarding setting sends verified alert payloads to a configurable OpenClaw endpoint; the security scan flags this behavior as a disclosure concern.

Mitigation: Review the destination and payload flow before enabling forwarding, and configure only an intended, trusted endpoint.

Risk: The security verdict is suspicious with medium confidence, and scanner coverage is partial.

Mitigation: Review the skill's commands and forwarding settings before installation; the scan does not provide complete assurance.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/nansen-devops/skills/nansen-alerts-webhook-listener)
- [Nansen CLI browser login platform scope documentation](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with JavaScript code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a Node.js webhook server, secret-file setup steps, tunnel and alert configuration commands, and optional OpenClaw forwarding instructions.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
