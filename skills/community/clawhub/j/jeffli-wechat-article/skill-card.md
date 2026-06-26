## Description: <br>
微信公众号文章抓取工具，可将微信公众号文章转换为 Markdown，并支持图片本地下载。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffli2002](https://clawhub.ai/user/jeffli2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and AI-agent users can use this skill to archive WeChat Official Account articles as local Markdown files with optional downloaded images. It supports direct CLI use and MCP tool integration for converting single articles or batches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs browser automation and scraper code against WeChat pages. <br>
Mitigation: Install only if comfortable running a Python scraper with browser automation, and use it only for WeChat articles you are allowed to archive. <br>
Risk: The skill saves article content, debug HTML, and optional image files locally. <br>
Mitigation: Keep output in a dedicated directory and delete output or debug folders when they may contain content you do not want retained. <br>
Risk: Dependencies in the artifact are not pinned to exact versions. <br>
Mitigation: Review dependency versions before deployment and pin approved versions in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeffli2002/jeffli-wechat-article) <br>
- [scripts/README.md](scripts/README.md) <br>
- [Camoufox](https://github.com/nichochar/camoufox) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown files with YAML frontmatter and local image assets; MCP tools return text summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written under an article-title directory; images may remain remote when downloads fail or image download is disabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
