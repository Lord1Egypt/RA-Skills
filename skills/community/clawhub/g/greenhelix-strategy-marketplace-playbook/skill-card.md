## Description: <br>
The Agent Strategy Marketplace Playbook is a guide to selling verified trading strategies with escrow-protected subscriptions, covering marketplace listing, performance verification, subscription management, and dispute resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, trading strategy sellers, and agent operators use this guide to structure GreenHelix marketplace listings, escrow-backed subscriptions, signed performance claims, and dispute workflows for trading strategies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide describes high-impact financial marketplace actions, including subscriptions, escrow funding or release, dispute resolution, and recurring automation. <br>
Mitigation: Use sandbox credentials first and require explicit human approval before any live marketplace, escrow, dispute, payment, wallet, or recurring automation action. <br>
Risk: The release security summary notes inconsistent claims about sandbox use and signed performance proof. <br>
Mitigation: Independently verify GreenHelix signing, escrow, dispute, and performance-proof mechanics before relying on the guide for production financial workflows. <br>
Risk: The skill references sensitive credentials for API access and agent signing. <br>
Mitigation: Keep GREENHELIX_API_KEY and AGENT_SIGNING_KEY in a secrets manager or protected environment and do not provide live credentials unless live GreenHelix actions are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/greenhelix-strategy-marketplace-playbook) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API documentation](https://api.greenhelix.net/docs) <br>
- [Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guide with inline Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable guide; examples require user-supplied GreenHelix API and signing credentials for live use.] <br>

## Skill Version(s): <br>
1.3.1 (source: server-resolved release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
