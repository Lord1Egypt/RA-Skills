## Description: <br>
Create complete WeChat Official Account viral articles from a user-provided title by researching high-view YouTube videos, confirming topic/outline with user, writing professional content through self-iteration, and outputting both Markdown and HTML formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffli2002](https://clawhub.ai/user/jeffli2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and operators use this skill to research a supplied topic, confirm an article direction, and produce WeChat Official Account content ready for review. It supports Markdown and WeChat-styled HTML outputs, with optional cover-image generation and WeChat draft or publishing steps when credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles GLM and WeChat credentials, and the release security guidance warns users to remove or rotate any real exposed credentials. <br>
Mitigation: Store credentials in environment variables or a private .env file, avoid commands that print API keys, and rotate any credential that may have been exposed. <br>
Risk: The skill can use WeChat draft or freepublish actions and may route publishing through a configured proxy endpoint. <br>
Mitigation: Restrict WECHAT_PROXY_URL to a trusted endpoint or disable it, and require explicit user approval before any WeChat draft or freepublish action. <br>
Risk: Generated articles may contain claims derived from YouTube or web research that require editorial verification before publication. <br>
Mitigation: Review every generated article and verify cited claims against source material before publishing commercially. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/jeffli2002/jeff-content-factory) <br>
- [YouTube Research Checklist](references/youtube_research_checklist.md) <br>
- [WeChat Publish Rules](references/WECHAT_PUBLISH_RULES.md) <br>
- [WeChat Format Rules](references/wechat-format-rules.md) <br>
- [WeChat Viral Frameworks](references/wechat_viral_frameworks.md) <br>
- [GLM API Key Setup](API_KEY_SETUP.md) <br>
- [Configuration Guide](CONFIGURATION.md) <br>
- [WeChat Cover Photo Guide](scripts/COVER_PHOTO_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, html, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown articles, WeChat-ready HTML, social snippets, cover-image files, and command/configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May optionally create WeChat drafts or publish through WeChat APIs when credentials are configured and the user approves.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
