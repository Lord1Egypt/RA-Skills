## Description: <br>
Google Workspace Reseller: Manage Workspace subscriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Google Workspace reseller administrators and operators use this skill to inspect and manage reseller customers, notification watches, and subscriptions through the gws CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward Google Workspace reseller actions that affect customer billing, subscriptions, transfers, paid service starts, suspensions, and cancellations. <br>
Mitigation: Require explicit human approval before create, update, suspend, cancel, transfer, plan, seat, renewal, or paid-service actions. <br>
Risk: Misconfigured credentials or scopes could expose unintended reseller customers or subscriptions. <br>
Mitigation: Verify the gws CLI and shared authentication setup, and restrict credentials to the intended reseller account and scopes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/googleworkspace-bot/gws-reseller) <br>
- [Google Workspace Reseller API: Manage Customers](https://developers.google.com/workspace/admin/reseller/v1/how-tos/manage_customers) <br>
- [Google Workspace Reseller API: Manage Subscriptions](https://developers.google.com/workspace/admin/reseller/v1/how-tos/manage_subscriptions) <br>
- [Google Workspace Reseller API: Customers Insert Reference](https://developers.google.com/workspace/admin/reseller/v1/reference/customers/insert.html) <br>
- [Google Workspace Admin Help: Verify Your Domain](https://support.google.com/a/answer/9122284) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and CLI method guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses gws reseller help and schema discovery before API operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
