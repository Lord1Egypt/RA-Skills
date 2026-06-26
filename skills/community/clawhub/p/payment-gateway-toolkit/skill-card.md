## Description: <br>
Payment Gateway Toolkit helps agents and applications integrate Stripe and Alipay payment processing for order creation, refunds, status queries, webhook verification, and order history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add multi-channel payment handling to an agent or application, including Stripe card payments, Alipay web or scan-code payments, refunds, payment status checks, and webhook verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create payment orders and initiate refunds through Stripe or Alipay. <br>
Mitigation: Use sandbox or test credentials first, and review order creation and refund paths before production use. <br>
Risk: The skill requires sensitive Stripe API keys and Alipay private or public key material. <br>
Mitigation: Store credentials in environment variables or a secrets manager, and avoid committing keys to source control. <br>
Risk: Incorrect webhook or compliance handling can affect payment integrity, privacy, PCI, or business obligations. <br>
Mitigation: Verify webhook signatures and confirm applicable privacy, PCI, and compliance requirements before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kaiyuelv/payment-gateway-toolkit) <br>
- [Project Homepage](https://github.com/kaiyuelv/payment-gateway-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires payment-provider credentials and produces payment order, refund, status, history, and webhook verification outputs when connected to Stripe or Alipay.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
