## Description: <br>
Generate beautiful knowledge concept cards from book summaries, notes, or topics, with core concepts, quotes, and branding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackyken](https://clawhub.ai/user/jackyken) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to turn book summaries, course notes, meeting insights, or topic overviews into visual knowledge concept cards. It extracts four to five concepts, generates a PNG card, and can send the image back through the active chat channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu delivery uses app credentials and raw messaging APIs to upload and send generated card images. <br>
Mitigation: Use least-privileged Feishu credentials, store them outside prompts, and verify the target recipient or group before sending. <br>
Risk: Generated card content may be uploaded externally or rendered with remote Google Fonts requests. <br>
Mitigation: Avoid sensitive source content when external upload or third-party font network requests are not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackyken/knowledge-card) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu image upload API](https://open.feishu.cn/open-apis/im/v1/images) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with JSON arguments and shell commands; generated artifact is a PNG image file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated card is rendered at 800px display width with a 3x PNG capture; Feishu delivery requires app credentials and a verified recipient or group.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
