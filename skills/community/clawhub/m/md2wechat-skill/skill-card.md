## Description: <br>
Converts Markdown into WeChat Official Account-compatible inline-styled HTML and can upload the result as a WeChat draft. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[koraiHub](https://clawhub.ai/user/koraiHub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content operators, and agent users can use this skill to prepare Markdown articles for WeChat Official Accounts, generate local HTML previews, and optionally create WeChat draft posts with uploaded images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft upload mode uses WeChat public-account credentials. <br>
Mitigation: Keep .env files private, use convert-only mode when upload is not needed, and rotate the WeChat secret if it may have been exposed. <br>
Risk: Draft mode sends Markdown content and referenced images to WeChat. <br>
Mitigation: Use draft mode only for content and images that are approved for upload to the configured WeChat account. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/koraiHub/md2wechat-skill) <br>
- [Publisher profile](https://clawhub.ai/user/koraiHub) <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files, HTML, API calls] <br>
**Output Format:** [Markdown guidance with shell commands; generated WeChat-compatible HTML files and optional WeChat draft uploads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3. Draft upload mode requires WECHAT_APPID and WECHAT_SECRET; convert-only mode does not require WeChat credentials.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
