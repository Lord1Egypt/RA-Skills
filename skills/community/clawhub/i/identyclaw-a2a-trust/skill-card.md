## Description:

Cryptographically trusted OpenClaw inter-agent messaging that wraps payloads in identyclaw.collaboration.v1 envelopes with HOLA mutual auth for sessions_send or A2A.

This skill is ready for commercial/non-commercial use.

## Publisher:

[identyclaw](https://clawhub.ai/user/identyclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add verifiable task delegation and forged-sender protection to OpenClaw inter-agent messages sent through sessions_send or A2A.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential and authorization controls may be too loosely configured for production agent fleets.

Mitigation: Review the skill before fleet installation and use narrowly scoped, short-lived IdentyClaw credentials.

Risk: An unreviewed or unpinned @rodit/hola-client implementation can weaken message construction or verification.

Mitigation: Use only a reviewed, pinned @rodit/hola-client implementation.

Risk: A receiver can accept messages meant for a different recipient slot if recipient expectations are not configured locally.

Mitigation: Configure a local expected recipient for receivers and reject envelopes that fail recipient or impersonation checks.

Risk: Pointing IDENTYCLAW_BASE_URL at an untrusted endpoint can undermine HOLA nonce and verification flows.

Mitigation: Restrict IDENTYCLAW_BASE_URL to the official HTTPS endpoint or a trusted private deployment.

## Reference(s):

- [Trusted inter-agent messages reference](references/trusted-sessions-send.md)
- [IdentyClaw OpenAPI schema](https://api.identyclaw.com/openapi.json)
- [OpenClaw issue #57387](https://github.com/openclaw/openclaw/issues/57387)
- [OpenClaw issue #38570](https://github.com/openclaw/openclaw/issues/38570)
- [OpenClaw issue #45427](https://github.com/openclaw/openclaw/issues/45427)
- [OpenClaw issue #47070](https://github.com/openclaw/openclaw/issues/47070)
- [OpenClaw A2A IdentyClaw plugin](https://github.com/discernible-io/openclaw-a2a-idc-plugin)
- [ClawHub skill page](https://clawhub.ai/identyclaw/skills/identyclaw-a2a-trust)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes helper script outputs for trusted message envelopes and verification results.]

## Skill Version(s):

0.2.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
