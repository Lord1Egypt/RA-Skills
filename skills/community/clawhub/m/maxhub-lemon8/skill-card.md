## Description: <br>
Maxhub Lemon8 helps agents query and analyze public Lemon8 posts, comments, user profiles, search results, recommendations, and topics through the MaxHub API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiewxx](https://clawhub.ai/user/xiewxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content analysts use this skill to collect and analyze public Lemon8 content, creator profiles, comments, search results, hot keywords, topics, and recommendations for lifestyle content research, creator profiling, trend monitoring, and competitive analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Lemon8 links, IDs, keywords, optional cookies or tokens, and the MAXHUB_API_KEY to the MaxHub service at https://www.aconfig.cn. <br>
Mitigation: Use it only for authorized Lemon8 research, avoid production cookies or session credentials, minimize personal data, and keep API keys out of logs and prompts. <br>
Risk: Follower, following, profile, and comment data may identify people or include sensitive user-generated content. <br>
Mitigation: Handle returned data under applicable privacy and platform rules, and do not store or publish personal data without authorization. <br>
Risk: Incorrect endpoint paths or invented parameters can produce failed or misleading lookups. <br>
Mitigation: Use the bundled recipe index, parameter mappings, and endpoint whitelist before calling APIs, and report missing response fields rather than fabricating values. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiewxx/maxhub-lemon8) <br>
- [MaxHub API Service](https://www.aconfig.cn) <br>
- [README](README.md) <br>
- [Recipe Index](references/recipes/_index.md) <br>
- [Atomic Endpoint Index](references/atoms/_index.md) <br>
- [Content Endpoints](references/content.md) <br>
- [User Endpoints](references/user.md) <br>
- [Parameter Mappings](references/param-mappings.md) <br>
- [Endpoint Whitelist](references/endpoints_whitelist.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and API call plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only API lookup guidance; requires curl and MAXHUB_API_KEY; sends authorized Lemon8 queries to https://www.aconfig.cn.] <br>

## Skill Version(s): <br>
3.8.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
