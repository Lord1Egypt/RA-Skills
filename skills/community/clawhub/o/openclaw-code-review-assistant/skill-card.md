## Description: <br>
自动化代码审查助手，支持 PR 审查、代码质量分析、潜在 bug 检测、安全漏洞扫描。 <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[keven0706](https://clawhub.ai/user/keven0706) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers can invoke this skill as a demonstration code review assistant for file, diff, and pull request review workflows. Its reports should be treated as illustrative guidance rather than assurance because the security evidence says outputs may be canned and unrelated to the user's code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may present canned code review and security findings that are unrelated to the user's actual code. <br>
Mitigation: Use it only as a demo or placeholder, and do not rely on its output for merge decisions, CI gates, or security assurance. <br>
Risk: The PR workflow references GITHUB_TOKEN even though the evidence says real PR analysis is not implemented. <br>
Mitigation: Do not provide a GitHub token unless the implementation is replaced with transparent PR analysis and least-privilege credential handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keven0706/openclaw-code-review-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports and terminal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are generated as single-stream text; PR review mode references GITHUB_TOKEN but the evidence says not to provide a token unless the implementation is replaced with real, transparent PR analysis and least-privilege handling.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
