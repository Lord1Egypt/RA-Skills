## Description: <br>
Enables AI agents to send USDC payments and order freelance services through an escrow-backed marketplace on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjorgensen](https://clawhub.ai/user/wjorgensen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and their agents use this skill to make USDC payments, place escrow-backed freelance orders, and monitor order status through Locus. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent real-money authority to send USDC or place escrow-backed freelance orders. <br>
Mitigation: Require human confirmation for every payment and order, and enforce allowance, per-transaction, and approval thresholds. <br>
Risk: Heartbeat routines can create recurring payment or ordering behavior if allowed to act beyond status polling. <br>
Mitigation: Limit heartbeat behavior to order status checks and require explicit human approval before any reorder or new purchase. <br>
Risk: Remote skill files can change after installation. <br>
Mitigation: Disable automatic remote updates or manually review and scan fetched updates before use. <br>
Risk: A leaked Locus API key can allow wallet spending through the connected account. <br>
Mitigation: Store the key securely, send it only to api.paywithlocus.com, and rotate it immediately if exposure is suspected. <br>
Risk: Freelance order requests may expose confidential or personal files through public URLs. <br>
Mitigation: Use only approved, non-sensitive public links in order requests. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wjorgensen/hire-with-locus) <br>
- [Locus skill documentation](https://paywithlocus.com/skill.md) <br>
- [Locus onboarding guide](https://paywithlocus.com/onboarding.md) <br>
- [Locus freelance ordering guide](https://paywithlocus.com/fiverr.md) <br>
- [Locus heartbeat guide](https://paywithlocus.com/heartbeat.md) <br>
- [Locus API base](https://api.paywithlocus.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API request and response examples, local credential setup guidance, and heartbeat status text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
