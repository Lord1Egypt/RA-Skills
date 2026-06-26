## Description: <br>
Create complete WeChat Official Account viral articles from a user-provided title by researching high-view YouTube videos, confirming topic/outline with user, writing professional content through self-iteration, and outputting both Markdown and HTML formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffli2002](https://clawhub.ai/user/jeffli2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and marketing teams can use this skill to research timely topics, propose and confirm WeChat article angles, draft polished Chinese articles, and produce publishing-ready Markdown and HTML. The workflow can also generate cover media and assist with WeChat draft publishing when the user intentionally configures the required credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish generated content and media to a WeChat Official Account when account credentials are configured. <br>
Mitigation: Keep automatic publishing disabled until the article, cover media, and destination account are reviewed and explicitly approved. <br>
Risk: The artifact includes credential setup guidance and example-looking WeChat secrets that could be mistaken for safe defaults. <br>
Mitigation: Remove or replace example credentials before use, rotate any real credentials that may have been exposed, and store secrets only in environment variables or a managed secret store. <br>
Risk: Proxy and account-management code can route WeChat API traffic through configured endpoints. <br>
Mitigation: Do not set a WeChat proxy URL unless the endpoint is fully controlled and reviewed by the user or organization. <br>
Risk: Generated persuasive articles may include inaccurate, stale, or overconfident claims from web and video research. <br>
Mitigation: Verify source links, dates, statistics, and claims before publishing, and retain the mandatory user approval step for topic and outline decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeffli2002/jeffli-content-factory) <br>
- [API key setup guide](API_KEY_SETUP.md) <br>
- [Configuration guide](CONFIGURATION.md) <br>
- [YouTube research checklist](references/youtube_research_checklist.md) <br>
- [WeChat viral frameworks](references/wechat_viral_frameworks.md) <br>
- [WeChat format rules](references/wechat-format-rules.md) <br>
- [WeChat publish rules](references/WECHAT_PUBLISH_RULES.md) <br>
- [Cover photo guide](scripts/COVER_PHOTO_GUIDE.md) <br>
- [Zhipu AI platform](https://open.bigmodel.cn/) <br>
- [WeChat Official Account platform](https://mp.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown articles, styled HTML, social post variants, cover image files, and publishing guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save generated assets to an output directory and may call external research, image generation, and WeChat publishing services when configured.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
