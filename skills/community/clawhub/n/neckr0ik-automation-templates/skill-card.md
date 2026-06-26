## Description: <br>
Provides ready-to-use automation templates for n8n, Make.com, and Zapier with pre-built workflows for common use cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neckr0ik](https://clawhub.ai/user/Neckr0ik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and automation builders use this skill to find, customize, and generate starter workflows for n8n, Make.com, and Zapier covering email, CRM, data sync, notifications, and e-commerce. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated automation workflows can trigger external effects when activated with real credentials, webhooks, CRM targets, Slack channels, or email recipients. <br>
Mitigation: Review each workflow node by node, use test data and least-privilege credentials, confirm endpoints and recipients, and activate only after verifying expected effects and rollback steps. <br>
Risk: Template variables include API keys, webhook URLs, and destination placeholders that may be misconfigured during customization. <br>
Mitigation: Replace placeholders deliberately, keep credentials out of shared artifacts, and validate generated JSON or YAML in the target automation platform before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Neckr0ik/neckr0ik-automation-templates) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or YAML workflow configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated workflows may contain placeholder credentials, webhook URLs, recipients, channels, and service targets that require review before activation.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, claw.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
