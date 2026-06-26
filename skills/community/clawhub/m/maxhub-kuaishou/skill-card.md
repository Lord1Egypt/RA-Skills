## Description: <br>
Kuaishou public-data lookup and short-video analysis skill that uses the MaxHub API to query video details, author profiles, comments, search, trending lists, live data, and related content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiewxx](https://clawhub.ai/user/xiewxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, analysts, and developers use this skill to gather and analyze Kuaishou video, user, comment, search, trending, and live-stream data through MaxHub. It supports content planning, creator and KOL analysis, engagement tracking, trend monitoring, and operations review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Kuaishou search terms, profile or video IDs, links, optional cookies or tokens, and the MaxHub API key are transmitted to a third-party API service. <br>
Mitigation: Use a dedicated MaxHub API key, minimize personal data, avoid production cookies or session tokens, and do not expose secrets in logs or prompts. <br>
Risk: Returned comments, profile data, collections, favorites, or other user-generated content may contain personal or sensitive information. <br>
Mitigation: Use the skill only for authorized data processing and avoid storing or publishing personal data without a valid basis and user review. <br>
Risk: Resolving personal profiles, collections or favorites, and share links can increase privacy and platform terms-of-service risk. <br>
Mitigation: Ask for explicit user confirmation before those actions and keep the skill's read-only posture. <br>
Risk: Incorrect endpoint paths or guessed parameters can lead to failed or misleading API calls. <br>
Mitigation: Use only documented recipes, parameter mappings, and the endpoint whitelist instead of inventing paths or parameters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiewxx/maxhub-kuaishou) <br>
- [Publisher Profile](https://clawhub.ai/user/xiewxx) <br>
- [MaxHub API Website](https://www.aconfig.cn) <br>
- [README](README.md) <br>
- [Endpoint Whitelist](references/endpoints_whitelist.yaml) <br>
- [Parameter Mappings](references/param-mappings.md) <br>
- [Recipe Index](references/recipes/_index.md) <br>
- [Video Reference](references/video.md) <br>
- [User Reference](references/user.md) <br>
- [Search Reference](references/search.md) <br>
- [Comments Reference](references/comments.md) <br>
- [Live Reference](references/live.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown or plain text with inline shell commands, API call plans, and structured data summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAXHUB_API_KEY and curl; all API requests are sent to https://www.aconfig.cn.] <br>

## Skill Version(s): <br>
3.8.0 (source: frontmatter, server release metadata, target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
