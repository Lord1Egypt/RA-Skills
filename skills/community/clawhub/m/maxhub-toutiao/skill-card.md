## Description: <br>
Maxhub Toutiao helps agents query and analyze Toutiao articles, videos, comments, and user profiles through the MaxHub API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiewxx](https://clawhub.ai/user/xiewxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and content operations teams use this skill to retrieve Toutiao content and user data for content intelligence, monitoring, reporting, and data alignment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the MaxHub API key, user-provided IDs, profile URLs, keywords, URLs, and optional cookies or tokens to https://www.aconfig.cn. <br>
Mitigation: Use only authorized data, minimize personal data, avoid production cookies or sensitive account tokens, rotate the API key, and do not expose secrets in logs or prompts. <br>
Risk: Returned comments or user-generated content may contain personal or sensitive information. <br>
Mitigation: Do not publish or store returned personal data unless the user has authorization and has checked applicable platform terms and privacy obligations. <br>
Risk: The security review notes documentation inconsistencies around advertised search, hot, and recommendation features. <br>
Mitigation: Treat those features as unsupported unless fixed by the publisher, and limit agent calls to the documented read-only whitelisted endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiewxx/maxhub-toutiao) <br>
- [MaxHub API service](https://www.aconfig.cn) <br>
- [README](README.md) <br>
- [Param & Field Mapping Index](references/param-mappings.md) <br>
- [Endpoint Whitelist](references/endpoints_whitelist.yaml) <br>
- [Toutiao Posts](references/post.md) <br>
- [Toutiao Users](references/user.md) <br>
- [Recipe Index](references/recipes/_index.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Text, JSON] <br>
**Output Format:** [Markdown guidance with curl commands and JSON response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only requests require MAXHUB_API_KEY and send query inputs to https://www.aconfig.cn.] <br>

## Skill Version(s): <br>
3.8.0 (source: server release metadata, SKILL.md frontmatter, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
