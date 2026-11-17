## Description:

Secure outbound-only relay for remote OpenClaw control with no exposed ports, SSH, Telegram, or Discord dependency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-czar](https://clawhub.ai/user/jason-czar)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use this skill to connect headless or server-deployed OpenClaw nodes to a trusted relay so they can send prompts, check status, trigger workflows, and restart nodes remotely without exposing inbound network ports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote relay control can expose prompts, response tokens, workflow triggers, status, and restart actions to the configured relay operator.

Mitigation: Use only a relay operator you trust, rotate AUTH_TOKEN as a remote-control credential, and review relay access policies before enabling the skill.

Risk: Plaintext relay URLs or weak transport settings can undermine the promised encrypted WebSocket posture.

Mitigation: Require a wss:// relay URL and avoid ws:// or http:// relay configuration except in isolated local testing.

Risk: The server security summary warns that authentication and encrypted transport enforcement may be weaker than the documentation promises.

Mitigation: Prefer a version that gates remote commands on successful authentication and restricts which workflows can be triggered remotely.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jason-czar/skills/private-bridge)
- [Publisher profile](https://clawhub.ai/user/jason-czar)
- [Artifact skill documentation](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript code interfaces, shell commands, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RELAY_URL, NODE_ID, and AUTH_TOKEN configuration; output focuses on remote relay setup, status, workflow triggering, and operational guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
