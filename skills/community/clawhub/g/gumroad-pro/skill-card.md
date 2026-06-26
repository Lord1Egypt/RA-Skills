## Description: <br>
Gumroad Pro helps agents manage Gumroad products, sales, licenses, discounts, payouts, and webhooks through an adaptive UI or Node.js CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abdul-karim-mia](https://clawhub.ai/user/abdul-karim-mia) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External creators, merchants, and store operators use this skill to administer a Gumroad storefront, including product catalog updates, sales review, refunds, shipping status, discounts, payout review, license-key operations, and webhook management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer a live Gumroad store, including product changes, refunds, shipping updates, license operations, discounts, payouts, and webhooks. <br>
Mitigation: Install only for agents authorized to manage the store, use a dedicated Gumroad token where possible, and verify product, sale, license, and webhook identifiers before running mutations. <br>
Risk: Customer emails, addresses, purchase details, and license keys may appear in chat or command output. <br>
Mitigation: Limit transcript sharing, avoid exposing customer data outside approved workflows, and review outputs before forwarding them. <br>
Risk: Webhook creation can send Gumroad events to configured URLs. <br>
Mitigation: Create webhooks only for trusted destinations and review each target URL before enabling it. <br>


## Reference(s): <br>
- [Gumroad Pro API Reference](references/api-reference.md) <br>
- [AI Guide: Gumroad Pro Handler Interaction](references/handler-guide.md) <br>
- [UI Rendering: Buttons](references/ui-rendering.md) <br>
- [Changelog: Gumroad Pro](references/changelog.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/abdul-karim-mia/gumroad-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses, interactive button metadata, and JSON CLI results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a Gumroad API token via GUMROAD_ACCESS_TOKEN or API_KEY.] <br>

## Skill Version(s): <br>
1.2.9 (source: release evidence, package.json, _meta.json, changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
