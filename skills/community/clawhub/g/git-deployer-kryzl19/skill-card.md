## Description: <br>
Push static site content to GitHub Pages repositories. Clone, copy files, commit with timestamp, force-push. Use when updating GitHub Pages sites, deploying static sites, or syncing local content to a git-based host. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kryzl19](https://clawhub.ai/user/kryzl19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy a local static site directory to a git-backed host such as GitHub Pages without setting up a separate CI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deployment script can overwrite the target Git branch by force-pushing deployment output. <br>
Mitigation: Use it only with a dedicated deployment repository or branch where overwriting history is acceptable; verify the remote URL and branch before execution and prefer --force-with-lease when adapting the workflow. <br>
Risk: An existing temporary clone with the same repository name may affect what gets fetched, copied, committed, and pushed. <br>
Mitigation: Inspect or remove any existing /tmp clone for the target repository before running the deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with shell command examples and deployment status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local site path, git remote URL, target branch, and preconfigured git credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
