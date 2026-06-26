## Description: <br>
Git Deploy stages local repository changes, commits them with a supplied message, and pushes the current branch for quick local deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sirenday](https://clawhub.ai/user/sirenday) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to automate a local Git deployment loop: stage repository changes, commit with a supplied message, and push the current branch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports an exposed plaintext repository token. <br>
Mitigation: Revoke or rotate the token, remove secrets from the skill, and use normal Git credential handling before installation or execution. <br>
Risk: The skill can stage, commit, and push all local changes with little user control. <br>
Mitigation: Review status and diff output, then confirm the remote, branch, and commit message before running the deployment script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sirenday/git-deploy) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/sirenday) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify repository state by staging, committing, and pushing changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
