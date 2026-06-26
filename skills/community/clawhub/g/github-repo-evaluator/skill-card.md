## Description: <br>
GitHub项目调研器通过 GitHub API 搜索和采集仓库数据，帮助用户对开源项目进行系统化对比并生成结构化推荐报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudyli](https://clawhub.ai/user/cloudyli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical evaluators use this skill to search, compare, and assess GitHub repositories against user requirements. It produces structured recommendations using repository popularity, activity, issues, documentation, roadmap, and technology-stack signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository names, search terms, and public GitHub metadata lookups are sent to GitHub. <br>
Mitigation: Avoid using confidential internal project names or sensitive search terms when running repository searches. <br>
Risk: GitHub CLI requests may use the currently logged-in GitHub account. <br>
Mitigation: Confirm the active GitHub CLI account and permissions before issuing authenticated lookup commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cloudyli/github-repo-evaluator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with comparison tables, recommendations, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live GitHub API or GitHub CLI data; results depend on public repository metadata, authentication context, and rate limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
