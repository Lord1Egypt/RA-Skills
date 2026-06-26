## Description: <br>
Helps agents draft and run Pilot Protocol capability certificate issuance, transfer, and verification workflows using pilotctl, jq, and openssl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create, send, and inspect time-limited Pilot Protocol capability certificate files for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill claims cryptographically signed authorization certificates but the supplied security evidence says the documented workflow only checks unsigned JSON for high-impact capabilities. <br>
Mitigation: Review carefully before real authorization use; update the workflow to sign a canonical payload, verify signatures against trusted issuer keys, use minimal capabilities, confirm recipients, and provide revocation or containment controls. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-certificate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, jq, openssl, and the Pilot Protocol environment described by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
