## Description: <br>
Monitor PopMart product restock status across multiple channels including WeChat Mini Programs, Taobao, JD.com, and Tmall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iiustrator](https://clawhub.ai/user/iiustrator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure PopMart product watch lists, run stock checks across supported commerce channels, and receive restock notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for Taobao/JD credentials, session cookies, proxy credentials, and Feishu webhooks. <br>
Mitigation: Treat all credentials and webhook URLs as secrets, avoid committing populated config files, and only provide credentials in a constrained runtime you trust. <br>
Risk: The stock monitor may produce fabricated or unreliable stock results because current handlers and parsing are incomplete. <br>
Mitigation: Review and test platform handlers against live products before relying on alerts for purchasing decisions. <br>
Risk: Recurring monitoring can make outbound third-party requests to commerce platforms and notification services. <br>
Mitigation: Use reasonable intervals, respect platform terms and rate limits, and run monitoring only where those outbound requests are expected. <br>


## Reference(s): <br>
- [Setup Guide](references/SETUP_GUIDE.md) <br>
- [OpenClaw Integration Guide](references/OPENCLAW_INTEGRATION.md) <br>
- [Example Configuration](references/example_config.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/iiustrator/popmart-stock-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate or update local configuration files and send outbound notification requests when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
