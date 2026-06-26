## Description: <br>
提交前质量闸门。快速完成本地测试、静态检查和风险审查，判断“是否可提交”。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasilva](https://clawhub.ai/user/chinasilva) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill before committing or opening a PR to run a focused local quality gate, summarize changed files, report lint/type/test/build results, and list blocking or risky findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run repository-defined npm, test, build, workflow:check, and gate:db scripts that can access local services or environment variables. <br>
Mitigation: Review the repository scripts first and run the skill only in an appropriate local development environment with expected services and credentials. <br>
Risk: Manual UI smoke testing is required for UI changes, so automated checks alone may miss layout or interaction regressions. <br>
Mitigation: Keep UI findings marked as not executed or risky until a human completes the smoke checks described by the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chinasilva/peter-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with command results, risk findings, and a commit readiness conclusion] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports whether review covered workspace changes or the latest HEAD commit when the workspace is empty.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
