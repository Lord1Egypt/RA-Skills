## Description:

Implement one-time pairing-code authentication between an OpenClaw gateway and a desktop or remote client such as OCMAP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement persistent trusted-device enrollment between an OpenClaw gateway and OCMAP or another desktop client. It guides the server and client through short-lived pairing codes, bootstrap authentication, signed device proof, trusted-token persistence, and revocation flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pairing codes, nonces, or bootstrap auth values could be exposed or reused during trusted-device enrollment.

Mitigation: Keep them short-lived, single-use, rate-limited, and out of logs and renderer storage.

Risk: A long-lived trusted-device token could be exposed through browser or renderer UI state.

Mitigation: Store the trusted token only in backend or main-process storage and provide a clear revoke or forget-device path.

Risk: Server and client implementations could drift on the pairing exchange contract.

Mitigation: Use the protocol contract as the source of truth for create, exchange, revoke, signed payload, structured errors, and reconnect behavior.

## Reference(s):

- [Protocol contract](artifact/references/protocol.md)
- [Server implementation](artifact/references/server-openclaw.md)
- [Client implementation](artifact/references/client-ocmap.md)
- [ClawHub skill page](https://clawhub.ai/maverick-software/skills/ocmap-pairing-auth)
- [Publisher profile](https://clawhub.ai/user/maverick-software)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with protocol JSON examples and implementation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; outputs should preserve the server/client contract and security requirements.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
