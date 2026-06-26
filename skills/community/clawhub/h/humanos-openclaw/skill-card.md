## Description: <br>
Require verifiable human approval before high-risk agent actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lagosrui](https://clawhub.ai/user/lagosrui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to request, verify, and enforce human approval before actions involving money, data, identity, signing, or delegated authority. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends contacts and action metadata to the Humanos/VIA remote approval service. <br>
Mitigation: Install only when that approval service is intended, review the data included in each approval request, and use a dedicated least-privilege API key. <br>
Risk: The optional guard hook can affect whether protected tool calls execute. <br>
Mitigation: Configure VIA_PROTECTED_TOOLS explicitly before enabling the hook and test protected workflows before relying on enforcement. <br>
Risk: Local API credentials and signing secrets are required for operation. <br>
Mitigation: Store credentials in the expected environment or OpenClaw configuration and protect ~/.openclaw/openclaw.json with restrictive permissions such as chmod 600. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lagosrui/humanos-openclaw) <br>
- [Humanos API documentation](https://humanos.mintlify.app/essentials/introduction) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [W3C Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VIA_API_KEY and VIA_SIGNATURE_SECRET; optional guard hook can block protected tool calls until a mandate is verified.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
