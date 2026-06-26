## Description: <br>
用于每周自动分析 Git 提交记录，生成包含技术挑战、性能优化及 AI 提效维度的深度复盘报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Raccoon-Office](https://clawhub.ai/user/Raccoon-Office) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review the current user's last seven days of Git commits and diffs, then produce a concise weekly technical retrospective focused on technical challenges, performance and stability work, AI-assisted productivity, and next-step recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read recent Git history and full patch diffs from the current repository when triggered. <br>
Mitigation: Use explicit triggers such as "git-weekly" and review generated reports for sensitive code, credentials, or internal implementation details before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Raccoon-Office/git-weekly) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, analysis, markdown, guidance] <br>
**Output Format:** [Markdown weekly retrospective with referenced Git analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads recent Git history and patch diffs from the current repository when triggered.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
