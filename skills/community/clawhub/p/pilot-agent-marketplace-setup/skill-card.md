## Description: <br>
Deploy a decentralized agent marketplace with directory, matchmaker, escrow, and gateway agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure a four-agent Pilot marketplace for capability discovery, request matching, trust handshakes, and escrow-backed settlement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup includes networked agent communication and trust handshakes. <br>
Mitigation: Confirm the required Pilot and ClawHub tooling is trusted, and test handshake and trust flows in an isolated environment before public exposure. <br>
Risk: The marketplace flow includes escrow-related actions and purchase-capable behavior. <br>
Mitigation: Validate escrow behavior with non-production hosts and test funds before using real funds or production services. <br>
Risk: The skill installs multiple transitive pilot-* skills. <br>
Mitigation: Review each transitive Pilot skill individually before deployment. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-agent-marketplace-setup) <br>
- [Publisher Profile](https://clawhub.ai/user/teoslayer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes per-role setup guidance, manifest examples, trust-handshake commands, and message-flow examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
