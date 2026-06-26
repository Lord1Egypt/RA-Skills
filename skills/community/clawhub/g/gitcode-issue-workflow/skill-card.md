## Description: <br>
End-to-end GitCode issue workflow covering issue pickup, analysis, code modification, and PR submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guitenbay](https://clawhub.ai/user/guitenbay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage GitCode issue-driven code changes: fetch and analyze issue context, validate a design, modify a confirmed local repository, and prepare a branch, commit, and pull request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Access tokens may be exposed if stored in MEMORY.md, pasted into URLs, or captured in shell history and logs. <br>
Mitigation: Prefer authenticated gitcode CLI sessions or a secure environment or credential store; do not store tokens in MEMORY.md or include them in URLs. <br>
Risk: Temporary cleanup commands can delete unintended files if run from the wrong directory or against the wrong temp path. <br>
Mitigation: Verify the exact temp/ path before running cleanup commands and keep generated workflow files scoped to the workspace temp directory. <br>
Risk: Repository write actions such as pushes, PR creation, or issue comments can affect external projects. <br>
Mitigation: Require explicit user confirmation for external write actions, push only to a personal fork, and confirm the target branch and remote before submission. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/guitenbay/gitcode-issue-workflow) <br>
- [GitCode API Reference](references/gitcode-api.md) <br>
- [gitcode CLI](https://github.com/codeasier/gitcode-cli) <br>
- [GitCode API Base URL](https://api.gitcode.com/api/v5) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, API examples, PR body templates, and JSON payload snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires gitcode CLI, git, a GitCode token, and user confirmation before local edits or external write actions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
