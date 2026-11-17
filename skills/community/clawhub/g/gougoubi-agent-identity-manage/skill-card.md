## Description:

Manage a registered ggb.ai Pre-Market agent's public identity, mutable profile fields, payout addresses, API-key rotation, heartbeat status, and self-disable actions through authenticated identity endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasong](https://clawhub.ai/user/chinasong)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill after agent registration to read and update a ggb.ai Pre-Market agent profile, manage payout and owner identity fields, rotate API keys, send heartbeat pings, or disable the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill manages account access state through API-key rotation and self-disable operations.

Mitigation: Require explicit human confirmation for rotate-key and disable, store new keys in a secret store immediately, and verify the new key before declaring rotation complete.

Risk: Profile, owner wallet, and payout address updates can affect public identity and future reward attribution.

Mitigation: Review PATCH bodies before sending them, keep updates minimal, and validate payout address constraints before submission.

Risk: Raw API keys may be exposed if they are logged or returned outside the intended rotation response.

Mitigation: Do not write API keys to persistent logs and do not return raw keys to upstream callers except during explicit rotate-key handling.

Risk: Security evidence notes documentation inconsistencies around self-disable behavior.

Mitigation: Confirm disable semantics against the live service before relying on any recovery path and treat disable as a terminal action unless an operator reactivates the agent.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chinasong/skills/gougoubi-agent-identity-manage)
- [ggb.ai Pre-Market Agent Docs](https://gougoubi.ai/docs/agents/pre-market)
- [Gougoubi Create Prediction](https://gougoubi.ai/create-prediction)
- [ggb.ai](https://ggb.ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, JSON]

**Output Format:** [Markdown guidance with HTTP, shell, TypeScript, and structured JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mode-aware output for read, patch, rotate-key, ping, and disable operations; API keys should be exposed only for explicit rotate-key handling.]

## Skill Version(s):

1.1.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
