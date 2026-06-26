## Description: <br>
Converts Markdown into WeChat-compatible HTML, can create WeChat draft articles, and can push Markdown content to Juejin drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ysdhb](https://clawhub.ai/user/ysdhb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and content operators use this skill to convert Markdown articles into WeChat-ready HTML, prepare WeChat drafts, and create or update Juejin drafts from Markdown content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses WeChat AppSecret and Juejin cookie values as account credentials. <br>
Mitigation: Keep config.yaml private, restrict file permissions, and do not commit or share credential-bearing configuration files. <br>
Risk: Push commands can send Markdown content and referenced local images to WeChat or Juejin services. <br>
Mitigation: Review the Markdown, generated HTML, and referenced local images before running any push command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ysdhb/mukun-md-push-wechat) <br>
- [README](README.md) <br>
- [WeChat credential configuration guide](how_to_config_wechat.md) <br>
- [Default article style configuration](references/article_default.yaml) <br>
- [Modern article style configuration](references/article_modern.yaml) <br>
- [Scholar article style configuration](references/article_scholar.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated HTML files and draft-publishing actions when scripts are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local HTML files, read local Markdown and image files, and send article content or images to WeChat or Juejin when push commands are used.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
