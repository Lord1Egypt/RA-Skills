## Description: <br>
Create disposable virtual credit cards for user-approved online checkout payments as part of broader purchasing tasks such as ordering food, buying subscriptions, purchasing domains, or booking services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adhambadr](https://clawhub.ai/user/adhambadr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill during a user-approved checkout to create a single-use virtual card for an online purchase, then fill payment details and confirm the order. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create payment cards with real spending authority. <br>
Mitigation: Approve each transaction only after checking the merchant, items, total, currency, and spending limit; use a revocable or limited HALOCARD_TOKEN where available. <br>
Risk: Payment credentials or card details could be exposed if copied into chats, files, or logs. <br>
Mitigation: Keep HALOCARD_TOKEN and generated card details out of chats and files, and create cards only when ready to fill the checkout form. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/adhambadr/halocard-virtualcards) <br>
- [Halocard signup](https://secure.halocard.co/enter) <br>
- [Halocard dashboard](https://secure.halocard.co/dashboard) <br>
- [Halocard payment API endpoint](https://agent.halocard.co/api/v1/payments) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HALOCARD_TOKEN and explicit user approval before creating a card.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
