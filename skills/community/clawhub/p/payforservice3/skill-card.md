## Description: <br>
Processes Alipay cashier links by checking wallet authorization, submitting payment requests, and querying payment status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xhc1111](https://clawhub.ai/user/xhc1111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to handle Alipay payment flows when a cashier link is present or the user explicitly requests payment. It guides wallet checks, payment submission, authorization handoff, and follow-up payment-status queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can begin wallet authorization or payment submission from broad or indirect payment triggers. <br>
Mitigation: Require explicit user confirmation before wallet authorization or submit-payment, and verify the merchant, amount, and cashier URL each time. <br>
Risk: Generated payment or authorization URLs may expose payment flow details if logged or forwarded outside the selected channel. <br>
Mitigation: Avoid logging or forwarding generated payment and authorization URLs outside the user's chosen channel. <br>
Risk: The skill installs and executes an external npm package for payment handling. <br>
Mitigation: Check the pinned npm package integrity before installation and install only when Alipay payment assistance is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xhc1111/payforservice3) <br>
- [Publisher profile](https://clawhub.ai/user/xhc1111) <br>
- [Alipay payment skills repository](https://github.com/alipay/payment-skills) <br>
- [@alipay/agent-payment npm package](https://www.npmjs.com/package/@alipay/agent-payment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with CLI command invocations, payment links, QR media references, and payment-status messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Payment and authorization URLs must remain intact and should not be logged or forwarded outside the user-selected channel.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
