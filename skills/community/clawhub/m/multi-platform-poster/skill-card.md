## Description: <br>
Adapts and prepares content for publishing across WeChat, Weibo, Zhihu, Xiaohongshu, and Douyin, including platform-specific formatting, scheduling, and performance tracking guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daimingvip-a11y](https://clawhub.ai/user/daimingvip-a11y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, operators, and marketing teams use this skill to turn one source article into platform-specific publishing drafts and posting plans for multiple Chinese social platforms. It is intended to reduce manual formatting, scheduling, and post-publication tracking work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connected social-media account credentials and API secrets could be exposed or over-scoped. <br>
Mitigation: Configure only the platforms needed, keep secrets out of chat, and store credentials in the host platform's secret management or environment configuration. <br>
Risk: Adapted content or schedules could publish incorrect, sensitive, or unintended public posts. <br>
Mitigation: Review each platform-specific draft, target platform, and scheduled time before confirming publication. <br>
Risk: Dependent publishing, rewriting, or image-handling skills may introduce separate behavior or security risks. <br>
Mitigation: Review and approve dependent skills separately before using them in a publishing workflow. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/daimingvip-a11y/multi-platform-poster) <br>
- [WeChat Official Account developer documentation](https://developers.weixin.qq.com/doc/offiaccount/) <br>
- [Weibo open platform documentation](https://open.weibo.com/wiki/) <br>
- [Zhihu developer documentation](https://www.zhihu.com/developers) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with configuration snippets, adapted post drafts, confirmation prompts, publishing status tables, and performance summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include platform-specific links, schedules, account authorization notes, and review prompts before publishing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
