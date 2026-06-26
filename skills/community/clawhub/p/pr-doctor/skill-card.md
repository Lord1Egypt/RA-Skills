## Description: <br>
PR全流程质量医生 — 自动化代码审查、测试分析、问题追踪和持续改进的完整流水线 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use PR Doctor to run a Pull Request quality pipeline that reviews code, checks test coverage, creates follow-up GitHub Issues, and records review learnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically create GitHub Issues using the user's GitHub authorization. <br>
Mitigation: Confirm the target repository and GitHub account before execution, and require approval before any write operation when possible. <br>
Risk: Review learnings may be persisted under .learnings/ without an explicit confirmation step. <br>
Mitigation: Review retention expectations before running the skill and inspect persisted learnings for sensitive project details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/pr-doctor) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Files, Guidance] <br>
**Output Format:** [Markdown report with GitHub Issue links and optional console or Feishu delivery] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use GitHub authorization to read PR diffs, create Issues, and write review learnings under .learnings/.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and workflow.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
