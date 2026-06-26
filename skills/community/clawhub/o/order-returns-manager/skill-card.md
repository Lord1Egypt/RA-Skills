## Description: <br>
Manage UK-compliant Shopify and WooCommerce orders via chat, including status checks, returns, refunds, exchanges, fulfilment updates, fraud flags, lost parcels, and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hussainpatan9](https://clawhub.ai/user/hussainpatan9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Store operators and commerce support teams use this skill to manage Shopify and WooCommerce order operations from chat, including returns, refunds, fulfilment changes, inventory restocking, fraud review, and customer updates. It is especially focused on UK merchants that need workflows aligned with UK consumer-rights rules. <br>

### Deployment Geography for Use: <br>
United Kingdom <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for powerful live store credentials through chat. <br>
Mitigation: Use dedicated least-privilege API keys, avoid sharing production secrets in ordinary chat where possible, and plan credential rotation or deletion before use. <br>
Risk: The skill can change live orders, refunds, inventory, and customer messages. <br>
Mitigation: Restrict who can invoke the bot and keep refund and mutation confirmations enabled, especially for high-value or irreversible actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hussainpatan9/order-returns-manager) <br>
- [README](artifact/README.md) <br>
- [Setup guide](artifact/CONFIG.md) <br>
- [Examples](artifact/EXAMPLES.md) <br>
- [Skill workflow source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration guidance] <br>
**Output Format:** [Markdown-style chat responses with API request examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may propose or execute live commerce actions such as refunds, order updates, fulfilment changes, inventory restocks, and customer notifications.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
