## Description:

自动化代码审查助手，支持 PR 审查、代码质量分析、潜在 bug 检测、安全漏洞扫描。

This skill is ready for commercial/non-commercial use.

## Publisher:

[keven0706](https://clawhub.ai/user/keven0706)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to request code review-style reports for files, git diffs, and pull requests. Server security evidence warns that reported findings are canned and should not be trusted for code quality, security review, PR approval, or CI gating without real analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may present canned code review and security findings as if they were based on the user's code.

Mitigation: Do not use its output for code quality decisions, security review, PR approval, or CI gating unless the author replaces the canned reports with real analysis or clearly labels the behavior as a demo.

Risk: Users may over-trust security or bug findings that are not derived from the inspected files.

Mitigation: Treat reports as illustrative guidance only and verify any findings with an independent review or trusted scanner before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keven0706/skills/openclaw-code-review-assistant)
- [Publisher profile](https://clawhub.ai/user/keven0706)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style terminal text with sample findings, summaries, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The review and diff commands emit fixed sample findings; pull request review reports that GitHub integration is not configured unless a token is available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
