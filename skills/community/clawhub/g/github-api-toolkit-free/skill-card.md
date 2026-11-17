## Description: <br>
Guides agents through GitHub REST API operations for repositories, issues, pull requests, branches, and commits using CLI and Python examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide agents in scripted GitHub REST API workflows such as listing or updating repositories, creating and closing issues, reviewing pull requests, and inspecting branches or commits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may perform high-impact GitHub write actions such as creating, updating, closing, commenting on, or merging repository content. <br>
Mitigation: Require explicit user confirmation before any write, close, comment, merge, or repository-changing request is executed. <br>
Risk: Broad GitHub token scopes can expose private repositories or workflow controls beyond the task's needs. <br>
Mitigation: Use the narrowest viable GitHub token scopes and avoid granting workflow access unless the requested operation requires it. <br>
Risk: GitHub tokens may be leaked through hardcoded values, command history, or logs. <br>
Mitigation: Provide tokens through environment variables or a secrets manager, redact authorization headers from logs, and rotate tokens regularly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/github-api-toolkit-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [GitHub REST API base URL](https://api.github.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with bash, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include GitHub API request examples, token setup guidance, structured response examples, and operational cautions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
