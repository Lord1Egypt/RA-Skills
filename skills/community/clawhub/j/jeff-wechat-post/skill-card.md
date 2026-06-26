## Description: <br>
微信公众号/朋友圈营销内容智能体。输入产品/服务主题、卖点、讲师信息、配图需求，输出专业文案+结构化配图。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffli2002](https://clawhub.ai/user/jeffli2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers, sales teams, and content creators use this skill to gather WeChat campaign details and produce Chinese WeChat Moments copy, image prompts, poster images, QR-code composites, and a final Markdown delivery package. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Campaign prompts, contact details, QR-code settings, and generated image requests may be sent to third-party image services. <br>
Mitigation: Use dedicated API keys, avoid sensitive personal data in prompts, and review campaign content before submitting it to KIE.ai or Seedream/Volcengine. <br>
Risk: The KIE callback workflow can expose an unauthenticated callback endpoint and save inbound request data. <br>
Mitigation: Bind callbacks to localhost when possible, use a public tunnel only when required, restrict tunnel lifetime, and delete callback logs after use. <br>
Risk: Saved QR-code preferences and generated campaign files may contain personal contact information. <br>
Mitigation: Store only user-provided QR codes, keep output directories access-controlled, and remove saved QR settings and generated files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeffli2002/jeff-wechat-post) <br>
- [Copy Template](references/workflow/copy-template.md) <br>
- [Image Layout - WeChat Moments Poster](references/workflow/image-layout.md) <br>
- [QR Code Configuration](references/config/qrcode-schema.md) <br>
- [dark-warm palette](references/palettes/dark-warm.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, API calls] <br>
**Output Format:** [Markdown files, image prompts, PNG image outputs, QR-code composite files, and shell-command workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a wechat-post/{topic-slug}/ workspace with copy.md, prompts/image-prompt.md, optional qrcode_setting.txt, a PNG poster, and wechat-post-complete.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
