## Description: <br>
Maxhub Temp Mail helps agents create temporary email addresses, list inbox messages, and read message details through the MaxHub API at https://www.aconfig.cn. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiewxx](https://clawhub.ai/user/xiewxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and authorized testers use this skill to create one-time inboxes, poll for registration or verification emails, and read message contents for non-sensitive testing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Temporary email workflows can support unauthorized registration, platform-rule evasion, or bulk account creation. <br>
Mitigation: Use only for authorized testing or low-risk one-time inboxes; do not use the skill to evade platform rules or create accounts at scale. <br>
Risk: The skill handles API keys, mailbox tokens, email addresses, and message contents through a third-party API. <br>
Mitigation: Keep MAXHUB_API_KEY, mailbox tokens, and message contents out of logs and prompts; avoid sensitive financial, legal, or private mail. <br>
Risk: Creating a temporary inbox is a resource-creating action, and displaying message contents can expose private or sensitive information. <br>
Mitigation: Require explicit user confirmation before creating an inbox or displaying message contents. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiewxx/maxhub-temp-mail) <br>
- [MaxHub API Service](https://www.aconfig.cn) <br>
- [Mail API Reference](references/mail.md) <br>
- [Endpoint Whitelist](references/endpoints_whitelist.yaml) <br>
- [Parameter Mappings](references/param-mappings.md) <br>
- [Recipe Index](references/recipes/_index.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with curl commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and MAXHUB_API_KEY; requests transmit API keys, mailbox tokens, and message data to https://www.aconfig.cn.] <br>

## Skill Version(s): <br>
3.8.0 (source: evidence release and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
