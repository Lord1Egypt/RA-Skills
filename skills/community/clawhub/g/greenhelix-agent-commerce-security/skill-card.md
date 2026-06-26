## Description: <br>
A Markdown security guide for hardening autonomous AI agents that handle GreenHelix commerce workflows, credentials, payments, prompt injection defenses, monitoring, and audit trails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this guide to review and adapt hardening patterns for autonomous commerce agents that interact with GreenHelix tools, payment flows, signing keys, and audit logs. It is intended as human-facing guidance with illustrative code, not as a runnable agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide references GreenHelix, Stripe, and signing credentials, and copied examples could encourage unsafe private-key or payment-secret handling. <br>
Mitigation: Read without providing production credentials; when adapting examples, use an isolated signer, KMS/HSM, or secret manager rather than broad environment-based secret access. <br>
Risk: The security scan reports that an illustrative mutual-authentication example should fail closed before production use. <br>
Mitigation: Review and correct authentication examples before deployment, and test failure paths so transaction flows deny access when verification is incomplete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/greenhelix-agent-commerce-security) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API documentation](https://api.greenhelix.net/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guide with Python examples, checklists, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable guide; references GreenHelix, signing, and Stripe credentials that users supply in their own environments.] <br>

## Skill Version(s): <br>
1.3.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
