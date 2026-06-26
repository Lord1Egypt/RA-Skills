## Description: <br>
Omni 内容发布器：一篇文章适配公众号/小红书/知乎/抖音，批量生成多平台版本 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and content operators use this skill to convert one Markdown article into platform-specific drafts for WeChat, Xiaohongshu, Zhihu, and Douyin. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated files such as article_wechat.md can overwrite existing files with the same generated name. <br>
Mitigation: Run the tool in a dedicated output directory or check generated filenames before writing outputs. <br>
Risk: Automated platform adaptation can shorten or reformat article content in ways that change emphasis. <br>
Mitigation: Review each generated platform draft before publishing it externally. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/utopiabenben/omnipublisher) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown files with CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a user-selected Markdown input file and writes platform-specific Markdown outputs to the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
