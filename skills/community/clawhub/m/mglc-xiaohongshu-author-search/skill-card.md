## Description:

按作者名或关键词搜索小红书账号，返回候选作者、公开资料和作者标识，支持分页与表格导出。适合找博主、找同行或确认同名账号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

External users can find candidate Xiaohongshu creators by name or keyword, compare public profile details to distinguish similarly named accounts, and export the results. Depending on the plan, the skill can also collect public posts, details, or comments for evidence-based analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags that the skill can collect posts, post details, and comments beyond the advertised author search, which may incur additional API costs; scanner analysis is partial.

Mitigation: Review the planned collection scope and estimated maximum fee before running paid queries, then check actual coverage and charges in the results.

## Reference(s):

- [ClawHub release](https://clawhub.ai/dunkong/skills/mglc-xiaohongshu-author-search)
- [API key setup](https://api.we-media.cn?source=clawhub&skill=mglc-xiaohongshu-author-search)
- [Usage and pagination guide](references/usage.md)
- [Analysis and evidence format](references/analysis.md)

## Skill Output:

**Output Type(s):** [JSON, CSV, Markdown, HTML, Guidance]

**Output Format:** [Structured author and public content data with optional evidence-based analysis and report exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paged results include observed coverage and cost information; Excel export is optional.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
