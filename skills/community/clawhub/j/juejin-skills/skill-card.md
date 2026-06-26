## Description: <br>
掘金技术社区一站式操作技能，支持热门文章排行榜查询、Markdown 文章发布（默认草稿）和文章下载保存为 Markdown。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wscats](https://clawhub.ai/user/wscats) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content authors use this skill to query Juejin article rankings, create reviewed Juejin drafts from Markdown, and save selected Juejin articles as Markdown files. It is intended for explicit Juejin workflows where the user provides the target article, account action, or local Markdown input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A stored Juejin session cookie can act as the user's Juejin account while it remains valid. <br>
Mitigation: Use the skill only on trusted local machines, avoid shared or CI environments, and delete ~/.juejin_cookie.json when authenticated access is no longer needed. <br>
Risk: Publishing content could make user-provided Markdown visible on Juejin if public publishing is confirmed. <br>
Mitigation: Keep the default draft workflow, review generated drafts before publishing, and require explicit confirmation for public publication. <br>
Risk: Article downloads can write files and images locally. <br>
Mitigation: Use the configured output directory, rely on the documented output path validation, and confirm bulk downloads before enabling them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wscats/juejin-skills) <br>
- [Publisher profile](https://clawhub.ai/user/wscats) <br>
- [Project homepage](https://github.com/wscats/juejin) <br>
- [Juejin website](https://juejin.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, text summaries, command snippets, and local Markdown files for downloaded articles] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store a local Juejin session cookie and may write downloaded article content under the configured output directory.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
