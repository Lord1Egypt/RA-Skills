## Description: <br>
掘金自动发布 - 一键发布文章到掘金，支持定时发布、标签优化、封面设置。适合：内容创作者、技术博主。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators and technical bloggers use this skill to prepare, schedule, and publish Markdown articles to Juejin with tag, summary, and cover settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to store a full Juejin login cookie. <br>
Mitigation: Treat the cookie like a password, keep it out of shared or committed files, and use an account that is acceptable for automation. <br>
Risk: The skill supports automatic and batch public publishing. <br>
Mitigation: Disable automatic or batch publishing unless there are clear manual review controls for every post. <br>
Risk: The skill references Python scripts that are not included in the artifact. <br>
Mitigation: Inspect the local scripts before running any generated command. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yang1002378395-cmyk/juejin-auto-publisher) <br>
- [Juejin article draft API endpoint](https://api.juejin.cn/content_api/v1/article_draft/create) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, YAML, JSON, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a Juejin login cookie supplied by the user.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
