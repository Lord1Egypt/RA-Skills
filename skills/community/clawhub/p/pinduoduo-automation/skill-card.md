## Description: <br>
Pinduoduo Automation helps Pinduoduo merchants prepare store operations workflows, sales reports, competitor monitoring, and pricing guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wukaikai522](https://clawhub.ai/user/wukaikai522) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External Pinduoduo merchants and developers can use this skill to configure store automation, generate sales reports, monitor competitors, and prepare pricing or promotion guidance. Live merchant actions should be reviewed before use because the release requests merchant API credentials and the implementation is incomplete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for Pinduoduo merchant credentials. <br>
Mitigation: Use a limited or non-production account and do not enter production credentials until the publisher documents least-privilege scopes and credential handling. <br>
Risk: The skill advertises automation that could affect products, orders, pricing, promotions, and logistics. <br>
Mitigation: Require explicit confirmations, dry-run previews, and human review before enabling any live business-changing action. <br>
Risk: The artifact includes placeholder scripts and missing implementation for real API behavior. <br>
Mitigation: Treat generated reports and recommendations as templates until the missing implementation is supplied and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wukaikai522/pinduoduo-automation) <br>
- [Pinduoduo Open Platform](https://open.pinduoduo.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, shell-command output, and YAML configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local Markdown reports and requires user-provided Pinduoduo API credentials for live integrations.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
