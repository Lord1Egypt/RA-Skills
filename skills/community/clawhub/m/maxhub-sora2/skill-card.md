## Description: <br>
Maxhub Sora2 helps agents query and analyze Sora2 posts, users, comments, replies, Remix relationships, download and media information, and perform confirmed image upload and video creation through the MaxHub API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiewxx](https://clawhub.ai/user/xiewxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and analysts use this skill to inspect Sora2 content, user activity, comments, remixes, downloads, and creation tasks through MaxHub. It is suitable for authorized creative workflows and content analysis where write, upload, and download actions are explicitly confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the MaxHub API key and user-supplied IDs, keywords, URLs, and optional cookies or tokens to the third-party MaxHub API. <br>
Mitigation: Use a dedicated API key, minimize personal data, and do not expose secrets in prompts, logs, or generated output. <br>
Risk: The skill supports video creation, image upload, download-related actions, and other non-idempotent workflows. <br>
Mitigation: Require explicit user confirmation before write, media upload, non-idempotent, or download actions. <br>
Risk: Private or signed image URLs and primary-account cookies or session tokens could expose sensitive account or media access. <br>
Mitigation: Avoid private or signed image URLs and do not provide primary-account cookies or session tokens. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiewxx/maxhub-sora2) <br>
- [Publisher Profile](https://clawhub.ai/user/xiewxx) <br>
- [MaxHub Website](https://www.aconfig.cn) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [Endpoint Whitelist](references/endpoints_whitelist.yaml) <br>
- [Parameter Mappings](references/param-mappings.md) <br>
- [Recipe Index](references/recipes/_index.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and API-derived result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and MAXHUB_API_KEY; write, media upload, non-idempotent, and download actions require confirmation.] <br>

## Skill Version(s): <br>
3.8.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
