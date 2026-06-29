## Description: <br>
Drafts, restructures, reviews, and optionally submits GitHub issues from findings, bugs, security reviews, regressions, feature requests, or technical debt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiluoduyu](https://clawhub.ai/user/xiluoduyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to turn investigation findings, bugs, security concerns, feature requests, or technical debt into actionable GitHub issues with appropriate evidence, impact, recommendations, and acceptance criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Issue submission can expose secrets, private credentials, or sensitive exploit details if the user-provided issue body is not reviewed. <br>
Mitigation: Before submitting, confirm the target repository and review the issue title and body for secrets, private credentials, and excessive exploit detail. <br>


## Reference(s): <br>
- [Issue Writer on ClawHub](https://clawhub.ai/xiluoduyu/issue-writer) <br>
- [Bug Or Regression Issue Shape](references/bug-issue.md) <br>
- [Epic Or Technical Debt Issue Shape](references/epic-issue.md) <br>
- [Security Issue Shape](references/security-issue.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown issue drafts with optional inline shell commands for GitHub submission] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce issue titles, issue bodies, acceptance criteria, recommendations, and user-reviewed submission commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
