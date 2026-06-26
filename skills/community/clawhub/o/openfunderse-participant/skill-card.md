## Description: <br>
Participant MoltBot for allocation proposal, validation, and submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wiimdy](https://clawhub.ai/user/wiimdy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and OpenClaw operators use this skill to run a participant bot that proposes, validates, and optionally submits OpenFunderse allocation claims through a relayer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a blockchain signer key through PARTICIPANT_PRIVATE_KEY. <br>
Mitigation: Use a dedicated low-value participant wallet and never reuse treasury, custody, or admin keys. <br>
Risk: Installation can execute code fetched from npm. <br>
Mitigation: Install first in an isolated or non-production OpenClaw environment, review the pinned npm package before production use, and avoid funding the wallet until setup is verified. <br>
Risk: Install and bot-init flows can change global OpenClaw runtime state and restart the gateway. <br>
Mitigation: Prefer no-sync and no-restart options until changes are inspected, and back up and audit ~/.openclaw/openclaw.json and generated wallet backup files after setup. <br>
Risk: Relayer submissions can transmit signed allocation claims to a network endpoint. <br>
Mitigation: Keep explicit-submit gates enabled, configure trusted relayer host checks, and require HTTPS except for local development. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wiimdy/openfunderse-participant) <br>
- [Publisher profile](https://clawhub.ai/user/wiimdy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON contracts and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces allocation claim guidance, validation or dry-run decisions, relayer submission instructions, and OpenClaw environment setup details.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
