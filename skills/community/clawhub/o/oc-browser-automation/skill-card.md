## Description: <br>
封装 OpenClaw browser 工具，用于网页导航、截图、快照、点击、输入、等待、标签页管理、上传和下载等浏览器自动化操作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaoren36-arch](https://clawhub.ai/user/gaoren36-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to drive browser sessions for web testing, page inspection, form entry, screenshots, downloads, uploads, and other interactive web workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can act in logged-in sessions or on private pages. <br>
Mitigation: Use an isolated browser profile and require explicit confirmation before logins, form submissions, purchases, account changes, or other sensitive actions. <br>
Risk: The skill supports uploads and downloads, which can transfer local or remote files. <br>
Mitigation: Confirm file paths, destination pages, and download intent before executing upload or download actions. <br>


## Reference(s): <br>
- [ClawHub skill release: OpenClaw 浏览器自动化](https://clawhub.ai/gaoren36-arch/oc-browser-automation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline browser command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser actions may operate on authenticated sessions and local file transfers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
