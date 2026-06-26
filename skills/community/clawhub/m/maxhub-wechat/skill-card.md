## Description: <br>
Maxhub Wechat helps agents query and analyze public WeChat Official Accounts, Channels, search, comment, interaction, and media data through the MaxHub API at https://www.aconfig.cn. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiewxx](https://clawhub.ai/user/xiewxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, analysts, editors, and researchers use this skill to collect and analyze authorized WeChat article, account, comment, interaction, video, live, collection, and search data. It is intended for read-only content research, media monitoring, account profiling, and structured reporting through MaxHub APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends WeChat URLs, search terms, account IDs, and optional credentials to MaxHub/aconfig.cn. <br>
Mitigation: Use the skill only for authorized data processing, minimize personal data, and avoid exposing API keys, cookies, or tokens in logs or prompts. <br>
Risk: Returned comments, profiles, IP-region fields, media links, and decryption keys may be sensitive. <br>
Mitigation: Treat retrieved data as sensitive, avoid unauthorized storage or publication, and review outputs before sharing them. <br>
Risk: The security summary flags broad third-party data collection and media download/decryption behavior with inconsistent safeguards. <br>
Mitigation: Require explicit user confirmation before video download/decryption, bulk collection, or cross-domain account profiling. <br>


## Reference(s): <br>
- [MaxHub Website](https://www.aconfig.cn) <br>
- [ClawHub Skill Page](https://clawhub.ai/xiewxx/maxhub-wechat) <br>
- [WeChat Official Accounts Reference](references/mp.md) <br>
- [WeChat Channels Reference](references/channels.md) <br>
- [WeChat Search Reference](references/search.md) <br>
- [Parameter and Field Mapping Index](references/param-mappings.md) <br>
- [Recipe Index](references/recipes/_index.md) <br>
- [Endpoint Whitelist](references/endpoints_whitelist.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and JSON API request handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAXHUB_API_KEY and curl; sends authorized query parameters to https://www.aconfig.cn.] <br>

## Skill Version(s): <br>
3.8.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
