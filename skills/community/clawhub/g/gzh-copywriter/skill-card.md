## Description: <br>
公众号文案创作工具，基于红狐数据公众号爆款雷达按关键词检索热门文章，分析流量规律，并生成可发布的完整文章。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
公众号号主、内容运营和品牌策划人员使用该技能按关键词检索公众号爆款文章，分析标题、开头、结构、互动和高频词规律，并生成约 1500 字的可发布公众号文案。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A plaintext RedFox API key is present in the artifact evidence. <br>
Mitigation: Do not use the bundled key; create a separate RedFox key with revocation controls, and rotate or remove any exposed key before use. <br>
Risk: Personal writing samples, drafts, client material, or regulated data may be processed while adapting the output style. <br>
Mitigation: Avoid providing private or confidential material and review generated copy before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/gzh-copywriter) <br>
- [公众号趋势数据格式说明](references/gzh_trend_data_format.md) <br>
- [RedFox Official Account viral search API](https://redfox.hk/story/api/gzh/search/hotArticle) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown article draft with recommended titles, full body copy, core viewpoint, tags, differentiation notes when applicable, and viral formula sources.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY for trend retrieval; default search covers the last 7 days and can expand to 30 days when samples are insufficient.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
