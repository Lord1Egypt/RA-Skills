## Description: <br>
OC PR Review guides an agent through GitHub Pull Request review with GitHub CLI, covering security, test coverage, performance, code quality, Markdown reporting, and optional Feishu notification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[penghang1223](https://clawhub.ai/user/penghang1223) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect GitHub Pull Requests, analyze changed files, assess security, tests, performance, and code quality, and produce an actionable review report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill with an authenticated GitHub CLI session can expose private Pull Request metadata and diffs to the agent. <br>
Mitigation: Confirm the target repository and Pull Request before inspection, and use an account or token with only the repository access needed for the review. <br>
Risk: Optional GitHub review comments or Feishu notifications can disclose review findings or private repository details to the wrong audience. <br>
Mitigation: Before sending or posting, confirm the recipient, review type, target Pull Request, and exact message content. <br>


## Reference(s): <br>
- [OC PR Review on ClawHub](https://clawhub.ai/penghang1223/oc-pr-review) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown review reports with inline GitHub CLI commands and checklist findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated GitHub CLI session; may optionally prepare GitHub review comments or Feishu notification summaries for user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
