## Description: <br>
Fetches Juejin technology article rankings, including category lists and hot or newest article trends by category. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical readers use this skill to discover Juejin article categories and retrieve current ranked articles for topics such as frontend, backend, Android, iOS, AI, development tools, career, and reading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled Node.js script makes automated requests to Juejin, so results depend on the remote service and on sending expected query values. <br>
Mitigation: Use category IDs returned by the categories command, use documented type values such as hot or new, and review returned rankings before relying on them. <br>


## Reference(s): <br>
- [Juejin skill page](https://clawhub.ai/wuchubuzai2018/juejin-article-trends) <br>
- [Juejin](https://juejin.cn/) <br>
- [Juejin category API](https://api.juejin.cn/tag_api/v1/query_category_briefs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return public Juejin category and article ranking data, including titles, authors, counts, tags, article IDs, and URLs.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
