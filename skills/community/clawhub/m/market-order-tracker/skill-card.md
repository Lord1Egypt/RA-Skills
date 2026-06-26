## Description: <br>
Tracks export order lifecycles from order confirmation through delivery with status stages, deadline reminders, exception handling, and customer notification drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External trade operations teams, order trackers, and factory export departments use this skill to organize order stages, production milestones, logistics status, payment checkpoints, and customer updates. It is best suited for teams managing many active orders where missed handoffs or delayed notifications create delivery risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer, payment, shipment, and attachment details may contain sensitive business or personal information. <br>
Mitigation: Install only in approved workspaces and remove unnecessary personal or financial details before sharing outputs. <br>
Risk: Customer notification drafts could be sent to the wrong recipient or include sensitive attachments without adequate review. <br>
Mitigation: Treat outbound messages as drafts; verify the recipient, channel, and attachments such as invoices, packing lists, bills of lading, and certificates before sending. <br>


## Reference(s): <br>
- [Order Lifecycle Reference](references/order-lifecycle.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/wangm-a3/market-order-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with checklists, status tables, formulas, and message templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only workflow guidance; outbound customer messages should be reviewed before use.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
