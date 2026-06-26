## Description: <br>
Finds lowest prices for Pincode 500081 without freezing. Optimized for memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sparshkhandelwal28](https://clawhub.ai/user/sparshkhandelwal28) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users in Hyderabad use this skill to compare grocery and shopping prices for pincode 500081 across supported platforms, then receive a checkout handoff for manual payment approval. <br>

### Deployment Geography for Use: <br>
Hyderabad, India (pincode 500081) <br>

## Known Risks and Mitigations: <br>
Risk: The skill can navigate checkout flows and add selected items to merchant carts. <br>
Mitigation: Require explicit user selection before cart actions and keep manual payment confirmation outside the agent. <br>
Risk: Checkout screenshots or totals may be sent through Telegram. <br>
Mitigation: Confirm the Telegram recipient and screenshot content before sending, and avoid logged-in merchant accounts or sensitive delivery details unless the user explicitly wants that workflow. <br>
Risk: Price or item extraction can be stale, incomplete, or wrong when shopping sites time out or change layout. <br>
Mitigation: Show timeouts clearly in the final table and have the user verify item, quantity, delivery address, and total on the checkout page before payment. <br>


## Reference(s): <br>
- [Hyderabad Shopper on ClawHub](https://clawhub.ai/sparshkhandelwal28/hyderabad-shopper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown price table with checkout handoff text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open shopping sites, add selected items to carts, pause before payment, and send checkout screenshots or totals through Telegram.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
