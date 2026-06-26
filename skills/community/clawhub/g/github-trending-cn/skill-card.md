## Description: <br>
GitHub 趋势监控 | GitHub Trending Monitor. 获取 GitHub 热门项目、编程语言趋势、开源动态 | Get GitHub trending repos, language trends, open source updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and open source watchers use this skill to ask for GitHub trending repositories, language-specific trend lists, popular developers, and emerging projects over daily, weekly, or monthly windows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may return sample or stale GitHub Trending data rather than live trend results. <br>
Mitigation: Treat generated rankings as potentially stale unless the skill fetches current GitHub data and cites the source used for the response. <br>
Risk: Broad trigger terms may invoke the skill during general GitHub discussions. <br>
Mitigation: Use explicit prompts for trending lookups and review whether the skill response is relevant before relying on it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON-formatted repository rankings and descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require python3 and curl; scanner guidance notes results may be sample or stale unless live GitHub data is fetched and cited.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
