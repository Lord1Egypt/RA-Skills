## Description: <br>
Complete cold email campaign suite for Mailgo: verify recipients, claim a free mailbox, generate and optimize content, create campaigns, manage lifecycle, and view reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leadsnavideveloper](https://clawhub.ai/user/leadsnavideveloper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to prepare, launch, monitor, and manage Mailgo cold-email campaigns from recipient verification through reporting. It is intended for authorized Mailgo accounts and recipient lists the user is permitted to process. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload lead data and launch live cold-email campaigns with insufficient final user confirmation. <br>
Mitigation: Run dry-run or draft mode first, then require final human review of recipients, content, sender, schedule, and timezone before activating a campaign. <br>
Risk: The skill requires a Mailgo API token and can access account-level campaign, mailbox, recipient, and reporting operations. <br>
Mitigation: Set credentials only through environment or action authentication, avoid pasting secrets into chat, and prefer a limited or disposable API token if Mailgo supports it. <br>
Risk: The skill can process recipient lists that may contain personal or unauthorized contact data. <br>
Mitigation: Use only recipient lists the user is authorized to process and verify deliverability before sending to larger lists. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/leadsnavideveloper/mailgo-coldmail-marketing) <br>
- [Publisher profile](https://clawhub.ai/user/leadsnavideveloper) <br>
- [Mailgo application](https://app.mailgo.ai) <br>
- [Spam trigger reference](resources/spam-triggers.md) <br>
- [Industry template reference](resources/industry-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON outputs from bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Mailgo APIs through bundled scripts and may create or modify live campaign state after user review.] <br>

## Skill Version(s): <br>
1.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
