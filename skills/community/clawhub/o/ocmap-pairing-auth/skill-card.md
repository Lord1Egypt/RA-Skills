## Description: <br>
Implement one-time pairing-code authentication between an OpenClaw gateway and a desktop or remote client such as OCMAP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement and review OpenClaw-to-OCMAP pairing flows, including one-time code exchange, short-lived bootstrap auth, signed device proof, trusted-device persistence, revocation, and recovery behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Short-lived bootstrap auth and pairing codes could be treated as durable credentials or exposed in logs. <br>
Mitigation: Keep bootstrap auth and pairing codes temporary, use very short TTLs, avoid logging them, and complete the exchange through the normal trusted-device flow. <br>
Risk: A long-lived trusted-device token could be exposed through renderer or browser UI state. <br>
Mitigation: Store trusted-device tokens only in backend or keychain-style storage and keep them out of renderer localStorage, IndexedDB, logs, and plain UI state. <br>
Risk: Revoked devices could continue reconnecting if revocation does not invalidate future trust checks. <br>
Mitigation: Ensure server-side revocation reliably disables future reconnects and returns the client to an unpaired or revoked recovery flow. <br>


## Reference(s): <br>
- [Pairing Protocol Contract](references/protocol.md) <br>
- [Server Implementation: OpenClaw](references/server-openclaw.md) <br>
- [Client Implementation: OCMAP or Other Desktop App](references/client-ocmap.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Code] <br>
**Output Format:** [Markdown guidance with protocol examples and implementation checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces implementation guidance for agents; does not execute tools or call external services.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
