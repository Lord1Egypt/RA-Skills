## Description: <br>
Instagram public social data query and content analysis skill that uses the MaxHub API to retrieve posts, Reels, Stories, Highlights, comments, likes, user profiles, followers, following, searches, hashtags, and related content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiewxx](https://clawhub.ai/user/xiewxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and social media analysts use this skill to query and analyze Instagram public or user-authorized data for creator research, content engagement analysis, competitor tracking, and trend research through MaxHub API endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Instagram targets, searches, URLs, location-related queries, and MAXHUB_API_KEY to the third-party MaxHub service at https://www.aconfig.cn. <br>
Mitigation: Use the skill only when this third-party data transfer is acceptable, keep API keys out of logs and prompts, and rotate credentials as needed. <br>
Risk: Broad Instagram collection workflows can expose or aggregate personal data from followers, likers, comments, locations, and search results. <br>
Mitigation: Limit use to public or clearly authorized analysis, minimize collected personal data, and avoid storing or republishing sensitive user-generated content without authorization. <br>
Risk: Optional cookies or session tokens could expose production Instagram accounts. <br>
Mitigation: Avoid providing Instagram cookies, session tokens, or production account credentials; use separate test credentials when a workflow requires account context. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiewxx/maxhub-instagram) <br>
- [MaxHub Website](https://www.aconfig.cn) <br>
- [SkillHub Listing](https://skillhub.cn/skills/maxhub-instagram) <br>
- [Repository](https://github.com/XieWxx/maxhub-api-skills) <br>
- [Recipe Index](references/recipes/_index.md) <br>
- [Endpoint Whitelist](references/endpoints_whitelist.yaml) <br>
- [Parameter Mappings](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only API workflows require curl and MAXHUB_API_KEY; outputs should disclose that data comes from https://www.aconfig.cn.] <br>

## Skill Version(s): <br>
3.8.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
