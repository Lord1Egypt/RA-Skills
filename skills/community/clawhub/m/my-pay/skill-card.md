## Description: <br>
A payment skill powered by mypay-bot CLI for payment, purchase, checkout, transfer, wallet, and transaction workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xhc1111](https://clawhub.ai/user/xhc1111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to guide payment, purchase, checkout, transfer, wallet, and transaction workflows through the mypay-bot CLI after credentials and dependencies are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill can submit real payments using wallet-signing credentials without a required final approval step. <br>
Mitigation: Require the agent to show the exact amount, recipient or merchant, currency, fees, source wallet, and payment link, then get an explicit yes/no confirmation immediately before any submit-payment command. <br>
Risk: Payment credentials and payment URLs may contain tokens, signatures, hashes, or other secret-bearing parameters. <br>
Mitigation: Use only credentials that can be revoked, prefer a low-balance or scoped wallet, and do not paste or expose full secret-bearing payment URLs. <br>
Risk: Payment execution depends on the external mypay-bot package installed on the user's system. <br>
Mitigation: Review carefully before installing and use only a trusted mypay-bot package at the documented pinned version. <br>


## Reference(s): <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes exact payment workflow command guidance and credential setup instructions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
