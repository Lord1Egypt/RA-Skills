## Description: <br>
Named trust groups with automatic mutual handshakes for Pilot Protocol agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create and maintain named Pilot Protocol trust circles for teams or projects, including adding members and bootstrapping mutual handshakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates durable agent-trust approvals, which can grant unintended access if a circle member is misidentified. <br>
Mitigation: Verify each member through a stable identity or fingerprint before approval and review proposed trust changes before execution. <br>
Risk: The bootstrap approval flow can approve pending agents based on hostname membership alone. <br>
Mitigation: Use the bootstrap flow only when hostname membership is backed by a trusted identity process and revocation is available for mistakes. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-trust-circle) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilot-protocol skill, pilotctl, jq, and a running Pilot daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
