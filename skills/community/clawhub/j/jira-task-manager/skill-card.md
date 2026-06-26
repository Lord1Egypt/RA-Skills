## Description: <br>
Jira automation for JiraATX project DS: create, update, comment on, transition, and list issues; sync repositories; and support issue-driven task workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clairproqc-star](https://clawhub.ai/user/clairproqc-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage Jira issues for project DS and coordinate issue-driven repository work, including branch setup and test execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says this version may include hidden shared Jira credentials. <br>
Mitigation: Do not install until embedded Jira tokens are removed and rotated; require explicit user-provided credentials through documented environment variables. <br>
Risk: The security review flags broad local code-execution capabilities. <br>
Mitigation: Require manual review and explicit user confirmation before repository sync, branch changes, issue updates, comments, transitions, or local test execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/clairproqc-star/jira-task-manager) <br>
- [Publisher Profile](https://clawhub.ai/user/clairproqc-star) <br>
- [Jira Resources Reference](references/jira.md) <br>
- [Repository Mapping Reference](references/repos.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Jira credentials and local repository configuration before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
