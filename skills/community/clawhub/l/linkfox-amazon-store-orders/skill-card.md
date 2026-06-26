## Description: <br>
Helps agents retrieve Amazon seller orders and order details, inspect buyer, address, item, and regulated-order information, and submit shipment or verification updates through Amazon SP-API Orders workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ecommerce operators use this skill to let an agent search Amazon orders, retrieve order-level data, inspect order items and restricted order details, and prepare operational updates such as shipment confirmation or regulated-order verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose Amazon customer order data, including buyer, address, item, and regulated-order details. <br>
Mitigation: Install only for users authorized to access the relevant seller account, use least-privilege Amazon roles and RDT controls, and redact stdout, logs, and support tickets. <br>
Risk: The skill can change live shipment status, submit shipment confirmations, or update regulated-order verification status. <br>
Mitigation: Require deliberate human confirmation before running write operations and review the generated request body before submission. <br>
Risk: The skill depends on sensitive gateway credentials and a configurable gateway endpoint. <br>
Mitigation: Protect LINKFOXAGENT_API_KEY, keep the gateway URL on a trusted endpoint, and avoid sharing command output that contains account or order data. <br>


## Reference(s): <br>
- [API and gateway calling guide](references/api.md) <br>
- [Amazon SP-API searchOrders](https://developer-docs.amazon.com/sp-api/reference/searchorders) <br>
- [Amazon SP-API getOrder](https://developer-docs.amazon.com/sp-api/reference/getorder-3) <br>
- [Amazon SP-API getOrderBuyerInfo](https://developer-docs.amazon.com/sp-api/reference/getorderbuyerinfo) <br>
- [Amazon SP-API getOrderAddress](https://developer-docs.amazon.com/sp-api/reference/getorderaddress) <br>
- [Amazon SP-API getOrderItems](https://developer-docs.amazon.com/sp-api/reference/getorderitems) <br>
- [Amazon SP-API getOrderItemsBuyerInfo](https://developer-docs.amazon.com/sp-api/reference/getorderitemsbuyerinfo) <br>
- [Amazon SP-API updateShipmentStatus](https://developer-docs.amazon.com/sp-api/reference/updateshipmentstatus) <br>
- [Amazon SP-API getOrderRegulatedInfo](https://developer-docs.amazon.com/sp-api/reference/getorderregulatedinfo) <br>
- [Amazon SP-API updateVerificationStatus](https://developer-docs.amazon.com/sp-api/reference/updateverificationstatus) <br>
- [Amazon SP-API confirmShipment](https://developer-docs.amazon.com/sp-api/reference/confirmshipment) <br>
- [Amazon SP-API createRestrictedDataToken](https://developer-docs.amazon.com/sp-api/reference/createrestricteddatatoken) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some scripts include resolved request paths, query strings, assembled request bodies, and developerProxy status details in stdout for troubleshooting.] <br>

## Skill Version(s): <br>
0.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
