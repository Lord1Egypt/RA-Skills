## Description: <br>
Voice and text ordering agent for pizza shops that handles complex customizations, validates delivery zones, logs orders to Google Sheets, and applies ThumbGate checks to reduce order mistakes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igorganapolsky](https://clawhub.ai/user/igorganapolsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External pizza-shop operators and developers use this skill to support voice or text pizza ordering workflows, including menu matching, customizations, delivery-zone checks, upsells, and order logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer phone numbers, addresses, and order details may be logged to Google Sheets during ordering workflows. <br>
Mitigation: Use a dedicated Google Sheet with narrow permissions and explicit retention rules for customer phone, address, and order data. <br>
Risk: Incorrect delivery-zone or ThumbGate configuration could allow invalid deliveries or costly customization mistakes. <br>
Mitigation: Verify the delivery-zone settings and ThumbGate configuration before using the skill for a real shop. <br>
Risk: A live order could be finalized before the customer confirms the details. <br>
Mitigation: Require explicit confirmation before finalizing live orders. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/igorganapolsky/pizza-ordering-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Natural-language guidance with setup steps, order-handling rules, validation checks, and confirmation prompts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include customer order details intended for Google Sheets logging; live use should require confirmation before finalizing orders.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
