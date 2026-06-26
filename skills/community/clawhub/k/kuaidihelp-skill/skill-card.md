## Description: <br>
Assist with express delivery services including shipping cost estimation, logistics tracking, QR-code order creation, and order cancellation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanghai-kb](https://clawhub.ai/user/shanghai-kb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents assisting users with express delivery workflows use this skill to estimate shipping fees, query logistics status, create QR-code-based shipment orders, and cancel shipment orders through Kuaidihelp. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles full shipment personal data and sends shipment details to Kuaidihelp. <br>
Mitigation: Collect only the details required for the requested workflow, avoid unnecessary notes or images, and use the skill only when the user is comfortable sharing shipment data with Kuaidihelp. <br>
Risk: Order creation and cancellation can affect real shipments. <br>
Mitigation: Require explicit user confirmation immediately before creating an order or cancelling an order. <br>
Risk: The current script may print sensitive request data to terminal output or logs. <br>
Mitigation: Run it in a controlled environment and redact or avoid retaining command output that contains personal shipment details. <br>


## Reference(s): <br>
- [Kuaidihelp Open Platform](http://open.kuaidihelp.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/shanghai-kb/kuaidihelp-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/shanghai-kb) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with shell command examples and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return shipment pricing, tracking details, QR-code order links, or cancellation results depending on the selected workflow.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
