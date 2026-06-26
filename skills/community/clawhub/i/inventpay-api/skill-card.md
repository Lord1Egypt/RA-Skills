## Description: <br>
Accept crypto payments, manage a digital storefront, and track balances through the InventPay REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jams24](https://clawhub.ai/user/jams24) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and merchants use this skill to let an agent create crypto payment links and invoices, manage InventPay storefront products and key pools, review orders, and check merchant balances. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad live merchant-account authority, including persistent storefront changes and deletion operations. <br>
Mitigation: Require manual confirmation before deleting products, removing keys, changing order status, publishing store changes, or creating customer-facing payment content. <br>
Risk: The INVENTPAY_API_KEY authorizes merchant operations and could expose account control if mishandled. <br>
Mitigation: Treat INVENTPAY_API_KEY like a password, keep it out of shared content, and revoke it if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jams24/inventpay-api) <br>
- [InventPay homepage](https://inventpay.io) <br>
- [InventPay API documentation](https://docs.inventpay.io) <br>
- [InventPay source repository](https://github.com/jams24/inventpay-mcp) <br>
- [InventPay JavaScript SDK](https://www.npmjs.com/package/inventpay) <br>
- [InventPay Python SDK](https://pypi.org/project/inventpay) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown] <br>
**Output Format:** [Markdown with inline HTTP examples, JSON request and response bodies, and shell configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires INVENTPAY_API_KEY for authenticated merchant operations.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata; SKILL.md frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
