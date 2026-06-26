## Description: <br>
Buy AI services, crypto data, and digital goods on Pactum marketplace. Supports credit card, Alipay, WeChat Pay, and USDC payments. Register with email, search items, place orders, track delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fredm45](https://clawhub.ai/user/fredm45) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to browse Pactum marketplace listings, register for an account, place free or paid orders, track fulfillment, and handle post-delivery actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide account, payment, escrow, order, dispute, message, and shipping-address actions on the user's behalf. <br>
Mitigation: Require explicit user approval before every purchase, credit top-up, escrow deposit, payment release, dispute, message, and shipping-address change. <br>
Risk: The skill asks users to handle API keys and JWTs that can grant account access. <br>
Mitigation: Do not paste API keys or JWTs into chat logs or third-party bots unless the user fully trusts the service and understands how to revoke or rotate credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fredm45/pactum) <br>
- [Publisher profile](https://clawhub.ai/user/fredm45) <br>
- [Pactum marketplace](https://www.pactum.cc) <br>
- [Pactum API gateway](https://api.pactum.cc) <br>
- [Pactum orders](https://www.pactum.cc/orders) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, API calls, configuration] <br>
**Output Format:** [Markdown guidance with Python requests examples and REST API parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and user-provided account, payment, order, and shipping details when the selected marketplace action needs them.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
