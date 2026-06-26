## Description: <br>
Publishes completed Markdown or text articles to a WeChat Official Account draft box by converting them to compliant HTML, uploading images, and submitting the draft; it does not generate article content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youyouyoumagic](https://clawhub.ai/user/youyouyoumagic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External publishers and developers use this skill to prepare finished article content and image files for WeChat Official Account publication. It helps an agent produce WeChat-compatible HTML, upload assets, submit a draft, and tell the user to review it before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WeChat account secrets may be stored in a plaintext local configuration file. <br>
Mitigation: Prefer passing credentials at runtime; if credentials are saved, protect and exclude artifact/scripts/.wechat-config.json from backups and version control. <br>
Risk: Selected article content and images are uploaded to WeChat during draft creation. <br>
Mitigation: Install and use the skill only when uploading that content to WeChat is intended, and review the created draft before publishing. <br>
Risk: The skill includes a fixed footer and disclaimer rule that may not match every account. <br>
Mitigation: Remove or customize the fixed “有用AI” footer and disclaimer behavior before using it for a different publisher. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/youyouyoumagic/magicx-wechat-publisher) <br>
- [WeChat access token endpoint](https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}) <br>
- [WeChat image upload endpoint](https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={TOKEN}) <br>
- [WeChat permanent image material endpoint](https://api.weixin.qq.com/cgi-bin/material/add_material?type=image&access_token={TOKEN}) <br>
- [WeChat draft add endpoint](https://api.weixin.qq.com/cgi-bin/draft/add?access_token=${accessToken}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated WeChat HTML submitted through WeChat APIs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WeChat Official Account credentials and sends selected article content and images to WeChat; the resulting draft should be reviewed in the WeChat backend before publication.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
