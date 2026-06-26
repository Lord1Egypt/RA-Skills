## Description: <br>
Unified food ordering assistant for India that supports Swiggy and Zomato workflows with strict pre-order confirmation, cart preview, address checks, and vendor fallback logic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anugotta](https://clawhub.ai/user/anugotta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users in India use this skill to compare supported food-ordering vendors, prepare carts, verify delivery details, and proceed only after explicit confirmation. <br>

### Deployment Geography for Use: <br>
India <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help place real food orders, so incorrect cart, address, payment, or cancellation details could cause user-impacting purchases. <br>
Mitigation: Before order placement, verify the vendor, restaurant, items, total payable, full delivery address, ETA, payment method, and cancellation terms with the user. <br>
Risk: Checkout failures, fallback flows, or automatic retries could create duplicate or unintended orders. <br>
Mitigation: Use only trusted connectors, do not auto-retry order placement, and require a fresh full-cart confirmation before fallback checkout. <br>
Risk: Delivery addresses and order history may expose sensitive personal context in shared sessions. <br>
Mitigation: Avoid storing address aliases or order logs in shared contexts, and ask the user to clarify ambiguous saved address labels. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/anugotta/india-food-ordering) <br>
- [OpenClaw Homepage](https://clawhub.ai/regalstreak/swiggy) <br>
- [Operational Notes](vendor-playbook.md) <br>
- [Prompt Examples](examples.md) <br>
- [Safety and QA Checks](validation-checklist.md) <br>
- [Launch Flow](launch-playbook.md) <br>
- [Setup](setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown responses with vendor comparisons, cart summaries, confirmation prompts, and order status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires trusted food-ordering connectors and explicit user confirmation before any order placement.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
