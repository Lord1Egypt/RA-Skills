## Description: <br>
查询 GitHub Trending 热门项目，支持按编程语言、日期范围、口语（文档语言）筛选。当用户想了解 GitHub 今日/本周/本月热门项目、特定语言的热门仓库、或中文文档的热门项目时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[langlyyy](https://clawhub.ai/user/langlyyy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to construct GitHub Trending repository or developer links filtered by programming language, daily/weekly/monthly time window, and spoken documentation language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is reviewed for constructing GitHub Trending links only; requests for tokens, shell commands, local file access, or repository changes are outside its reviewed scope. <br>
Mitigation: Use the skill only to build and explain GitHub Trending URLs, and treat any future behavior requesting credentials, execution, or data modification as out of scope. <br>
Risk: GitHub Trending pages and filter values can change over time, so generated links may not always produce the expected view. <br>
Mitigation: Open the generated GitHub Trending link and verify that the displayed filters match the requested language, time range, and spoken language. <br>


## Reference(s): <br>
- [GitHub Trending](https://github.com/trending) <br>
- [GitHub Trending Developers](https://github.com/trending/developers) <br>
- [GitHub Trending Programming Language Parameters](references/languages.md) <br>
- [GitHub Trending Spoken Language Parameters](references/spoken-languages.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/langlyyy/github-trending-project) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with GitHub Trending links and brief parameter explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include constructed URLs for GitHub Trending repositories or developers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
