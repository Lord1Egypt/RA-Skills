## Description: <br>
Commit and push local project changes to GitHub, with optional repo creation and deployment hints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cruciata](https://clawhub.ai/user/cruciata) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare GitHub deployment steps for local projects, including git checks, commits, pushes, optional remote setup, optional repository creation, and deployment hints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented command references `github-deploy-skill.ps1`, but that script is not included in the package. <br>
Mitigation: Do not run the command unless the script is supplied from a trusted source and reviewed first. <br>
Risk: The workflow can commit, push, change remotes, or create a GitHub repository in the wrong destination. <br>
Mitigation: Before use, inspect `git status` and `git diff`, confirm the repository and branch, and verify the authenticated GitHub CLI account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cruciata/github-deploy-skill) <br>
- [Publisher profile](https://clawhub.ai/user/cruciata) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with PowerShell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Git, network access to a remote Git host, and GitHub CLI authentication when repository creation is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
