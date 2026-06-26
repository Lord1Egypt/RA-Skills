## Description: <br>
Create crypto payment and withdrawal links for your app across BSC, Ethereum, and TRON using the PayTheFlyPro gateway with built-in signature verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanlan](https://clawhub.ai/user/seanlan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to generate signed PayTheFlyPro payment and withdrawal URLs, and to query whether payment or withdrawal serial numbers have been used on supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The signer key authorizes PayTheFlyPro payment and withdrawal links. <br>
Mitigation: Use a dedicated unfunded signer key, store PTF_SIGNER_KEY securely, and keep it out of shared logs and CI output. <br>
Risk: A signed withdrawal URL can authorize a financial withdrawal for its encoded recipient, amount, serial number, and deadline. <br>
Mitigation: Verify the recipient, amount, serial number, and deadline before generating a withdrawal link, and share it only with the intended recipient. <br>


## Reference(s): <br>
- [PayTheFlyPro](https://pro.paythefly.com) <br>
- [ClawHub skill page](https://clawhub.ai/seanlan/paythefly) <br>
- [Publisher profile](https://clawhub.ai/user/seanlan) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown text with command examples, generated payment or withdrawal URLs, and order status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm, PayTheFlyPro project environment variables, and chain-specific configuration.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
