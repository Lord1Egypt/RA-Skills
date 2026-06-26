## Description: <br>
将 Markdown 转换为数十种精美主题 HTML，并一键推送到微信公众号草稿箱（支持自动解析文内图片并生成封面）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shijianzhong](https://clawhub.ai/user/shijianzhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content creators, and publishing teams use this skill to format Markdown articles, preview themed HTML output, and create WeChat draft posts through the mpa CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup asks users to run an unpinned remote shell installer for the mpa CLI. <br>
Mitigation: Review the mpa project and installer before running it, and prefer a pinned release or manually downloaded binary with checksum verification. <br>
Risk: Publishing workflows require WeChat credentials and allow the CLI to create drafts and upload article media. <br>
Mitigation: Configure only credentials approved for this use case, and review generated drafts and uploaded media before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shijianzhong/multi-platform-articles) <br>
- [mpa installer script](https://raw.githubusercontent.com/shijianzhong/multi-platform-articles/main/scripts/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide use of mpa to render HTML files and create WeChat draft posts.] <br>

## Skill Version(s): <br>
0.1.18 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
