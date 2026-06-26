## Description: <br>
Helps agents prepare WeChat Official Account articles with publishing guidance, layout templates, image upload support, and draft creation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenyd002025](https://clawhub.ai/user/chenyd002025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content teams and developers use this skill to format WeChat Official Account articles, upload article images, and prepare drafts for manual review and publishing in WeChat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled Python scripts disable HTTPS certificate verification while handling WeChat credentials and upload requests. <br>
Mitigation: Restore TLS certificate verification before running those scripts, or use the documented curl workflow with normal certificate verification. <br>
Risk: The skill requires WeChat Official Account AppID and AppSecret values. <br>
Mitigation: Keep config.json out of source control and shared folders, and avoid pasting real secrets into shell history. <br>
Risk: Publishing workflows can upload unintended images or draft article content to a WeChat account. <br>
Mitigation: Confirm each image, generated article, and WeChat draft manually before final publication. <br>


## Reference(s): <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com) <br>
- [WeChat Official Account API Documentation](https://developers.weixin.qq.com/doc/offiaccount/) <br>
- [Professional Article Template](assets/templates/professional.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce WeChat draft metadata and image URL JSON when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
