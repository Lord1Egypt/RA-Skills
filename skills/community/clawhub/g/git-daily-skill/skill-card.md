## Description: <br>
今日 Git 提交日报助手 —— 自动扫描当天（含次日凌晨6点前）所有仓库的 commit 记录，生成结构化日报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenneychen](https://clawhub.ai/user/kenneychen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scan local Git repositories and produce a daily summary of their own commits across a 06:00-to-next-day-05:59 work window. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated report can expose private repository names, commit messages, ticket IDs, author names, timestamps, and local paths. <br>
Mitigation: Use a specific --root directory and review the report before sharing it outside the intended audience. <br>
Risk: Scanning a broad workspace may include repositories the user did not intend to summarize. <br>
Mitigation: Limit the scan root and depth to the repositories needed for the daily report. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/kenneychen/git-daily-skill) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Human-readable text or JSON commit activity report, with agent-facing Markdown summaries when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include repository paths, commit hashes, author names, timestamps, and commit messages from local Git history.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md body) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
