## Description: <br>
Manage shopping cart operations via n8n webhook integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haresh-sai06](https://clawhub.ai/user/haresh-sai06) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and shopping assistants use this skill to add items, remove items, and update quantities in a shopping cart through a trusted local n8n workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change cart contents through local n8n webhooks when invoked. <br>
Mitigation: Install only when the localhost n8n workflow is trusted, and require user confirmation before removing items. <br>
Risk: Invalid product IDs or quantities could cause unintended cart updates. <br>
Mitigation: Validate product IDs and allow only positive integer quantities before calling cart webhooks. <br>


## Reference(s): <br>
- [Haresh Cart Management on ClawHub](https://clawhub.ai/haresh-sai06/haresh-cart-management) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [Natural-language confirmations and local HTTP webhook requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses localhost n8n webhook endpoints for add, remove, and update cart operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
