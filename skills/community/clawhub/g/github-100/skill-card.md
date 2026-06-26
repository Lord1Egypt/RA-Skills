## Description: <br>
Interact with GitHub using the `gh` CLI for issues, pull requests, workflow runs, and advanced API queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Keyserkazi1](https://clawhub.ai/user/Keyserkazi1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository maintainers use this skill to have an agent form GitHub CLI commands for inspecting pull requests, issues, workflow runs, logs, and GitHub API responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can suggest GitHub CLI commands that act with the permissions of the locally authenticated `gh` account. <br>
Mitigation: Confirm the active GitHub account and review commands that create, edit, delete, merge, rerun, cancel, publish, or change repository settings before execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/Keyserkazi1/github-100) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may need repository identifiers, pull request or issue numbers, workflow run IDs, and authenticated GitHub CLI context.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
