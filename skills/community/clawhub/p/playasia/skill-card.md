## Description: <br>
Search Play-Asia digital products, check prices, make wallet or Lightning purchases, retrieve orders and digital codes, and manage customer-service enquiries through an MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tom-playasia](https://clawhub.ai/user/tom-playasia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent browse Play-Asia products, compare live prices, purchase digital codes, inspect wallet and order data, and manage support tickets when the required token or payment flow is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make purchases or trigger paid Lightning flows. <br>
Mitigation: Require explicit user confirmation before wallet purchases or Lightning payments, prefer info-only tokens for non-purchase tasks, and configure daily or weekly spending limits. <br>
Risk: The skill can access wallet, order, support-ticket, and purchased digital-code data when PA_TOKEN is configured. <br>
Mitigation: Use the least-privileged PA_TOKEN scope, keep the token out of chat and logs, and require confirmation before revealing digital codes or account details. <br>
Risk: The skill can send support messages and attachments through the connected Play-Asia account. <br>
Mitigation: Preview support text and attachments before submission and require user approval for each outbound support action. <br>
Risk: Capability labels and safety disclosures are reported as inconsistent by the provided security evidence. <br>
Mitigation: Review the skill configuration and disclosures before deployment, especially purchase, wallet, credential, and crypto capability labels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tom-playasia/playasia) <br>
- [Play-Asia L402 API](https://www.play-asia.com/l402) <br>
- [Play-Asia access tokens](https://www.play-asia.com/account/access-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON tool responses and concise Markdown guidance with configuration or shell command examples when setup or manual payment is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live product data, wallet balances, order details, Lightning invoices, support-ticket data, or digital-code delivery fields returned by Play-Asia APIs.] <br>

## Skill Version(s): <br>
0.3.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
