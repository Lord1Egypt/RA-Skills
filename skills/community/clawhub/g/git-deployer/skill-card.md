## Description: <br>
Pushes static site content to GitHub Pages or other git-backed hosts by cloning or initializing a target repository, copying local files, committing changes, and force-pushing the selected branch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kryzl19](https://clawhub.ai/user/kryzl19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy or sync local static site output to GitHub Pages repositories or other git-backed hosting branches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Force-pushing can overwrite the target Git branch and replace existing remote history. <br>
Mitigation: Verify the site directory, remote URL, branch, and Git identity before running; avoid shared or protected branches unless history replacement is intended and backed up. <br>
Risk: The deployment can reuse a temporary clone path, which may contain unexpected local state. <br>
Mitigation: Inspect or remove the temporary clone before deployment, and prefer a disposable or validated clone path for sensitive repositories. <br>
Risk: The script uses configured Git credentials to push to the supplied remote. <br>
Mitigation: Use a scoped deploy key or token limited to the intended repository. <br>


## Reference(s): <br>
- [Git Deployer ClawHub Page](https://clawhub.ai/kryzl19/git-deployer) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and deployment status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports success or failure, commit hash, remote URL, branch, and temporary clone path when the deployment script runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
