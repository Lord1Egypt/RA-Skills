## Description: <br>
Process e-commerce checkout via n8n webhook integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haresh-sai06](https://clawhub.ai/user/haresh-sai06) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and commerce agents use this skill to validate carts, handle authentication and shipping collection, initiate payment through a local n8n checkout workflow, and present order confirmation to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger payment or order processing through a local checkout webhook before final confirmation is clearly enforced. <br>
Mitigation: Require the agent to show the full order summary and receive explicit user confirmation before calling the checkout-process webhook. <br>
Risk: Checkout data may include sensitive payment or order information handled by a local n8n workflow. <br>
Mitigation: Install only with trusted local n8n workflows and verify the webhook does not receive or log full payment details unnecessarily. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haresh-sai06/haresh-checkout-flow) <br>
- [Publisher profile](https://clawhub.ai/user/haresh-sai06) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, API calls] <br>
**Output Format:** [Markdown or plain text checkout status, prompts, summaries, and local webhook calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted local n8n checkout workflow and explicit user confirmation before payment/order processing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
