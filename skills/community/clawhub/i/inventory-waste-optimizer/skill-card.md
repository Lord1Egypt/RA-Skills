## Description: <br>
Autonomous inventory management and waste reduction agent for QSRs. Cross-references sales data with inventory levels to forecast ordering and flag excessive waste. Hardened with ThumbGate to prevent over-ordering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igorganapolsky](https://clawhub.ai/user/igorganapolsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External QSR operators and inventory managers use this skill to monitor sales and inventory sheets, forecast restocking, flag waste or expiration risks, and apply ThumbGate checks before supply orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes automated ordering and purchase-order authority without clear approval limits. <br>
Mitigation: Start in recommendation-only or dry-run mode and require explicit human approval for each order with clear budget, vendor, and item limits. <br>
Risk: The setup uses Google Sheets data and an npx ThumbGate command in the order-control path. <br>
Mitigation: Connect only dedicated least-privilege Google Sheets and verify the ThumbGate npm package before running the setup command. <br>


## Reference(s): <br>
- [Inventory Waste Optimizer on ClawHub](https://clawhub.ai/igorganapolsky/inventory-waste-optimizer) <br>
- [Make.com](https://make.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain-text inventory recommendations or alerts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose restock actions and purchase-order creation; use only with explicit human approval and defined budget, vendor, and item limits.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
