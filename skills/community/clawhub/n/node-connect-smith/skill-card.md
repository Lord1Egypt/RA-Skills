## Description:

Diagnoses OpenClaw node connection and pairing failures for Android, iOS, and macOS companion apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ciklopentan](https://clawhub.ai/user/ciklopentan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose OpenClaw companion app connectivity, route configuration, and device pairing or authentication failures across local, LAN, Tailscale, and public URL topologies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting commands can reveal OpenClaw auth tokens or device pairing state.

Mitigation: Review command output before sharing logs and redact auth tokens, bootstrap tokens, device IDs, and request IDs.

Risk: Approving, rotating, or re-approving devices or nodes can affect access to the OpenClaw gateway.

Mitigation: Only approve current trusted request IDs and confirm the intended route and topology before changing pairing or token state.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sequential troubleshooting flow with at most one targeted route or configuration fix before re-checking.]

## Skill Version(s):

1.0.2 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
