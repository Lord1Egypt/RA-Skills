## Description: <br>
Maxhub Douyin helps agents query and analyze Douyin video, user, search, trending, creator, Xingtu KOL, content index, live, comment, and utility data through the MaxHub API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiewxx](https://clawhub.ai/user/xiewxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content operators, analysts, and agent users use this skill to collect Douyin data, compare accounts or competitors, monitor trends, inspect creator and live data, and prepare research or operational reports. It is not purely read-only and should be used with explicit approval for restricted, write-like, cookie, session, signature, bulk extraction, or private-message-link actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restricted and write-like endpoints can perform high-risk automation, session, anti-bot, messaging, or play-count related actions. <br>
Mitigation: Require explicit per-call approval before restricted, write, non-idempotent, session, cookie, anti-bot signature, bulk extraction, private-message-link, or play-count related requests. <br>
Risk: API keys, user-supplied identifiers, keywords, URLs, and optional cookies or tokens are transmitted to a third-party MaxHub service. <br>
Mitigation: Use only authorized data, minimize personal data, avoid logging secrets, rotate the API key, and avoid primary production account cookies or session credentials. <br>
Risk: Douyin data collection and automation may create platform policy or regional compliance obligations. <br>
Mitigation: Review each workflow against applicable platform terms and data protection rules before using collected data in databases, reports, or public outputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiewxx/maxhub-douyin) <br>
- [MaxHub API Service](https://www.aconfig.cn) <br>
- [Agent Decision Tree](SKILL.md) <br>
- [Recipes Index](references/recipes/_index.md) <br>
- [Endpoint Whitelist](references/endpoints_whitelist.yaml) <br>
- [Parameter Mappings](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl commands, configuration snippets, and structured API-response interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAXHUB_API_KEY and sends API keys, user-supplied IDs, keywords, URLs, and optional cookies or tokens to https://www.aconfig.cn.] <br>

## Skill Version(s): <br>
3.8.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
